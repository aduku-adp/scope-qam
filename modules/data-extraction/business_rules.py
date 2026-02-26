"""Business-rule validation engine (YAML-driven + SQL checks)."""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RuleOutcome:
    rule_id: str
    level: str
    status: str
    violations: int
    message: str


class BusinessRuleEngine:
    def __init__(self, rules_path: Path) -> None:
        self.rules_path = rules_path
        self.rules = self._load_rules(rules_path)

    @staticmethod
    def _load_rules(rules_path: Path) -> dict[str, Any]:
        if not rules_path.exists():
            return {"payload_rules": []}
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError("PyYAML is required for business-rule validation") from exc
        data = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
        data.setdefault("payload_rules", [])
        return data

    @staticmethod
    def _get_path_value(payload: dict[str, Any], path: str) -> Any:
        current: Any = payload
        for part in path.split("."):
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        return current

    @staticmethod
    def _iter_scalar_paths(value: Any, prefix: str) -> list[tuple[str, Any]]:
        if isinstance(value, dict):
            out: list[tuple[str, Any]] = []
            for key, item in value.items():
                next_prefix = f"{prefix}.{key}" if prefix else key
                out.extend(BusinessRuleEngine._iter_scalar_paths(item, next_prefix))
            return out
        if isinstance(value, list):
            out: list[tuple[str, Any]] = []
            for idx, item in enumerate(value):
                next_prefix = f"{prefix}.{idx}" if prefix else str(idx)
                out.extend(BusinessRuleEngine._iter_scalar_paths(item, next_prefix))
            return out
        return [(prefix, value)]

    def _evaluate_industry_weight_sum(self, payload: dict[str, Any], rule: dict[str, Any]) -> int:
        cfg = rule.get("config", {})
        expected = float(cfg.get("expected_sum", 1.0))
        tolerance = float(cfg.get("tolerance", 0.001))
        risk_items = self._get_path_value(payload, "company_information.industry_risk")
        if not isinstance(risk_items, list) or not risk_items:
            return 1
        weights = [item.get("industry_weight") for item in risk_items if isinstance(item, dict)]
        if any(not isinstance(w, (int, float)) for w in weights if w is not None):
            return 1
        total = sum(float(w) for w in weights if w is not None)
        return 0 if abs(total - expected) <= tolerance else 1

    def _evaluate_score_scale(self, payload: dict[str, Any], rule: dict[str, Any]) -> int:
        cfg = rule.get("config", {})
        allowed_values = {str(v).strip().upper() for v in cfg.get("allowed_values", [])}
        paths = cfg.get("paths", [])
        violations = 0

        flattened = self._iter_scalar_paths(payload, "")
        for path in paths:
            if "*" in path:
                pattern = path.replace("[*]", ".*")
                for p, value in flattened:
                    if fnmatch.fnmatch(p, pattern) and value is not None:
                        if str(value).strip().upper() not in allowed_values:
                            violations += 1
                continue
            value = self._get_path_value(payload, path)
            if value is None:
                continue
            if str(value).strip().upper() not in allowed_values:
                violations += 1
        return violations

    def _evaluate_credit_metrics_year_value_logic(
        self, payload: dict[str, Any], rule: dict[str, Any]
    ) -> int:
        cfg = rule.get("config", {})
        year_regex = re.compile(str(cfg.get("year_regex", r"^[0-9]{4}(E)?$")))
        require_numeric = bool(cfg.get("require_numeric_value", True))
        allow_null_values = bool(cfg.get("allow_null_values", True))
        allow_negative = bool(cfg.get("allow_negative_values", True))
        violations = 0

        for metric in payload.get("credit_metrics", []):
            seen_years: set[str] = set()
            for point in metric.get("values", []):
                year = point.get("year")
                value = point.get("value")

                if not isinstance(year, str) or not year_regex.match(year):
                    violations += 1
                if isinstance(year, str):
                    if year in seen_years:
                        violations += 1
                    seen_years.add(year)

                if value is None and allow_null_values:
                    continue

                if require_numeric and not isinstance(value, (int, float)):
                    violations += 1
                if isinstance(value, (int, float)) and not allow_negative and value < 0:
                    violations += 1

        return violations

    def _evaluate_credit_metrics_outlier(self, payload: dict[str, Any], rule: dict[str, Any]) -> int:
        cfg = rule.get("config", {})
        min_value = float(cfg.get("min_value", -10000.0))
        max_value = float(cfg.get("max_value", 10000.0))
        violations = 0

        for metric in payload.get("credit_metrics", []):
            for point in metric.get("values", []):
                value = point.get("value")
                if value is None:
                    continue
                if not isinstance(value, (int, float)):
                    violations += 1
                    continue
                if value < min_value or value > max_value:
                    violations += 1
        return violations

    @staticmethod
    def _resolve_status(violations: int, fail_threshold: int, warn_threshold: int) -> str:
        if violations >= fail_threshold:
            return "fail"
        if violations >= warn_threshold:
            return "warn"
        return "pass"

    def evaluate_payload(self, payload: dict[str, Any]) -> list[RuleOutcome]:
        outcomes: list[RuleOutcome] = []
        for rule in self.rules.get("payload_rules", []):
            rule_id = str(rule.get("id", "unknown_rule"))
            rule_type = str(rule.get("type", "")).strip()
            level = str(rule.get("severity", "warning")).strip().lower()
            fail_threshold = int(rule.get("fail_threshold", 1))
            warn_threshold = int(rule.get("warn_threshold", 1))

            if rule_type == "industry_weight_sum":
                violations = self._evaluate_industry_weight_sum(payload, rule)
            elif rule_type == "score_scale":
                violations = self._evaluate_score_scale(payload, rule)
            elif rule_type == "credit_metrics_year_value_logic":
                violations = self._evaluate_credit_metrics_year_value_logic(payload, rule)
            elif rule_type == "credit_metrics_outlier":
                violations = self._evaluate_credit_metrics_outlier(payload, rule)
            else:
                continue

            status = self._resolve_status(violations, fail_threshold, warn_threshold)
            outcomes.append(
                RuleOutcome(
                    rule_id=rule_id,
                    level=level,
                    status=status,
                    violations=violations,
                    message=f"{rule_id}: {violations} violation(s)",
                )
            )
        return outcomes
