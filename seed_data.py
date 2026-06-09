"""
Seed script — loads realistic sample ICT asset data for demonstration.
Run via: python asset_manager.py seed
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from asset_manager import add_asset, save_assets, DATA_DIR, ASSETS_FILE

SAMPLE_ASSETS = [
    # Harare HQ
    {
        "name": "Core Switch HQ-01",
        "category": "switch",
        "make": "Cisco",
        "model": "Catalyst 9600",
        "serial_number": "FXS2142Q0JK",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2022-03-15",
        "warranty_expiry": "2025-03-15",
        "ip_address": "10.10.1.1",
        "notes": "Core distribution switch, HQ server room"
    },
    {
        "name": "ISR Router HQ-01",
        "category": "router",
        "make": "Cisco",
        "model": "ISR 4331",
        "serial_number": "FXS2201A1BC",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2022-03-15",
        "warranty_expiry": "2025-03-15",
        "ip_address": "10.10.1.254",
        "notes": "WAN edge router"
    },
    {
        "name": "Sophos XG Firewall HQ",
        "category": "firewall",
        "make": "Sophos",
        "model": "XG 310",
        "serial_number": "SFP-310-9921X",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2022-03-15",
        "warranty_expiry": "2026-08-15",
        "ip_address": "10.10.1.253",
        "notes": "Perimeter firewall, HQ"
    },
    {
        "name": "Dell PowerEdge AD Server",
        "category": "server",
        "make": "Dell",
        "model": "PowerEdge R740",
        "serial_number": "DLPE-R740-7741",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2021-06-01",
        "warranty_expiry": "2024-06-01",
        "ip_address": "10.10.2.10",
        "notes": "Primary AD / DNS / DHCP server"
    },
    {
        "name": "Dell PowerEdge File Server",
        "category": "server",
        "make": "Dell",
        "model": "PowerEdge R540",
        "serial_number": "DLPE-R540-3312",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2021-06-01",
        "warranty_expiry": "2024-06-01",
        "ip_address": "10.10.2.11",
        "notes": "File services and shared storage"
    },
    {
        "name": "Laptop — Finance Manager",
        "category": "laptop",
        "make": "Lenovo",
        "model": "ThinkPad L14",
        "serial_number": "LNV-L14-88210",
        "assigned_to": "T. Chikwanda",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2023-01-10",
        "warranty_expiry": "2026-01-10",
        "ip_address": "",
        "notes": "Finance department"
    },
    {
        "name": "Laptop — Operations Director",
        "category": "laptop",
        "make": "HP",
        "model": "EliteBook 840 G9",
        "serial_number": "HPE-840-55432",
        "assigned_to": "B. Moyo",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2023-01-10",
        "warranty_expiry": "2026-01-10",
        "ip_address": "",
        "notes": ""
    },
    # Lusaka Branch
    {
        "name": "Access Switch LUS-01",
        "category": "switch",
        "make": "Cisco",
        "model": "Catalyst 9200",
        "serial_number": "FXS2200B8QQ",
        "assigned_to": "IT Infrastructure",
        "location": "Lusaka",
        "status": "active",
        "purchase_date": "2022-05-20",
        "warranty_expiry": "2025-05-20",
        "ip_address": "10.20.1.1",
        "notes": "Lusaka branch access layer"
    },
    {
        "name": "Sophos XG Firewall Lusaka",
        "category": "firewall",
        "make": "Sophos",
        "model": "XG 135",
        "serial_number": "SFP-135-4410Z",
        "assigned_to": "IT Infrastructure",
        "location": "Lusaka",
        "status": "active",
        "purchase_date": "2022-05-20",
        "warranty_expiry": "2026-09-20",
        "ip_address": "10.20.1.254",
        "notes": "Branch firewall with site-to-site VPN to HQ"
    },
    {
        "name": "Desktop — Lusaka Clerk 01",
        "category": "desktop",
        "make": "HP",
        "model": "ProDesk 400 G7",
        "serial_number": "HPD-400-11223",
        "assigned_to": "C. Banda",
        "location": "Lusaka",
        "status": "active",
        "purchase_date": "2022-07-01",
        "warranty_expiry": "2025-07-01",
        "ip_address": "10.20.5.21",
        "notes": ""
    },
    # Blantyre Branch
    {
        "name": "Access Switch BLT-01",
        "category": "switch",
        "make": "Cisco",
        "model": "Catalyst 9200",
        "serial_number": "FXS2200C9RR",
        "assigned_to": "IT Infrastructure",
        "location": "Blantyre",
        "status": "active",
        "purchase_date": "2022-05-20",
        "warranty_expiry": "2025-05-20",
        "ip_address": "10.30.1.1",
        "notes": "Blantyre branch access layer"
    },
    {
        "name": "Laptop — Blantyre Branch Manager",
        "category": "laptop",
        "make": "Lenovo",
        "model": "ThinkPad E14",
        "serial_number": "LNV-E14-99001",
        "assigned_to": "R. Phiri",
        "location": "Blantyre",
        "status": "active",
        "purchase_date": "2022-08-15",
        "warranty_expiry": "2026-06-20",
        "ip_address": "",
        "notes": ""
    },
    # Maintenance / misc
    {
        "name": "UPS — Server Room HQ",
        "category": "ups",
        "make": "APC",
        "model": "Smart-UPS 3000",
        "serial_number": "APC-3K-77612",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "active",
        "purchase_date": "2021-06-01",
        "warranty_expiry": "2024-06-01",
        "ip_address": "",
        "notes": "Server room power backup"
    },
    {
        "name": "Desktop — Decommissioned",
        "category": "desktop",
        "make": "HP",
        "model": "Compaq Elite 8300",
        "serial_number": "HPD-EL-00011",
        "assigned_to": "",
        "location": "Harare",
        "status": "decommissioned",
        "purchase_date": "2015-01-01",
        "warranty_expiry": "2018-01-01",
        "ip_address": "",
        "notes": "End of life, awaiting disposal"
    },
    {
        "name": "Laptop — Under Repair",
        "category": "laptop",
        "make": "Dell",
        "model": "Latitude 5520",
        "serial_number": "DLL-5520-44501",
        "assigned_to": "IT Infrastructure",
        "location": "Harare",
        "status": "maintenance",
        "purchase_date": "2021-09-01",
        "warranty_expiry": "2026-07-10",
        "ip_address": "",
        "notes": "Screen replacement in progress"
    },
]


def seed():
    # Clear existing data and re-seed
    if DATA_DIR.exists() and ASSETS_FILE.exists():
        ASSETS_FILE.unlink()
    for asset_data in SAMPLE_ASSETS:
        add_asset(asset_data)
    print(f"  Seeded {len(SAMPLE_ASSETS)} sample assets.")


if __name__ == "__main__":
    seed()
