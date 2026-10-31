# CivicFlow Design System — Indian Civic Identity

## 1. Approved design direction

Use `assets/01-approved-dashboard-reference.png` as the primary visual authority. This is the direction the user explicitly approved.

Visual character: dignified, warm, Indian civic identity with modern SaaS usability. Avoid generic pastel startup illustrations, blue-only SaaS styling, excessive glassmorphism or a traditional dense government-portal look.

### Brand cues to preserve

- Dark teal/green expanded left sidebar.
- Warm cream/ivory app canvas.
- Deep green/teal headings and primary actions.
- Restrained saffron/orange accents for selected highlights and category accents.
- White/ivory cards, subtle warm borders and low-elevation shadows.
- Temple/government-building hero, Indian national flag and tricolour ribbon exactly as represented in the approved dashboard image.
- CivicFlow logo lockup in green/teal. `assets/civicflow-logo.svg` is a clean vector direction and may be refined, but do not replace it with an unrelated logo.

## 2. App shell

### Desktop

- Sidebar: always expanded and visibly labelled, target width 236–244px.
- Sidebar has all nine items continuously visible:
  1. Dashboard
  2. New Application
  3. Explore Services
  4. My Applications
  5. Documents
  6. Approvals
  7. AI Assistant
  8. Notifications
  9. Settings
- Active item: lighter translucent green/teal fill, high-contrast label/icon. Do not use color alone.
- Topbar: global search; New Application dropdown; Explore Services dropdown; notification control; user profile.
- New Application top dropdown contains all six category links.
- Explore Services top dropdown contains All Services, By Category, By Department, By State, Popular Services, Recently Added.
- Keep the main navigation on the left even though New Application and Explore Services also exist in the topbar. This duplication is intentional and approved.
- Main canvas should use the rest of the viewport. Keep a spacious desktop content gutter (24–32px), no excessive max-width that wastes a wide viewport.

### Responsive behaviour

- Desktop/tablet landscape: keep the expanded sidebar whenever practical.
- Narrow mobile: transform the sidebar to a labelled slide-over drawer or compact overlay. Do not silently remove destinations. Keep a visible menu control and accessible labels.
- Top dropdowns open on click/tap and close on outside click, Escape, route navigation and second click. Hover may be an optional desktop enhancement, never the only way to open.
- Dropdown panels should be aligned to their triggers, have clear focus/hover states and not be clipped behind hero cards.

## 3. Design tokens

Use `design-tokens.json` as canonical. Key palette:

| Token | Value | Use |
|---|---|---|
| `brand.deep` | `#064B43` | Sidebar/deep surfaces |
| `brand.green` | `#08785E` | Primary actions, links, active indicators |
| `brand.greenDark` | `#075B4D` | Hover/deeper green |
| `brand.mint` | `#DDF3E7` | Soft green icon tiles |
| `accent.saffron` | `#E9902E` | Saffron accent |
| `accent.gold` | `#E5B35C` | Secondary highlight |
| `canvas` | `#F8F4EB` | Main warm ivory canvas |
| `surface` | `#FFFEFB` | Cards and panels |
| `text.primary` | `#10272B` | Primary copy |
| `text.secondary` | `#60756F` | Secondary copy |
| `border` | `#E9E1D5` | Warm subtle borders |

Typography:
- Preferred heading: Manrope (600–800).
- Preferred body/UI: Inter (400–600).
- Use locally available project fonts if already configured; do not create an unnecessary font dependency.
- Base body size should be at least 14–16px. Essential instructions must never be tiny.

## 4. Dashboard composition

Hero panel:
- Left: welcome, concise promise, one primary start action.
- Right: same temple/flag/tricolour hero artwork.
- Ensure text and actions never overlap the temple/flag artwork.
- Prefer reusing the existing approved hero asset if available in repo. `assets/04-temple-flag-hero-reference.png` is a crop from the approved screenshot for visual matching, not a source original.

Below hero:
- Four concise metric cards: Active Applications, In Review, Documents Pending, Action Required.
- Recent/Your Applications list on left.
- Quick Actions on right: Explore Services, Upload Documents, Ask AI Assistant, Track Application.
- All metrics must be bound to real application state. Do not copy illustrative counts from reference art.

## 5. Shared components

- `AppShell`, `ExpandedSidebar`, `TopBar`, `DropdownMenu`, `GlobalSearch`.
- `PageHeader`, `HeroBanner`, `MetricCard`, `CategoryCard`, `ServiceCard`.
- `FilterPanel`, `StatePicker`, `DepartmentPicker`, `IntegrationStatus`, `StatusPill`.
- `ApplicationRow`, `ApplicationStepper`, `FormSection`, `ReviewChecklist`, `Timeline`.
- `WorkspacePanel`, `BrowserTabBar`, `BrowserToolbar`, `BrowserViewport`, `AIToolbar`, `FieldMappingCard`, `TakeControlBanner`.
- `EmptyState`, `ErrorState`, `TrustNotice`, `ConfirmDialog`, `Skeleton`.

## 6. Visual rules

- Use consistent icon family (prefer existing Lucide package).
- Category icons may use modest individual tints; avoid rainbow UI.
- Status colors must have text labels; color alone is insufficient.
- Use a single clear primary action per decision area.
- Keep corners moderately rounded (12–18px), not pill-shaped everything.
- Use light borders and subtle shadows, not heavy blur/glass overlays.
- Keep forms calm and high-contrast with visible labels and explanatory helper text.
- Desktop service directory should feel structured: category/filter area and result cards, not a giant decorative poster.
- All decorative artwork needs alt behavior (empty alt for decorative images).
