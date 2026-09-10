# Manual tests

Pass/fail checklists for guest-facing and console flows. Canonical JSON suites stay result-free so they remain reusable. Record Pass / Fail / Blocked in the interactive runner (saved in the browser).

## Interactive runner (recommended)

With the app server running:

```bash
npm start
```

Open **[http://localhost:8000/manual-tests.html](http://localhost:8000/manual-tests.html)**.

- Pick a suite from the left nav
- Click **✓** (pass), **✗** (fail), or **◌** (blocked) on each step — click again to clear
- Notes autosave in this browser (`localStorage`)
- Download JSON for a suite if you want a run artifact

Canonical suite `.json` files are not modified.

## Setup

```bash
npm run seed
npm start
```

Default server: `http://localhost:8000`

| Page | URL |
|------|-----|
| Manual test runner | http://localhost:8000/manual-tests.html |
| Map | http://localhost:8000/map.html |
| Itinerary | http://localhost:8000/itinerary.html |
| Console | http://localhost:8000/console-operations.html |

Useful resets:

```bash
npm run clear:itinerary
npm run clear:itinerary-config
```

## Conventions

- One suite file = one focused scenario (~8–12 steps). See [`_template.json`](_template.json).
- Suite fields: `id`, `title`, `preconditions`, `dateUnderTest`, `cleanup`, and `steps[]` with `number`, `name`, `do`, `expect`.
- Results and notes are recorded in the runner, not in suite files.
- **Map** and **itinerary** suites are self-contained (seed + UI date/toggles). Do not use console to set up state.
- **Console** suites must verify map and/or itinerary on the same date **D**, then clean up.
- If seed cannot produce a state, mark **Blocked** and point to the matching `CON-*` suite.

## Suite index

### Map (`map/`)

| ID | File | Focus |
|----|------|-------|
| MAP-01 | [map/MAP-01-baseline-load-and-chrome.json](map/MAP-01-baseline-load-and-chrome.json) | Load, Explore, nav, pan/zoom, labels |
| MAP-02 | [map/MAP-02-date-presets.json](map/MAP-02-date-presets.json) | Summer / Winter / Specific Map |
| MAP-03 | [map/MAP-03-type-filters-and-search.json](map/MAP-03-type-filters-and-search.json) | Type filter + animal search |
| MAP-04 | [map/MAP-04-markers-likelihood-stacks.json](map/MAP-04-markers-likelihood-stacks.json) | Likelihood tints, stacks, carousel |
| MAP-05 | [map/MAP-05-tooltips-and-species-overlay.json](map/MAP-05-tooltips-and-species-overlay.json) | Tooltips + More Info overlay |
| MAP-06 | [map/MAP-06-off-display-and-closed-toggles.json](map/MAP-06-off-display-and-closed-toggles.json) | Include off-display / closed toggles |
| MAP-07 | [map/MAP-07-zoomobile-routes.json](map/MAP-07-zoomobile-routes.json) | Zoomobile route radios |
| MAP-08 | [map/MAP-08-closed-exhibits-updates-events.json](map/MAP-08-closed-exhibits-updates-events.json) | Updates, Events, closed exhibits |
| MAP-09 | [map/MAP-09-deep-link-focus.json](map/MAP-09-deep-link-focus.json) | `?focus=` deep link |
| MAP-10 | [map/MAP-10-narrow-layout-smoke.json](map/MAP-10-narrow-layout-smoke.json) | ~720px layout smoke |

### Itinerary (`itinerary/`)

| ID | File | Focus |
|----|------|-------|
| ITIN-01 | [itinerary/ITIN-01-wizard-happy-path.json](itinerary/ITIN-01-wizard-happy-path.json) | Full wizard Finish |
| ITIN-02 | [itinerary/ITIN-02-empty-finish-and-clear.json](itinerary/ITIN-02-empty-finish-and-clear.json) | Empty finish + Clear |
| ITIN-03 | [itinerary/ITIN-03-arrival-departure-early-admission.json](itinerary/ITIN-03-arrival-departure-early-admission.json) | Times + Early Admission |
| ITIN-04 | [itinerary/ITIN-04-schedule-module.json](itinerary/ITIN-04-schedule-module.json) | Schedule module + pills |
| ITIN-05 | [itinerary/ITIN-05-rebuild-and-unschedule-all.json](itinerary/ITIN-05-rebuild-and-unschedule-all.json) | Rebuild / Unschedule all |
| ITIN-06 | [itinerary/ITIN-06-off-display-low-likelihood-confirm.json](itinerary/ITIN-06-off-display-low-likelihood-confirm.json) | Off-display / low likelihood confirm |
| ITIN-07 | [itinerary/ITIN-07-talk-and-encounter-scheduling.json](itinerary/ITIN-07-talk-and-encounter-scheduling.json) | Talks + wild encounters |
| ITIN-08 | [itinerary/ITIN-08-conflict-and-overlap-flows.json](itinerary/ITIN-08-conflict-and-overlap-flows.json) | Conflicts / overlaps |
| ITIN-09 | [itinerary/ITIN-09-attraction-hours-and-transport-prompts.json](itinerary/ITIN-09-attraction-hours-and-transport-prompts.json) | Hours snap + transport prompts |
| ITIN-10 | [itinerary/ITIN-10-bulk-schedule-pressure.json](itinerary/ITIN-10-bulk-schedule-pressure.json) | Short day bulk schedule |
| ITIN-11 | [itinerary/ITIN-11-draft-and-past-date-recovery.json](itinerary/ITIN-11-draft-and-past-date-recovery.json) | Draft + past-date recovery |
| ITIN-12 | [itinerary/ITIN-12-map-path-smoke.json](itinerary/ITIN-12-map-path-smoke.json) | Walk path on itinerary map |

### Console (`console/`)

| ID | File | Focus |
|----|------|-------|
| CON-01 | [console/CON-01-animal-off-on-display.json](console/CON-01-animal-off-on-display.json) | Off/on display + map/itinerary |
| CON-02 | [console/CON-02-visibility-schedule.json](console/CON-02-visibility-schedule.json) | Limited viewing schedule |
| CON-03 | [console/CON-03-animal-viewing-alert.json](console/CON-03-animal-viewing-alert.json) | Viewing alert |
| CON-04 | [console/CON-04-exhibit-closed-open.json](console/CON-04-exhibit-closed-open.json) | Exhibit closed/open |
| CON-05 | [console/CON-05-restaurant-closed-override-schedule.json](console/CON-05-restaurant-closed-override-schedule.json) | Restaurant ops |
| CON-06 | [console/CON-06-restroom-closed-open-alert.json](console/CON-06-restroom-closed-open-alert.json) | Restroom ops |
| CON-07 | [console/CON-07-gift-shop-closed-override-schedule.json](console/CON-07-gift-shop-closed-override-schedule.json) | Gift shop ops |
| CON-08 | [console/CON-08-attraction-closed-override-schedule-hours.json](console/CON-08-attraction-closed-override-schedule-hours.json) | Attraction ops + hours |
| CON-09 | [console/CON-09-transportation-station-and-route.json](console/CON-09-transportation-station-and-route.json) | Stations + route |
| CON-10 | [console/CON-10-guardians-talks.json](console/CON-10-guardians-talks.json) | Guardians talk schedules |
| CON-11 | [console/CON-11-wild-encounters.json](console/CON-11-wild-encounters.json) | Wild encounter schedules |
| CON-12 | [console/CON-12-drinking-fountains.json](console/CON-12-drinking-fountains.json) | Drinking fountains |
| CON-13 | [console/CON-13-updates-crud.json](console/CON-13-updates-crud.json) | Updates CRUD |
| CON-14 | [console/CON-14-create-event.json](console/CON-14-create-event.json) | Create event |
| CON-15 | [console/CON-15-console-validation-matrix.json](console/CON-15-console-validation-matrix.json) | Validation errors |

## Recommended run order

MAP-01 → MAP-10, then ITIN-01 → ITIN-12, then CON-01 → CON-15.
