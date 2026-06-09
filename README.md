# ICT Infrastructure Asset Manager

A command-line Python tool for tracking, auditing, and reporting on ICT assets across distributed enterprise locations.

Built from real-world experience managing 500+ assets across multi-site operations in Zimbabwe, Zambia, and Malawi.

---

## Features

- **Full asset lifecycle tracking** — add, update, decommission, and delete records
- **Multi-site inventory** — filter and report by location, category, or status
- **Warranty expiry alerts** — flags assets expiring within 90 days
- **CSV import** — bulk-onboard assets from existing spreadsheets
- **Report export** — generate inventory summaries as `.txt` or `.json`
- **Python automation-friendly** — clean module API, importable into larger workflows
- **Zero dependencies** — built on the Python standard library only

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/faraidev/ict-asset-manager.git
cd ict-asset-manager

# Load sample data (15 realistic enterprise assets)
python asset_manager.py seed

# List all assets
python asset_manager.py list

# Generate a summary report
python asset_manager.py report

# Export the report
python asset_manager.py report --export json
```

No virtual environment or pip install required.

---

## Usage

```
python asset_manager.py list                          List all assets
python asset_manager.py search <query>                Search by keyword
python asset_manager.py filter --status <s>           Filter by status
python asset_manager.py filter --location <l>         Filter by location
python asset_manager.py filter --category <c>         Filter by category
python asset_manager.py get <ASSET-ID>                View single asset detail
python asset_manager.py add                           Add asset interactively
python asset_manager.py update <ASSET-ID>             Update asset fields
python asset_manager.py delete <ASSET-ID>             Delete an asset
python asset_manager.py report                        Print summary to terminal
python asset_manager.py report --export [txt|json]    Export report to file
python asset_manager.py import <file.csv>             Bulk import from CSV
python asset_manager.py seed                          Load sample data
```

---

## Example Output

```
ASSET_ID   NAME                       CATEGORY   LOCATION   STATUS    ASSIGNED_TO
----------------------------------------------------------------------------------
AST-0001   Core Switch HQ-01          switch     Harare     active    IT Infrastructure
AST-0008   Access Switch LUS-01       switch     Lusaka     active    IT Infrastructure
AST-0015   Laptop — Under Repair      laptop     Harare     maintenance  IT Infrastructure

  By Status:
    active               13
    decommissioned        1
    maintenance           1

  ⚠  Warranty Expiring Soon:
    AST-0012  Laptop — Blantyre Branch Manager  — 11 days
    AST-0015  Laptop — Under Repair             — 31 days
```

---

## Project Structure

```
ict-asset-manager/
├── asset_manager.py          # Core module — CRUD, search, reporting, CLI
├── scripts/
│   └── seed_data.py          # Sample data loader (15 enterprise assets)
├── data/
│   ├── assets.csv            # Live asset store (auto-created)
│   └── samples/
│       └── import_example.csv
├── reports/                  # Exported reports land here
├── tests/
│   └── test_asset_manager.py # Unit tests (pytest)
└── docs/
    └── field_reference.md    # Asset field definitions
```

---

## Asset Fields

| Field | Description |
|---|---|
| `asset_id` | Auto-generated (AST-0001, AST-0002…) |
| `name` | Descriptive name |
| `category` | laptop / desktop / server / switch / router / firewall / access_point / printer / ups / phone / other |
| `make` | Manufacturer |
| `model` | Model name |
| `serial_number` | Hardware serial |
| `assigned_to` | User or team |
| `location` | Site or office |
| `status` | active / inactive / maintenance / decommissioned / missing |
| `purchase_date` | YYYY-MM-DD |
| `warranty_expiry` | YYYY-MM-DD |
| `ip_address` | Management IP (optional) |
| `notes` | Free text |
| `last_updated` | Auto-set on every write |

---

## CSV Import Format

Use `data/samples/import_example.csv` as a template. Required field: `name`. All others optional.

```bash
python asset_manager.py import data/samples/import_example.csv
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Background

This tool was developed to address a real operational need: maintaining accurate, auditable records of ICT assets distributed across multiple international locations, without relying on expensive commercial ITAM platforms.

It replaces manual spreadsheet processes with a structured, scriptable workflow that can be extended into larger automation pipelines.

---

## Tech Stack

- Python 3.10+
- Standard library only (`csv`, `json`, `pathlib`, `datetime`)
- pytest for testing

---

## Author

**Farai Murindagomo** — ICT Infrastructure & Networks Engineer  
[linkedin.com/in/faraimur](https://linkedin.com/in/faraimur) · [github.com/faraidev](https://github.com/faraidev)
