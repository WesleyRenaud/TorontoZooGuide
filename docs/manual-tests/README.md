# Manual tests

Pass/fail checklists for guest-facing and console flows. Edit suite **content** in `.json`. Open the **single runner** HTML once, then pick suites from the left nav.

## Run suites

Do **not** use GitHub/Cursor’s code view for the runner — that only shows raw HTML. Open it in a real browser.

1. Seed and start the app under test (`npm run seed`, `npm start`) when needed.
2. Open **one** file in your browser:
   - Terminal: `open docs/manual-tests/index.html`
   - Or Finder / Cursor: open [`index.html`](index.html) with **Open in Default Browser**
3. Use the left nav to switch suites (MAP / ITIN / CON). You do not open a separate file per suite.
4. On each step: **✓** pass, **✗** fail, **◌** blocked (click again to clear). Notes autosave in that browser (`localStorage`).
5. **Clear suite results** or **Download results JSON** as needed.

Results are not written back into suite files.

## Edit suite content

1. Edit the suite `.json` (see [`_template.json`](_template.json)).
2. Regenerate the runner:

```bash
npm run manual-tests:build
```

## Setup (app under test)

```bash
npm run seed
npm start
```

Default server: `http://localhost:8000`

| Page | URL |
|------|-----|
| Map | http://localhost:8000/map.html |
| Itinerary | http://localhost:8000/itinerary.html |
| Console | http://localhost:8000/console-operations.html |

Useful resets:

```bash
npm run clear:itinerary
npm run clear:itinerary-config
npm run backdate:itinerary
```

`clear:itinerary-config` clears **Don't show this again** for itinerary confirmations (Short Visit, Early Admission, item-not-on-itinerary, etc.). Reload the itinerary page after running it.

`backdate:itinerary` sets the saved itinerary visit date to yesterday so **ITIN-11** can open **Itinerary Date Has Passed** without waiting overnight (the UI date picker cannot select past days).

## Conventions

- One suite file = one focused scenario (~8–12 steps).
- Suite JSON fields: `id`, `title`, and `steps[]` with `number`, `name`, `do`, `expect`. Optional suite meta (`preconditions`, `cleanup`) may be present and is shown in the hub only when non-empty.
- **Map** and **itinerary** suites are self-contained (seed + UI date/toggles). Do not use console to set up state. Exception: **ITIN-11** uses `npm run backdate:itinerary` because the date picker cannot select past days.
- **Console** suites must verify map and/or itinerary on today (unless a step names another date), then clean up.
- **Set … as closed** (restaurants / gift shops) fails if another opening schedule overlaps the same dates and does not offer Trim/Delete. Use seed amenities with no opening schedules: **Africa Restaurant**, **Zootique**. Attractions: use **Create … closure override** for closed guest checks (every seeded attraction has opening-schedule rows).
- If seed cannot produce a state, mark **Blocked** and point to the matching `CON-*` suite.

## Suite index

Content lives in the `.json` files below. Run them all from [`index.html`](index.html).

### Map (`map/`)

| ID | Edit | Focus |
|----|------|-------|
| MAP-01 | [json](map/MAP-01-baseline-load-and-chrome.json) | Load, Explore, nav, pan/zoom, labels |
| MAP-02 | [json](map/MAP-02-date-presets.json) | Summer / Winter / Specific Map |
| MAP-03 | [json](map/MAP-03-type-filters-and-search.json) | Type filter + animal search |
| MAP-04 | [json](map/MAP-04-markers-likelihood-stacks.json) | Likelihood tints, stacks, carousel |
| MAP-05 | [json](map/MAP-05-tooltips-and-species-overlay.json) | Tooltips + More Info overlay |
| MAP-06 | [json](map/MAP-06-off-display-and-closed-toggles.json) | Include off-display / closed toggles |
| MAP-07 | [json](map/MAP-07-zoomobile-routes.json) | Zoomobile route radios |
| MAP-08 | [json](map/MAP-08-updates-and-events.json) | Updates and Events |
| MAP-09 | [json](map/MAP-09-view-on-map-from-animals.json) | **View on Map** from Animals |

### Itinerary (`itinerary/`)

| ID | Edit | Focus |
|----|------|-------|
| ITIN-01 | [json](itinerary/ITIN-01-wizard-happy-path.json) | Full wizard Finish |
| ITIN-02 | [json](itinerary/ITIN-02-date-only-finish-and-clear.json) | Date-only finish + Clear |
| ITIN-03 | [json](itinerary/ITIN-03-arrival-departure-early-admission.json) | Times + Early Admission |
| ITIN-04 | [json](itinerary/ITIN-04-schedule-module.json) | Schedule module + pills |
| ITIN-05 | [json](itinerary/ITIN-05-rebuild-and-unschedule-all.json) | Rebuild / Unschedule all |
| ITIN-06 | [json](itinerary/ITIN-06-off-display-low-likelihood-confirm.json) | Off-display / low likelihood confirm |
| ITIN-07 | [json](itinerary/ITIN-07-talk-and-encounter-scheduling.json) | Talks + wild encounters auto-schedule |
| ITIN-08 | [json](itinerary/ITIN-08-conflict-and-overlap-flows.json) | Conflicts / overlaps |
| ITIN-09 | [json](itinerary/ITIN-09-attraction-hours-and-transport-prompts.json) | Hours snap + transport prompts |
| ITIN-10 | [json](itinerary/ITIN-10-bulk-schedule-pressure.json) | Short day bulk schedule |
| ITIN-11 | [json](itinerary/ITIN-11-past-date-recovery.json) | Past-date recovery + seasonal **Itinerary Updated** |
| ITIN-12 | [json](itinerary/ITIN-12-map-path-smoke.json) | Walk path on itinerary map |

### Console (`console/`)

| ID | Edit | Focus |
|----|------|-------|
| CON-01 | [json](console/CON-01-animal-off-on-display.json) | Off/on display + map/itinerary |
| CON-02 | [json](console/CON-02-visibility-schedule.json) | Limited viewing schedule |
| CON-03 | [json](console/CON-03-animal-viewing-alert.json) | Viewing alert |
| CON-04 | [json](console/CON-04-exhibit-closed-open.json) | Exhibit closed/open |
| CON-05 | [json](console/CON-05-restaurant-closed-override-schedule.json) | Restaurant ops |
| CON-06 | [json](console/CON-06-restroom-closed-open-alert.json) | Restroom ops |
| CON-07 | [json](console/CON-07-gift-shop-closed-override-schedule.json) | Gift shop ops |
| CON-08 | [json](console/CON-08-attraction-closed-override-schedule-hours.json) | Attraction hours + closure override |
| CON-09 | [json](console/CON-09-transportation-station-and-route.json) | Stations + route |
| CON-10 | [json](console/CON-10-guardians-talks.json) | Guardians talk schedules |
| CON-11 | [json](console/CON-11-wild-encounters.json) | Wild encounter schedules |
| CON-12 | [json](console/CON-12-drinking-fountains.json) | Drinking fountains |
| CON-13 | [json](console/CON-13-updates-crud.json) | Updates CRUD |
| CON-14 | [json](console/CON-14-create-event.json) | Create event |
| CON-15 | [json](console/CON-15-console-validation-matrix.json) | Validation errors |

## Recommended run order

MAP-01 → MAP-09, then ITIN-01 → ITIN-12, then CON-01 → CON-15.
