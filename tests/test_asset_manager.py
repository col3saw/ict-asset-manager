"""
Tests for ICT Asset Manager core functions.
Run with: python -m pytest tests/ -v
"""

import sys
import os
import tempfile
import shutil
import pytest

# Point imports at the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import asset_manager as am


@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Redirect data/reports dirs to a temp directory for each test."""
    monkeypatch.setattr(am, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(am, "ASSETS_FILE", tmp_path / "data" / "assets.csv")
    monkeypatch.setattr(am, "REPORTS_DIR", tmp_path / "reports")
    am.ensure_dirs()
    yield


# ── Asset ID generation ───────────────────────────────────────────────────────

def test_next_id_empty():
    assert am.next_asset_id([]) == "AST-0001"


def test_next_id_sequence():
    assets = [{"asset_id": "AST-0001"}, {"asset_id": "AST-0005"}]
    assert am.next_asset_id(assets) == "AST-0006"


# ── Add & retrieve ────────────────────────────────────────────────────────────

def test_add_asset_returns_id():
    asset = am.add_asset({"name": "Test Switch", "category": "switch", "location": "Harare"})
    assert asset["asset_id"] == "AST-0001"
    assert asset["name"] == "Test Switch"


def test_add_sets_default_status():
    asset = am.add_asset({"name": "Router"})
    assert asset["status"] == "active"


def test_add_multiple_assets():
    am.add_asset({"name": "Asset A"})
    am.add_asset({"name": "Asset B"})
    assets = am.load_assets()
    assert len(assets) == 2
    assert assets[1]["asset_id"] == "AST-0002"


def test_get_existing_asset():
    am.add_asset({"name": "Firewall", "location": "Lusaka"})
    result = am.get_asset("AST-0001")
    assert result is not None
    assert result["name"] == "Firewall"


def test_get_nonexistent_asset():
    assert am.get_asset("AST-9999") is None


# ── Update ────────────────────────────────────────────────────────────────────

def test_update_asset():
    am.add_asset({"name": "Laptop", "status": "active"})
    updated = am.update_asset("AST-0001", {"status": "maintenance", "assigned_to": "J. Doe"})
    assert updated["status"] == "maintenance"
    assert updated["assigned_to"] == "J. Doe"


def test_update_nonexistent_returns_none():
    result = am.update_asset("AST-9999", {"status": "inactive"})
    assert result is None


# ── Delete ────────────────────────────────────────────────────────────────────

def test_delete_asset():
    am.add_asset({"name": "Old Desktop"})
    assert am.delete_asset("AST-0001") is True
    assert am.get_asset("AST-0001") is None


def test_delete_nonexistent_returns_false():
    assert am.delete_asset("AST-9999") is False


# ── Search & filter ───────────────────────────────────────────────────────────

def test_search_by_keyword():
    am.add_asset({"name": "Core Switch", "location": "Harare"})
    am.add_asset({"name": "Firewall", "location": "Lusaka"})
    results = am.search_assets(query="Switch")
    assert len(results) == 1
    assert results[0]["name"] == "Core Switch"


def test_filter_by_location():
    am.add_asset({"name": "Asset A", "location": "Harare"})
    am.add_asset({"name": "Asset B", "location": "Lusaka"})
    results = am.search_assets(location="Lusaka")
    assert len(results) == 1
    assert results[0]["location"] == "Lusaka"


def test_filter_by_status():
    am.add_asset({"name": "Active Device", "status": "active"})
    am.add_asset({"name": "Old Device", "status": "decommissioned"})
    results = am.search_assets(status="decommissioned")
    assert len(results) == 1


# ── Summary report ────────────────────────────────────────────────────────────

def test_summary_report_counts():
    am.add_asset({"name": "A", "category": "laptop", "location": "Harare", "status": "active"})
    am.add_asset({"name": "B", "category": "switch", "location": "Lusaka", "status": "active"})
    report = am.summary_report()
    assert report["total_assets"] == 2
    assert report["by_location"]["Harare"] == 1
    assert report["by_category"]["laptop"] == 1


def test_warranty_expiry_flag(monkeypatch):
    from datetime import date, timedelta
    expiring_soon = (date.today() + timedelta(days=30)).isoformat()
    am.add_asset({"name": "Expiring Device", "warranty_expiry": expiring_soon})
    report = am.summary_report()
    assert len(report["warranty_expiring_soon"]) == 1
    assert report["warranty_expiring_soon"][0]["name"] == "Expiring Device"


# ── CSV import ────────────────────────────────────────────────────────────────

def test_import_csv(tmp_path):
    csv_file = tmp_path / "test_import.csv"
    csv_file.write_text(
        "name,category,location,status\n"
        "Test Switch,switch,Harare,active\n"
        "Test Laptop,laptop,Lusaka,active\n"
    )
    count, errors = am.import_csv(str(csv_file))
    assert count == 2
    assert errors == []


def test_import_csv_missing_name(tmp_path):
    csv_file = tmp_path / "bad_import.csv"
    csv_file.write_text("name,category\n,switch\n")
    count, errors = am.import_csv(str(csv_file))
    assert count == 0
    assert any("missing required field" in e for e in errors)


def test_import_csv_bad_file():
    count, errors = am.import_csv("/nonexistent/path/file.csv")
    assert count == 0
    assert errors
