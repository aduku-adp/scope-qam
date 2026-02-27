"""Health service UT."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from api.health.service import HealthService


def test_health_service_ok(tmp_path: Path):
    (tmp_path / "corporates_A_1.xlsm").write_text("x")
    (tmp_path / "ignore.txt").write_text("x")

    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchone.return_value = (1,)
    conn.cursor.return_value.__enter__.return_value = cursor

    with patch("api.health.service.psycopg2.connect", return_value=conn):
        health = HealthService(corporates_dir=str(tmp_path)).get_health()

    assert health.healthy is True
    assert health.database_ok is True
    assert health.corporates_dir_ok is True
    assert health.corporates_files_count == 1


def test_health_service_db_down(tmp_path: Path):
    (tmp_path / "corporates_A_1.xlsm").write_text("x")

    with patch("api.health.service.psycopg2.connect", side_effect=Exception("db down")):
        health = HealthService(corporates_dir=str(tmp_path)).get_health()

    assert health.healthy is False
    assert health.database_ok is False
    assert "db down" in health.database_message
    assert health.corporates_dir_ok is True


def test_health_service_dir_missing():
    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchone.return_value = (1,)
    conn.cursor.return_value.__enter__.return_value = cursor

    with patch("api.health.service.psycopg2.connect", return_value=conn):
        health = HealthService(corporates_dir="/not/found/path").get_health()

    assert health.healthy is False
    assert health.database_ok is True
    assert health.corporates_dir_ok is False

