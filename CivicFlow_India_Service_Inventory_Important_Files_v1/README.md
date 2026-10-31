# CivicFlow India Service Discovery Inventory — v1

**Research snapshot:** 31 October 2026  
**Scope:** State/UT portal discovery, common service taxonomy, national gateways and a starter service matrix.  
**Purpose:** Seed CivicFlow Explore Services and guide Member 1 (catalog), Member 2 (AI discovery) and Member 3 (browser worker).

## What this inventory is — and is not

This is a **national portal and service-discovery starter inventory**, not a claim that every service in India has been exhaustively enumerated or is currently available online. India's official National Government Services Portal shows 18 top-level categories and 14,546 service-information entries. ServicePlus separately reports 36 State/UTs onboarded and 4,835 services launched on that platform. Those counts have different scope and should not be added together or presented as the number of all applications that CivicFlow can automate.

The 36 jurisdiction records cover the 28 States and 8 Union Territories. Each row names a primary citizen-service discovery gateway plus relevant specialist links where identified. Some services are routed to separate department sites, state SSO, CSC/kiosk or offline counters. A portal homepage alone does not prove that any particular service is available online.

## Files

- `state_ut_portals.json` — 36 State/UT entry points, sample services, department facets, specialist portals and validation notes.
- `service_categories.json` — CivicFlow taxonomy and common service names.
- `national_portals.json` — national portals useful across states.
- `national_service_seed_matrix.csv` — 25 common service concepts × 36 jurisdictions = 900 candidate rows. Every row is deliberately marked `candidate_not_yet_verified`; do not import as confirmed service availability.
- `service_entity_schema.json` — suggested service data model and policy rules.
- `source_register.json` — main official sources and what each supports.

## Recommended Explore Services filters

1. State / Union Territory
2. District → Tehsil / Taluka / Block / Circle (where required)
3. Department (filtered by state)
4. Category
5. Service name / alias / local-language keyword
6. Application channel: online, CSC/kiosk, offline, hybrid
7. Government availability: available, temporarily unavailable, offline-only, unknown
8. CivicFlow support: directory-only, external link, browser-stream candidate, browser-stream tested, native integration
9. Document checklist verification: official checklist confirmed / missing / last verified date
10. Popular / recently verified / recently added

## High-value first-wave categories

- Caste/community, income, domicile/residence/nativity, EWS, NCL and other revenue certificates
- Birth, death and marriage registration
- Ration card and food security
- Land records, mutation, property registration and encumbrance
- Old-age, widow, disability and other pensions
- Scholarships and fee reimbursement
- Labour cards, eShram, employment exchange and worker welfare
- Driving licence, vehicle registration, permits and eChallan
- Trade, shop, factory, building, fire and pollution licences
- Electricity, water, property tax and municipal services
- Agriculture, farmer registration and PM-KISAN
- Passport, police clearance, voter registration and ILP
- RTI, state service-delivery appeals and grievances

## Key verified examples

### Bihar RTPS

Official portal: https://serviceonline.bihar.gov.in/  
The public catalogue explicitly lists Residential, Caste and Income certificates at Circle, Sub-Division and District levels; it also lists State/Central NCL and EWS income-and-asset certificates. Birth/death services route to CRS; other portal entries route to separate labour, ration, land, registration, transport and utility sites. The catalogued service's three issuing-level links are dynamic/shortened links on the official portal. For production, let Member 2 discover the level and Member 3 open the official live route; don't hardcode a guessed short-link.  
**Documents:** this inventory does NOT guess a document checklist for Bihar caste certificate. Extract the official checklist from the chosen service-level form/detail page and retain its source URL and date.

### Maharashtra Aaple Sarkar

Official portal: https://aaplesarkar.mahaonline.gov.in/en/CommonForm/CitizenServices_RTS  
The official page shows Income, Domicile, Temporary Residence, Senior Citizen, Non-Creamy Layer and Caste entries, plus Birth, Death and Marriage under RDPR. Its notified-services table distinguishes services available online in Aaple Sarkar from those merely notified under the RTS Act: for example, the page marks Caste Certificate as “No” for availability in Aaple Sarkar, despite listing a 21-day timeline. This is why CivicFlow must store `government_service_exists` separately from `portal_submission_mode` and `civicflow_integration_mode`.

### Tamil Nadu e-Sevai

Official portal: https://www.tnesevai.tn.gov.in/  
The official TNeGA page lists Community, Nativity, Income, First Graduate, Widow, Legal Heir, OBC, Residence, Small/Marginal Farmer and Solvency certificates. It explains that many e-Sevai services are delivered through CSCs. Do not label these as direct self-service online without checking the particular service.

