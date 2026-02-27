"""Snapshot service UT."""

from unittest.mock import create_autospec

import pytest

from api.providers.snapshot_provider import NotFound, SnapshotProvider
from api.snapshot.models import SnapshotModel
from api.snapshot.service import SnapshotService


@pytest.fixture(name="service")
def fix_service():
    return SnapshotService(snapshot_provider=create_autospec(SnapshotProvider))


@pytest.mark.parametrize(
    "snapshots",
    [
        [
            SnapshotModel(
                snapshot_id="COMP1_v1",
                company_id="COMP1",
                company_name="ACME",
                document_version=1,
                is_active=True,
            )
        ]
    ],
)
def test_list_snapshots(service, snapshots):
    service.snapshot_provider.list.return_value = snapshots

    output = service.list_snapshots(company_id="COMP1")

    service.snapshot_provider.list.assert_called_once_with(
        company_id="COMP1",
        from_date=None,
        to_date=None,
        sector=None,
        country=None,
        currency=None,
    )
    assert output == snapshots


def test_get_snapshot(service):
    snapshot = SnapshotModel(
        snapshot_id="COMP1_v1",
        company_id="COMP1",
        company_name="ACME",
        document_version=1,
        is_active=True,
    )
    service.snapshot_provider.get.return_value = snapshot

    output = service.get_snapshot("COMP1_v1")

    service.snapshot_provider.get.assert_called_once_with("COMP1_v1")
    assert output == snapshot


def test_get_snapshot_notfound(service):
    service.snapshot_provider.get.side_effect = NotFound

    with pytest.raises(NotFound):
        service.get_snapshot("UNKNOWN")


def test_get_latest_snapshots(service):
    snapshots = [
        SnapshotModel(
            snapshot_id="COMP1_v1",
            company_id="COMP1",
            company_name="ACME",
            document_version=1,
            is_active=True,
        )
    ]
    service.snapshot_provider.latest.return_value = snapshots

    output = service.get_latest_snapshots()

    service.snapshot_provider.latest.assert_called_once()
    assert output == snapshots

