# CivicFlow — Repository Context From Earlier Review

This is a snapshot from an earlier conversation/repository review, not a claim about the current HEAD. Codex must inspect the checked-out branch and confirm every item before relying on it.

## Repository

- GitHub repository previously identified: `Amankum25/null`.
- Frontend: Next.js App Router, React, TypeScript, Tailwind.
- Earlier reviewed deployment: `https://null-alpha-eight.vercel.app/dashboard`.
- Earlier known route tree included Dashboard, New Application, Services, Service Details, My Applications, per-application Workspace/Form/Review/Tracking, Approvals, Assistant, Documents, profile/notifications/settings.

## Previously reviewed frontend locations

- `app/(app)/applications/new/page.tsx` — category-based New Application landing.
- `components/service-catalog.tsx` — service cards/directory and create-application start action.
- `lib/civicflow-store.tsx` — client-side demo store, unique application IDs and localStorage persistence.
- `components/browser-viewer.tsx` — demo browser preview, not a live government portal session.
- `components/page-primitives.tsx` — shared UI primitives.
- `app/globals.css` — legacy global styles/select rules.

These paths may have changed. Re-discover the actual current paths before editing.

## Earlier audit findings to re-check

- The New Application landing was restored to six categories and search; preserve it.
- The service directory used the shared service catalog and started applications through `createApplication`.
- Only the Maharashtra Post-Matric Scholarship was considered currently available in that earlier catalog snapshot. Other sample services had coming-soon or information-only states. Re-check live repository data before display.
- The application store was a local/demo store, not full Core backend persistence.
- The browser viewer explicitly showed a demo preview; browser navigation controls were not all connected to a real session.
- AI assistant responses were demo behaviour rather than a connected LangGraph service.
- Document upload stored metadata and did not itself verify the document.
- The approvals screen needed a review-completeness guard; do not allow an approval to bypass required review checks.

## Instructions for Codex

1. Treat this file as a navigation hint only.
2. Read the live repository to identify actual source of truth.
3. Preserve the existing six-category flow and unique application lifecycle.
4. Clearly label any frontend-only prototype behaviour until real services are integrated.
5. Fix or retain the known safety gaps deliberately; do not silently keep unsafe demo shortcuts.
