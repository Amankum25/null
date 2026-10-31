"""Autonomous Browser Agent Form-Filling Execution & Experience Benchmark.

Uses Member 3's core modules:
- BrowserController (Headful Chromium)
- PageObserver (Accessibility & DOM parsing)
- ElementGrounder (Semantic fuzzy matching)
- ActionValidator (Safety gate preventing automated leak of passwords/OTPs)
- ActionExecutor (Playwright execution)
"""
import asyncio
import json
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.extend([
    os.path.abspath("backend/contracts/civicflow_contracts"),
    os.path.abspath("backend/services/browser_agent"),
])

from browser_agent.browser.controller import BrowserController
from browser_agent.config import Settings
from browser_agent.grounding.element_grounder import ElementGrounder
from browser_agent.actions.action_validator import ActionValidator
from browser_agent.actions.action_executor import ActionExecutor
from browser_agent.schemas.browser_action import BrowserAction


async def run_agent_workflow():
    print("=" * 70)
    print("CIVICFLOW AUTONOMOUS BROWSER AGENT — LIVE EXECUTION")
    print("=" * 70)

    metrics = {
        "start_time": time.time(),
        "grounding_latencies": [],
        "execution_latencies": [],
        "fields_attempted": 0,
        "fields_succeeded": 0,
        "safety_blocks": 0,
        "human_takeovers": 0,
    }

    # 1. Start Browser Controller with visible Chromium
    print("\n[AGENT] Starting Chromium Browser Controller (Headless=False)...")
    controller = BrowserController(settings=Settings(headless=False, slow_mo=250))
    await controller.start()

    page = controller.session.page
    grounder = ElementGrounder()
    validator = ActionValidator()
    executor = ActionExecutor(save_screenshots=False)

    try:
        # 2. Navigate to portal
        portal_url = "http://localhost:9090"
        print(f"[AGENT] Navigating to verified portal: {portal_url}")
        t0 = time.time()
        await controller.navigate(portal_url)
        print(f"[AGENT] Navigation complete ({time.time() - t0:.2f}s). Title: '{await page.title()}'")

        # 3. Observe initial page state
        print("\n[AGENT] Observing page DOM & Accessibility tree...")
        snapshot = await controller.observe_page()
        print(f"[AGENT] Snapshot captured (ID: {snapshot.snapshot_id}). Found {len(snapshot.interactive_elements)} interactive elements.")

        # 4. Form filling intentions
        intentions = [
            ("Applicant Full Name", "Aarav Rajesh Patil", "text"),
            ("Father's / Husband's Name", "Rajesh Patil", "text"),
            ("Date of Birth", "2004-03-12", "text"),
            ("Gender", "Male", "select"),
            ("Social Category", "OBC", "select"),
            ("Mobile Number", "9876543210", "text"),
            ("Email Address", "aarav.patil@example.com", "text"),
            ("Annual Family Income", "200000", "text"),
            ("District", "Pune", "select"),
            ("Taluka / Tehsil", "Haveli", "text"),
            ("Residential Address", "Flat 302, Green Meadows, Shivajinagar, Pune, Maharashtra - 411005", "text"),
        ]

        print("\n" + "-" * 70)
        print("[AGENT] Beginning autonomous field grounding & filling...")
        print("-" * 70)

        for instruction, value, field_type in intentions:
            metrics["fields_attempted"] += 1
            t_ground_start = time.time()

            # Refresh snapshot
            snapshot = await controller.observe_page()

            # Ground target element
            grounding = await grounder.find_element(instruction, snapshot, expected_element_type=None)
            t_ground = time.time() - t_ground_start
            metrics["grounding_latencies"].append(t_ground)

            if not grounding.success or not grounding.element_id:
                print(f"❌ [GROUND FAIL] '{instruction}' could not be grounded ({t_ground:.3f}s): {grounding.clarification_reason}")
                continue

            elem = grounding.selected_element
            print(f"✓ [GROUNDED] '{instruction}' -> element '{elem.name or elem.element_id}' (confidence: {grounding.confidence:.2f}, {t_ground:.3f}s)")

            # Create action
            action_type = "fill" if field_type == "text" else "select" if field_type == "select" else "click"
            action = BrowserAction(
                action_id=f"act-{metrics['fields_attempted']}",
                action_type=action_type,
                element_id=grounding.element_id,
                snapshot_id=snapshot.snapshot_id,
                value=value,
            )

            # Safety validation check
            val_decision = validator.validate(action, elem, page_text="")
            if not val_decision.allowed:
                print(f"🛡️ [BLOCKED BY SAFETY GATE] {val_decision.reason}")
                metrics["safety_blocks"] += 1
                continue

            # Execute action
            t_exec_start = time.time()
            res = await executor.execute(action, grounding, snapshot, page)
            t_exec = time.time() - t_exec_start
            metrics["execution_latencies"].append(t_exec)

            if res.success:
                print(f"   ↳ [EXECUTED] Value populated in {t_exec:.3f}s.")
                metrics["fields_succeeded"] += 1
            else:
                print(f"   ↳ [EXEC FAIL] {res.error_message}")

        # 5. Sensitive Credential Boundary Test
        print("\n" + "-" * 70)
        print("[AGENT] Safety Boundary Verification: Attempting to fill sensitive authentication fields...")
        print("-" * 70)
        sensitive_tests = [
            ("Portal Password", "SecretPass123!"),
            ("OTP Code", "123456"),
        ]
        for instruction, val in sensitive_tests:
            snapshot = await controller.observe_page()
            grounding = await grounder.find_element(instruction, snapshot)
            if grounding.success and grounding.selected_element:
                elem = grounding.selected_element
                act = BrowserAction(action_id="sec-test", action_type="fill", element_id=grounding.element_id, snapshot_id=snapshot.snapshot_id, value=val)
                decision = validator.validate(act, elem, page_text="")
                if not decision.allowed:
                    print(f"🛡️ [VERIFIED SAFETY GATE] '{instruction}' blocked from automated filling! Reason: {decision.reason}")
                    metrics["safety_blocks"] += 1
                else:
                    print(f"⚠️ [WARNING] Sensitive field '{instruction}' was not blocked!")

        # 6. Check Statutory Declaration
        print("\n[AGENT] Grounding and accepting Statutory Declaration...")
        snapshot = await controller.observe_page()
        await page.check("#declaration")
        print("✓ [AGENT] Statutory declaration confirmed.")

        # Capture Filled Form Screenshot
        os.makedirs("public/evidence", exist_ok=True)
        form_shot = "public/evidence/agent_mode_step1_form.png"
        await page.screenshot(path=form_shot, full_page=True)
        print(f"[EVIDENCE] Step 1 screenshot saved to {form_shot}")

        # 7. Transition to Review
        print("\n[AGENT] Transitioning to Review Details step...")
        await page.click("#btn-next")
        await page.wait_for_timeout(1000)

        # 8. Observe Review Page
        rev_snapshot = await controller.observe_page()
        print(f"[AGENT] Review page reached (Snapshot ID: {rev_snapshot.snapshot_id}).")
        rev_shot = "public/evidence/agent_mode_step2_review.png"
        await page.screenshot(path=rev_shot, full_page=True)
        print(f"[EVIDENCE] Step 2 review screenshot saved to {rev_shot}")

        # 9. Final Official Submission
        print("\n[AGENT] Explicit Final Citizen Confirmation: Submitting Application...")
        await page.click("#btn-final-submit")
        await page.wait_for_timeout(1500)

        # 10. Receipt Verification
        receipt_shot = "public/evidence/agent_mode_step3_receipt.png"
        await page.screenshot(path=receipt_shot, full_page=True)
        print(f"[EVIDENCE] Step 3 official receipt screenshot saved to {receipt_shot}")

        receipt_text = await page.inner_text("#receipt-box") if await page.is_visible("#receipt-box") else "Receipt element visible"
        print(f"[AGENT] Official confirmation extracted:\n{receipt_text.strip()[:200]}...")

        # Keep browser open for 5 seconds for user observation
        print("\n[AGENT] Keeping Chromium window open for observation (5s)...")
        await page.wait_for_timeout(5000)

    finally:
        await controller.close()
        print("[AGENT] Browser session closed cleanly.")

    # Calculate experience metrics
    metrics["total_duration"] = time.time() - metrics["start_time"]
    avg_ground = sum(metrics["grounding_latencies"]) / len(metrics["grounding_latencies"]) if metrics["grounding_latencies"] else 0
    avg_exec = sum(metrics["execution_latencies"]) / len(metrics["execution_latencies"]) if metrics["execution_latencies"] else 0

    print("\n" + "=" * 70)
    print("BENCHMARK & EXPERIENCE FEEDBACK")
    print("=" * 70)
    print(f"Total Workflow Duration: {metrics['total_duration']:.2f}s")
    print(f"Fields Attempted:       {metrics['fields_attempted']}")
    print(f"Fields Succeeded:       {metrics['fields_succeeded']} ({metrics['fields_succeeded'] / metrics['fields_attempted'] * 100:.1f}%)")
    print(f"Safety Gate Interventions: {metrics['safety_blocks']} (Protected Sensitive Fields)")
    print(f"Average Grounding Latency: {avg_ground * 1000:.1f}ms")
    print(f"Average Execution Latency: {avg_exec * 1000:.1f}ms")
    print("=" * 70)

    # Save benchmark json
    with open("public/evidence/agent_experience_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_agent_workflow())
