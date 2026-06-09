"""
ICT Infrastructure Asset Manager
----------------------------------
A command-line tool for tracking, auditing, and reporting on ICT assets
across distributed enterprise locations.

Author: Farai Murindagomo
"""

import csv
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")
ASSETS_FILE = DATA_DIR / "assets.csv"

VALID_STATUSES = {"active", "inactive", "maintenance", "decommissioned", "missing"}
VALID_CATEGORIES = {"laptop", "desktop", "server", "switch", "router", "firewall",
                    "access_point", "printer", "ups", "phone", "other"}

FIELDNAMES = [
    "asset_id", "name", "category", "make", "model", "serial_number",
    "assigned_to", "location", "status", "purchase_date", "warranty_expiry",
    "ip_address", "notes", "last_updated"
]


# ── File Helpers ──────────────────────────────────────────────────────────────

def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def load_assets() -> list[dict]:
    """Load all assets from CSV into a list of dicts."""
    if not ASSETS_FILE.exists():
        return []
    with open(ASSETS_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_assets(assets: list[dict]):
    """Write all assets back to CSV."""
    ensure_dirs()
    with open(ASSETS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(assets)


def next_asset_id(assets: list[dict]) -> str:
    """Generate the next sequential asset ID."""
    if not assets:
        return "AST-0001"
    ids = [int(a["asset_id"].split("-")[1]) for a in assets if a["asset_id"].startswith("AST-")]
    return f"AST-{max(ids) + 1:04d}"


# ── CRUD Operations ───────────────────────────────────────────────────────────

def add_asset(data: dict) -> dict:
    """Add a new asset record."""
    assets = load_assets()
    asset = {field: "" for field in FIELDNAMES}
    asset.update(data)
    asset["asset_id"] = next_asset_id(assets)
    asset["last_updated"] = date.today().isoformat()
    asset["status"] = asset.get("status", "active").lower()
    assets.append(asset)
    save_assets(assets)
    return asset


def update_asset(asset_id: str, updates: dict) -> dict | None:
    """Update fields on an existing asset."""
    assets = load_assets()
    for asset in assets:
        if asset["asset_id"] == asset_id:
            asset.update(updates)
            asset["last_updated"] = date.today().isoformat()
            save_assets(assets)
            return asset
    return None


def delete_asset(asset_id: str) -> bool:
    """Remove an asset by ID."""
    assets = load_assets()
    filtered = [a for a in assets if a["asset_id"] != asset_id]
    if len(filtered) == len(assets):
        return False
    save_assets(filtered)
    return True


def get_asset(asset_id: str) -> dict | None:
    """Retrieve a single asset by ID."""
    return next((a for a in load_assets() if a["asset_id"] == asset_id), None)


# ── Search & Filter ───────────────────────────────────────────────────────────

def search_assets(query: str = "", location: str = "", category: str = "",
                  status: str = "") -> list[dict]:
    """Filter assets by keyword, location, category, or status."""
    assets = load_assets()
    results = []
    for a in assets:
        if query and query.lower() not in json.dumps(a).lower():
            continue
        if location and a["location"].lower() != location.lower():
            continue
        if category and a["category"].lower() != category.lower():
            continue
        if status and a["status"].lower() != status.lower():
            continue
        results.append(a)
    return results


# ── Reporting ─────────────────────────────────────────────────────────────────

def summary_report() -> dict:
    """Generate a summary of the asset inventory."""
    assets = load_assets()
    total = len(assets)

    by_status = {}
    by_category = {}
    by_location = {}
    warranty_expiring = []

    today = date.today()

    for a in assets:
        # Status breakdown
        s = a.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1

        # Category breakdown
        c = a.get("category", "unknown")
        by_category[c] = by_category.get(c, 0) + 1

        # Location breakdown
        loc = a.get("location", "unknown")
        by_location[loc] = by_location.get(loc, 0) + 1

        # Warranty expiry check (within 90 days)
        exp = a.get("warranty_expiry", "")
        if exp:
            try:
                exp_date = date.fromisoformat(exp)
                delta = (exp_date - today).days
                if 0 <= delta <= 90:
                    warranty_expiring.append({
                        "asset_id": a["asset_id"],
                        "name": a["name"],
                        "warranty_expiry": exp,
                        "days_remaining": delta
                    })
            except ValueError:
                pass

    return {
        "generated_at": datetime.now().isoformat(),
        "total_assets": total,
        "by_status": by_status,
        "by_category": by_category,
        "by_location": by_location,
        "warranty_expiring_soon": sorted(warranty_expiring, key=lambda x: x["days_remaining"])
    }


def export_report(report: dict, fmt: str = "txt") -> Path:
    """Export a summary report to file."""
    ensure_dirs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if fmt == "json":
        path = REPORTS_DIR / f"asset_report_{timestamp}.json"
        with open(path, "w") as f:
            json.dump(report, f, indent=2)

    else:  # plain text
        path = REPORTS_DIR / f"asset_report_{timestamp}.txt"
        lines = [
            "=" * 60,
            "  ICT ASSET INVENTORY REPORT",
            f"  Generated: {report['generated_at']}",
            "=" * 60,
            f"\n  Total Assets: {report['total_assets']}",
            "\n── By Status ──────────────────────────────────────────────",
        ]
        for k, v in report["by_status"].items():
            lines.append(f"  {k:<20} {v}")

        lines.append("\n── By Category ────────────────────────────────────────────")
        for k, v in report["by_category"].items():
            lines.append(f"  {k:<20} {v}")

        lines.append("\n── By Location ────────────────────────────────────────────")
        for k, v in report["by_location"].items():
            lines.append(f"  {k:<20} {v}")

        if report["warranty_expiring_soon"]:
            lines.append("\n── Warranty Expiring Within 90 Days ───────────────────────")
            for item in report["warranty_expiring_soon"]:
                lines.append(
                    f"  {item['asset_id']}  {item['name']:<25} "
                    f"Expires: {item['warranty_expiry']}  ({item['days_remaining']} days)"
                )

        lines.append("\n" + "=" * 60)
        with open(path, "w") as f:
            f.write("\n".join(lines))

    return path


# ── Import / Export ───────────────────────────────────────────────────────────

def import_csv(filepath: str) -> tuple[int, list[str]]:
    """
    Import assets from an external CSV file.
    Returns (count_imported, list_of_errors).
    """
    errors = []
    imported = 0
    path = Path(filepath)

    if not path.exists():
        return 0, [f"File not found: {filepath}"]

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # row 1 = header
            if not row.get("name"):
                errors.append(f"Row {i}: missing required field 'name'")
                continue
            cat = row.get("category", "").lower()
            if cat and cat not in VALID_CATEGORIES:
                errors.append(f"Row {i}: unknown category '{cat}' — defaulting to 'other'")
                row["category"] = "other"
            try:
                add_asset(row)
                imported += 1
            except Exception as e:
                errors.append(f"Row {i}: {e}")

    return imported, errors


# ── CLI ───────────────────────────────────────────────────────────────────────

def print_table(assets: list[dict]):
    """Pretty-print a list of assets as a table."""
    if not assets:
        print("  No assets found.")
        return
    cols = ["asset_id", "name", "category", "location", "status", "assigned_to"]
    widths = {c: max(len(c), max((len(a.get(c, "")) for a in assets), default=0)) for c in cols}
    header = "  ".join(c.upper().ljust(widths[c]) for c in cols)
    print("\n" + header)
    print("-" * len(header))
    for a in assets:
        row = "  ".join(a.get(c, "").ljust(widths[c]) for c in cols)
        print(row)
    print(f"\n  {len(assets)} record(s) found.\n")


def cli():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("""
ICT Asset Manager — CLI Usage
──────────────────────────────
  python asset_manager.py list                         List all assets
  python asset_manager.py search <query>               Search by keyword
  python asset_manager.py filter --status <s>          Filter by status
  python asset_manager.py filter --location <l>        Filter by location
  python asset_manager.py filter --category <c>        Filter by category
  python asset_manager.py get <ASSET-ID>               Get single asset detail
  python asset_manager.py add                          Add asset interactively
  python asset_manager.py update <ASSET-ID>            Update asset interactively
  python asset_manager.py delete <ASSET-ID>            Delete an asset
  python asset_manager.py report                       Print summary report
  python asset_manager.py report --export [txt|json]   Export report to file
  python asset_manager.py import <file.csv>            Import assets from CSV
  python asset_manager.py seed                         Load sample data
""")
        return

    cmd = args[0]

    if cmd == "list":
        print_table(load_assets())

    elif cmd == "search":
        query = args[1] if len(args) > 1 else ""
        print_table(search_assets(query=query))

    elif cmd == "filter":
        kwargs = {}
        for flag in ["--status", "--location", "--category"]:
            if flag in args:
                kwargs[flag.lstrip("-")] = args[args.index(flag) + 1]
        print_table(search_assets(**kwargs))

    elif cmd == "get":
        if len(args) < 2:
            print("Usage: asset_manager.py get <ASSET-ID>")
            return
        asset = get_asset(args[1])
        if asset:
            for k, v in asset.items():
                print(f"  {k:<20} {v}")
        else:
            print(f"  Asset '{args[1]}' not found.")

    elif cmd == "add":
        print("\nAdd New Asset (press Enter to skip optional fields)\n")
        data = {}
        data["name"] = input("  Name (required): ").strip()
        if not data["name"]:
            print("  Name is required.")
            return
        data["category"] = input(f"  Category {sorted(VALID_CATEGORIES)}: ").strip().lower()
        data["make"] = input("  Make: ").strip()
        data["model"] = input("  Model: ").strip()
        data["serial_number"] = input("  Serial Number: ").strip()
        data["assigned_to"] = input("  Assigned To: ").strip()
        data["location"] = input("  Location: ").strip()
        data["status"] = input("  Status [active]: ").strip().lower() or "active"
        data["purchase_date"] = input("  Purchase Date (YYYY-MM-DD): ").strip()
        data["warranty_expiry"] = input("  Warranty Expiry (YYYY-MM-DD): ").strip()
        data["ip_address"] = input("  IP Address: ").strip()
        data["notes"] = input("  Notes: ").strip()
        asset = add_asset(data)
        print(f"\n  ✓ Asset added: {asset['asset_id']} — {asset['name']}\n")

    elif cmd == "update":
        if len(args) < 2:
            print("Usage: asset_manager.py update <ASSET-ID>")
            return
        asset = get_asset(args[1])
        if not asset:
            print(f"  Asset '{args[1]}' not found.")
            return
        print(f"\nUpdating {args[1]} — {asset['name']}. Press Enter to keep current value.\n")
        updates = {}
        for field in ["name", "assigned_to", "location", "status", "ip_address",
                      "warranty_expiry", "notes"]:
            val = input(f"  {field} [{asset.get(field, '')}]: ").strip()
            if val:
                updates[field] = val
        if updates:
            update_asset(args[1], updates)
            print(f"\n  ✓ Asset {args[1]} updated.\n")
        else:
            print("  No changes made.")

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: asset_manager.py delete <ASSET-ID>")
            return
        confirm = input(f"  Delete {args[1]}? This cannot be undone. [y/N]: ").strip().lower()
        if confirm == "y":
            if delete_asset(args[1]):
                print(f"  ✓ Asset {args[1]} deleted.")
            else:
                print(f"  Asset '{args[1]}' not found.")

    elif cmd == "report":
        report = summary_report()
        if "--export" in args:
            fmt = args[args.index("--export") + 1] if len(args) > args.index("--export") + 1 else "txt"
            path = export_report(report, fmt)
            print(f"\n  ✓ Report exported to: {path}\n")
        else:
            print(f"\n  Total Assets   : {report['total_assets']}")
            print(f"  Generated      : {report['generated_at']}\n")
            print("  By Status:")
            for k, v in report["by_status"].items():
                print(f"    {k:<20} {v}")
            print("\n  By Location:")
            for k, v in report["by_location"].items():
                print(f"    {k:<20} {v}")
            if report["warranty_expiring_soon"]:
                print("\n  ⚠  Warranty Expiring Soon:")
                for item in report["warranty_expiring_soon"]:
                    print(f"    {item['asset_id']}  {item['name']}  — {item['days_remaining']} days")
            print()

    elif cmd == "import":
        if len(args) < 2:
            print("Usage: asset_manager.py import <file.csv>")
            return
        count, errors = import_csv(args[1])
        print(f"\n  ✓ Imported: {count} assets")
        if errors:
            print(f"  ⚠  {len(errors)} warning(s):")
            for e in errors:
                print(f"    {e}")
        print()

    elif cmd == "seed":
        from scripts.seed_data import seed
        seed()
        print("  ✓ Sample data loaded.\n")

    else:
        print(f"  Unknown command: '{cmd}'. Run with --help for usage.")


if __name__ == "__main__":
    ensure_dirs()
    cli()
