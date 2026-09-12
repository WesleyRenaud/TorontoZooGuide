# Toronto Zoo Guide — Release 1.0

Release cycle notes for the first guest-ready cut of the Toronto Zoo Guide: map explore, animals directory, itinerary builder / day planner, and console operations for live zoo state.

## Scope

- **Map** — date presets (Summer / Winter / Specific Map), type filters, search, likelihood markers, stacks, tooltips, Zoomobile routes, Updates / Events, off-display and closed toggles.
- **Animals** — browse / search and **View on Map**.
- **Itinerary** — wizard (date, animals, attractions, talks, wild encounters, transportation), List / Day Planner, schedule module, rebuild / unschedule, conflict resolution including **Adjust Activity Times?** trim, Zoomobile as attraction vs transportation (including transit rides after rebuild), save / discard dirty builder close, past-date recovery.
- **Console** — off/on display, visibility schedules, viewing alerts, exhibit/amenity open-closed and overrides, attraction hours / closure overrides, transportation stations and routes, guardians talks, wild encounters, drinking fountains, updates CRUD, create event, form validation errors.

## Manual test map

Canonical suites live under [`docs/manual-tests/`](../../manual-tests/). Open the hub at [`docs/manual-tests/index.html`](../../manual-tests/index.html) in a real browser (not GitHub’s HTML preview).

Recommended order: **MAP-01 → MAP-09**, then **ITIN-01 → ITIN-18**, then **CON-01 → CON-15**.

### Map

| ID | Focus |
|----|-------|
| MAP-01 | Load, Explore, nav, pan/zoom |
| MAP-02 | Summer / Winter / Specific Map |
| MAP-03 | Type filters + search |
| MAP-04 | Likelihood, stacks |
| MAP-05 | Tooltips + More Info |
| MAP-06 | Off-display / closed toggles |
| MAP-07 | Zoomobile routes |
| MAP-08 | Updates and Events |
| MAP-09 | View on Map from Animals |

### Itinerary

| ID | Focus |
|----|-------|
| ITIN-01 | Wizard happy path |
| ITIN-02 | Date-only finish + Clear |
| ITIN-03 | Arrival / departure / Early Admission |
| ITIN-04 | Schedule module |
| ITIN-05 | Rebuild / Unschedule all |
| ITIN-06 | Off-display animal confirm |
| ITIN-07 | Talk + encounter auto-schedule |
| ITIN-08 | Same-start conflicts (pick one) |
| ITIN-09 | Attraction hours snap + Zoomobile prompts |
| ITIN-10 | Short-day bulk pressure |
| ITIN-11 | Past-date recovery |
| ITIN-12 | Walk path smoke |
| ITIN-13 | **Adjust Activity Times?** partial trim |
| ITIN-14 | Zoomobile transit rides after rebuild |
| ITIN-15 | **Save Changes?** / **Discard** |
| ITIN-16 | Add overlapping talk → **Update Plan** |
| ITIN-17 | **Add to Itinerary?** from Schedule item |
| ITIN-18 | **Attraction May Be Closed** |

### Console

| ID | Focus |
|----|-------|
| CON-01 … CON-15 | Live ops with map/itinerary verify on today (see [manual-tests README](../../manual-tests/README.md)) |

## Guest walkthrough

See [USER_GUIDE.md](USER_GUIDE.md) for a product-oriented walkthrough of Map, Animals, and Itinerary, plus a short Console appendix for staff.
