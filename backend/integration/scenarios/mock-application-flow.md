# Mock application flow

Use `mocks/mock_application.json`, `mocks/mock_browser_actions.json`, and `mocks/mock_portal/index.html` to exercise local integration. Serve the portal locally for browser development, and configure an explicit development-only domain allowlist for the local fixture. The browser service's production navigation policy blocks localhost/private network targets, so a test-only policy override must be isolated from normal configuration. Do not point automated submission scenarios at a real government portal.

Expected authority checks: review items must all be complete; the user must approve the specific application; the browser must return verifiable evidence for `submitted`; missing or ambiguous evidence maps to `uncertain`.
