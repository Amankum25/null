"""Open Chrome with DevTools and perform live DOM/Accessibility inspection."""
import asyncio
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.extend([
    os.path.abspath("backend/contracts/civicflow_contracts"),
    os.path.abspath("backend/services/browser_agent"),
])

from playwright.async_api import async_playwright
from browser_agent.observation.page_observer import PageObserver


async def main():
    print("=" * 70)
    print("OPENING CHROME WITH DEVTOOLS & LIVE INSPECTOR")
    print("=" * 70)

    async with async_playwright() as p:
        print("[LAUNCH] Launching Chromium with Chrome DevTools dock enabled...")
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--auto-open-devtools-for-tabs"]
        )
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        portal_url = "http://localhost:9090"
        print(f"[NAVIGATE] Navigating to: {portal_url}")
        await page.goto(portal_url, wait_until="networkidle")

        title = await page.title()
        print(f"[PAGE LOADED] Title: '{title}'")

        # Perform comprehensive element inspection
        observer = PageObserver()
        print("\n[INSPECT] Extracting Accessibility Tree and DOM Snapshot...")
        snapshot = await observer.observe(page)

        print("\n" + "=" * 70)
        print(f"INSPECTION RESULTS: {len(snapshot.interactive_elements)} Interactive Controls Detected")
        print("=" * 70)
        print(f"{'#':<3} | {'Type':<12} | {'Name / ID':<20} | {'Label / Description':<32} | {'Required':<8}")
        print("-" * 80)

        for idx, elem in enumerate(snapshot.interactive_elements, 1):
            label = (elem.label or elem.aria_label or elem.placeholder or elem.text or "No label")[:30]
            name = (elem.name or elem.element_id or "unnamed")[:18]
            req_str = "YES" if elem.required else "No"
            print(f"{idx:<3} | {elem.element_type:<12} | {name:<20} | {label:<32} | {req_str:<8}")

        # Visually highlight inspected elements on the live Chrome page
        print("\n[HIGHLIGHT] Adding visual inspection badges to elements in Chrome...")
        await page.evaluate("""() => {
            const elements = document.querySelectorAll("input, select, textarea, button, a");
            elements.forEach((el, i) => {
                el.style.outline = "2px solid #08785e";
                el.style.backgroundColor = "rgba(8, 120, 94, 0.05)";
                el.setAttribute("data-civicflow-inspected", "true");
            });
        }""")

        # Take screenshot of inspected elements
        os.makedirs("public/evidence", exist_ok=True)
        inspect_shot = "public/evidence/live_chrome_inspection.png"
        await page.screenshot(path=inspect_shot, full_page=True)
        print(f"[EVIDENCE] Saved screenshot with inspection badges: {inspect_shot}")

        print("\n" + "=" * 70)
        print("CHROME DEVTOOLS IS OPEN ON YOUR SCREEN.")
        print("You can interact with the page, inspect elements in the Elements tab,")
        print("or run commands in the Console.")
        print("Browser will remain open for 45 seconds for your inspection...")
        print("=" * 70)

        await page.wait_for_timeout(45000)
        await browser.close()
        print("\n[CLOSED] Inspection session ended.")


if __name__ == "__main__":
    asyncio.run(main())