### Manipur eDistrict

Official portal: https://eservicesmanipur.gov.in/eda/our_service.xhtml  
The public list includes Permanent Resident, Domicile, Income, OBC, SC/ST, Land Valuation, Land Ownership, Birth, Death, RTI, Grievance, Employment Exchange and social-welfare pension services.

## How Member 1 should seed the catalog

- Import `state_ut_portals.json` as `jurisdictions` and `national_portals.json` as shared directory sources.
- Use `service_categories.json` for `service_categories`.
- Treat the CSV as **candidate discovery tasks**, not active service records. Confirm each candidate against an official service page or notification before changing its status.
- Create one service variant per jurisdiction and, where applicable, issuing level (e.g. Bihar caste certificate at Circle vs Sub-Division vs District).
- Store a deep link to the exact service detail/application page. Keep a separate portal home URL as fallback.
- Store documents, eligibility, fees, SLA, issuing authority and application channel only with official evidence URLs and `last_verified_at` timestamps.

## How Member 2 should use it

- Use the inventory as search seed and alias dictionary, not as unquestioned truth.
- Resolve user intent + State/UT + district + category + issuing tier.
- Search the official state portal and service details. Return citations, direct URL, allowed portal domains, known application mode, document evidence, missing information and confidence.
- If sources conflict or are not found, return `needs_manual_verification`, not a fabricated service/checklist.

## How Member 3 should use it

- Only open `official_service_url` after Core approves the portal and domain allow-list.
- Validate the final URL and every redirect against approved domains.
- Try same-app iframe only when the government site allows it. Many sites may block framing; use a remote Playwright browser stream in CivicFlow workspace instead. Do not defeat `X-Frame-Options` or CSP with an insecure proxy.
- User enters password, OTP, CAPTCHA, payment and eSign secrets directly in the visible portal. Never send them to Member 2 or retain them in prompts/logs.
- Require citizen review and explicit confirmation for submit/payment. Keep a verified receipt/reference or mark status uncertain.

## Critical fields to display on every service card

- Service name / aliases
- State/UT, district scope and department
- Official service URL + portal home URL
- Government service status
- Actual application channel (online/CSC/offline/hybrid)
- Document checklist status (officially verified / not yet verified)
- CivicFlow capability badge (directory-only / browser-tested / native)
- Last checked date and official source

## Known limitations / validation queue

- Some portals are blocked to automated browsing or show maintenance/login-only screens. Their URL is identified but must be manually verified.
- State portals often publish a service list without a stable deep link; the user may need to select a district, issuing authority level or login first.
- Documents vary by State, district, caste/community, applicant age, previous certificates, purpose, issuing authority and service-level rules. Never show a single national document list for caste/income/domicile.
- Some online portals only accept applications through an authorised CSC/kiosk or service centre.
- Third-party and unofficial websites are intentionally excluded from the official portal directory.
- Every URL should be rechecked by an automated health monitor and a human owner before being marked verified in production.

## Official reference sources

- National Government Services Portal: https://services.india.gov.in/
- ServicePlus: https://serviceonline.gov.in/
- National eGovernance / NeSDA state-portal context: https://negd.gov.in/isl/Directory/statedata/487
- PIB / NeSDA state service delivery update (31 Jan 2026 data): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2229287&lang=1&reg=3
- NFSA state ration portal directory: https://nfsa.gov.in/portal/Ration_Card_State_Portals
- DILRMP State/UT RoR directory: https://dilrmp.gov.in/dilrmpold/State-RoR-Web
- NGDRS state/UT registration links: https://ngdrs.gov.in/NGDRS_Website/state_ut_links.php
- UMANG: https://web.umang.gov.in/
- DigiLocker: https://www.digilocker.gov.in/
- National Scholarship Portal: https://scholarships.gov.in/
- Parivahan: https://parivahan.gov.in/
- UIDAI My Aadhaar: https://uidai.gov.in/en/my-aadhaar
- Passport Seva: https://www.passportindia.gov.in/
- Voters' Services: https://voters.eci.gov.in/
- PM-KISAN: https://pmkisan.gov.in/
- eShram: https://eshram.gov.in/
- EPFO: https://unifiedportal-mem.epfindia.gov.in/
- CPGRAMS: https://pgportal.gov.in/
- RTI Online (Central Authorities only): https://rtionline.gov.in/
- NSWS (business approvals): https://www.nsws.gov.in/
