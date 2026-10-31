import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def fill_form():
    print("Launching Chromium browser with Playwright...")
    async with async_playwright() as p:
        # Launch Chrome / Chromium browser visibly
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=250,
            args=["--start-maximized"]
        )
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        print("Navigating to Citizen Portal at http://localhost:9090...")
        await page.goto("http://localhost:9090", wait_until="networkidle")

        print("Page loaded: " + await page.title())

        # Fill citizen profile fields
        print("1. Filling Applicant Name...")
        await page.fill("#applicantName", "Aarav Rajesh Patil")

        print("2. Filling Father's Name...")
        await page.fill("#fatherName", "Rajesh Patil")

        print("3. Filling Date of Birth...")
        await page.fill("#dob", "2004-03-12")

        print("4. Selecting Gender...")
        await page.select_option("#gender", "Male")

        print("5. Selecting Social Category...")
        await page.select_option("#category", "OBC")

        print("6. Filling Mobile Number...")
        await page.fill("#mobile", "9876543210")

        print("7. Filling Email...")
        await page.fill("#email", "aarav.patil@example.com")

        print("8. Filling Annual Family Income...")
        await page.fill("#income", "200000")

        print("9. Selecting District...")
        await page.select_option("#district", "Pune")

        print("10. Filling Taluka...")
        await page.fill("#taluka", "Haveli")

        print("11. Filling Residential Address...")
        await page.fill("#address", "Flat 302, Green Meadows, Shivajinagar, Pune, Maharashtra - 411005")

        print("12. Checking Declaration checkbox...")
        await page.check("#declaration")

        # Capture screenshot of completely filled form
        os.makedirs("public/evidence", exist_ok=True)
        screenshot_path = "public/evidence/step1_filled_form.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Captured screenshot of filled form: {screenshot_path}")

        print("13. Submitting form to Review page...")
        await page.click("#btn-next")
        await page.wait_for_timeout(1500)

        review_screenshot_path = "public/evidence/step2_review_page.png"
        await page.screenshot(path=review_screenshot_path, full_page=True)
        print(f"Captured review page screenshot: {review_screenshot_path}")

        print("14. Confirming Final Official Submission...")
        await page.click("#btn-final-submit")
        await page.wait_for_timeout(2000)

        receipt_screenshot_path = "public/evidence/step3_receipt.png"
        await page.screenshot(path=receipt_screenshot_path, full_page=True)
        print(f"Captured official receipt screenshot: {receipt_screenshot_path}")

        print("Form fill and submission verified! Browser remaining visible for 6 seconds...")
        await page.wait_for_timeout(6000)

        await browser.close()
        print("Completed automated browser form filling successfully!")

if __name__ == "__main__":
    asyncio.run(fill_form())
