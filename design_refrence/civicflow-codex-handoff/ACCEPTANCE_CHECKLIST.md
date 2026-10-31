# CivicFlow — Redesign Acceptance Checklist

## 1. Visual system
- [ ] Uses approved Indian Civic Identity dashboard reference.
- [ ] Deep teal/green sidebar, warm ivory canvas, green primary action, restrained saffron accent.
- [ ] Temple, Indian flag and tricolour hero matches approved reference (or approved repo asset).
- [ ] Manrope/Inter typography or equivalent available project fonts; body at least 14–16px.
- [ ] Cards, borders, corners, shadows and spacing are consistent.
- [ ] No return to old blue/pastel style unless explicitly requested.

## 2. Navigation
- [ ] Desktop sidebar visibly shows all nine labels continuously.
- [ ] Sidebar active item follows current route.
- [ ] New Application top dropdown lists all six categories.
- [ ] Explore Services top dropdown lists all six discovery views.
- [ ] Both dropdowns open on click/tap and support keyboard/outside click/Escape.
- [ ] No dead navigation controls.
- [ ] Responsive menu preserves access to all destinations.

## 3. New Application
- [ ] `/applications/new` initial view shows six category cards and search.
- [ ] Category selection prefilters `/services?category=...`.
- [ ] Other Services offers custom application discovery.

## 4. Explore Services
- [ ] Search works across service name, alias, department and keyword.
- [ ] State picker updates URL and results.
- [ ] Department filter changes with state/jurisdiction.
- [ ] Category filters work.
- [ ] Integration mode is distinct from official service availability.
- [ ] Popular/Recently Added only shown when data supports them.
- [ ] Clear filters returns expected state.
- [ ] No-results state offers custom application.
- [ ] Official claims have source metadata.

## 5. Custom service journey
- [ ] Citizen can describe any government service in natural language.
- [ ] Missing state/jurisdiction is requested before state-specific lookup.
- [ ] AI response returns structured candidates and source references.
- [ ] Ambiguous matches are shown for citizen selection.
- [ ] Unverified websites are not called official.
- [ ] Citizen can create a custom application session from a selected match.
- [ ] Custom application has unique ID and independent state.
- [ ] Fallback path exists for manual/guided completion when automation is unsupported.
- [ ] Custom service is not implemented as only a suggestion ticket.

## 6. Workspace / browser
- [ ] Desktop shows application progress/context, embedded browser and AI companion.
- [ ] Browser viewport is real only when connected to Browser Agent; otherwise explicitly demo/unavailable.
- [ ] Browser origin/portal identity is clear.
- [ ] Controls are implemented or visibly disabled with reason.
- [ ] Take Control, Pause AI, Resume AI and Stop Session work correctly.
- [ ] Field mappings use current grounded elements.
- [ ] Stale element handles are rejected and re-inspected.
- [ ] Citizen can edit/reject AI suggestions.
- [ ] Final submit/payment/declaration requires explicit current consent.
- [ ] Ambiguous submission becomes `submission_unconfirmed`, not submitted.

## 7. Existing application flow
- [ ] Each application has a distinct ID.
- [ ] Form, documents, review, approval and tracking state are per application.
- [ ] Review checklist blocks progression until all required items are complete.
- [ ] Unchecking required item revokes readiness.
- [ ] Approval cannot bypass review and consent.
- [ ] Tracking distinguishes official vs demo/self-reported status.
- [ ] Upload does not automatically mean verified.

## 8. Security and trust
- [ ] Passwords, OTPs, CAPTCHA answers, cookies and auth tokens never enter AI prompts/state/logs.
- [ ] CAPTCHA/MFA are never bypassed.
- [ ] Browser navigation restricted to verified/approved origins and safe redirects.
- [ ] Sensitive values are masked/redacted in screenshots/events/logs.
- [ ] User explicitly approves consequential actions.
- [ ] Official service claims cite/retain source and verification data.

## 9. Team integration
- [ ] Core, AI and Browser can run independently.
- [ ] Shared contracts are versioned.
- [ ] Core has mock AI and Browser adapters.
- [ ] Member 2 does not import Playwright or write Core DB.
- [ ] Member 3 does not import LangGraph or write Core DB.
- [ ] Correlation IDs and idempotency are used.
- [ ] Contract tests pass.

## 10. Quality
- [ ] All listed routes have been updated, not only Dashboard.
- [ ] Mobile/tablet layouts usable.
- [ ] Keyboard-only navigation works for menus and primary flows.
- [ ] No broken links, inert controls or console errors.
- [ ] Lint passes (if configured).
- [ ] Typecheck passes.
- [ ] Automated tests pass (if configured).
- [ ] Production build passes.
- [ ] Final report accurately distinguishes implemented vs mocked features.
