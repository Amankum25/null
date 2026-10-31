# Inventory ingestion

Run `python backend/scripts/ingest_inventory.py` to validate the supplied
inventory. It reports the 36 jurisdiction gateways, national portals and 900
candidate service rows. Candidate rows remain staging-only until an exact
official service URL, source evidence and verification date are recorded.
