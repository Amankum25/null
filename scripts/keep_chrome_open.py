"""Keeps a live visible Chrome browser open on the user desktop."""
import asyncio
import os
import sys

sys.path.extend([
    os.path.abspath("backend/contracts/civicflow_contracts"),
    os.path.abspath("backend/services/browser_agent"),
])

from playwright.async_api import async_playwright


async def main():
    print("[CHROME] Launching visible Chrome browser on desktop...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = await browser.new_context(viewport=None)

        print("[CHROME] Opening Tab 1: CivicFlow Home (http://localhost:3000)...")
        page1 = await context.new_page()
        await page1.goto("http://localhost:3000", wait_until="domcontentloaded")

        print("[CHROME] Opening Tab 2: Application Workspace (http://localhost:3000/applications/app-mvwn5q0p-o0pgpf/workspace)...")
        page2 = await context.new_page()
        await page2.goto("http://localhost:3000/applications/app-mvwn5q0p-o0pgpf/workspace", wait_until="domcontentloaded")

        print("[CHROME] Chrome is open on your desktop and will remain active.")

        # Keep running continuously in background
        while True:
            await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

