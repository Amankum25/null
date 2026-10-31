"""Validate the CivicFlow India inventory and emit a staging manifest.

The CSV is deliberately kept as candidate discovery data. This command never
promotes candidates to confirmed services.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).parents[2] / "CivicFlow_India_Service_Inventory_Important_Files_v1"

def main() -> None:
    jurisdictions = json.loads((ROOT / "state_ut_portals.json").read_text(encoding="utf-8"))
    national = json.loads((ROOT / "national_portals.json").read_text(encoding="utf-8"))
    with (ROOT / "national_service_seed_matrix.csv").open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    assert all(row["catalog_status"] == "candidate_not_yet_verified" for row in candidates)
    report = {
        "jurisdictions": len(jurisdictions),
        "national_portals": len(national),
        "candidate_rows": len(candidates),
        "confirmed_services": 0,
        "status": "staging_only",
        "category_ids": sorted({row["category_id"] for row in candidates}),
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
