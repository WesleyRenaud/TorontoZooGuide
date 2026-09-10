# Manual tests

Pass/fail checklists for guest-facing and console flows. Canonical files keep **Result** blank so they stay reusable; copy a suite or note results in a PR/working copy when running.

## Setup

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
```

## Conventions

- One suite file = one focused scenario (~8–12 steps).
- For each step: **Do**, **Expect**, **Result** (`Pass` / `Fail` / `Blocked`), **Notes**.
- **Map** and **itinerary** suites are self-contained (seed + UI date/toggles). Do not use console to set up state.
- **Console** suites must verify map and/or itinerary on the same date **D**, then clean up.
- If seed cannot produce a state, mark **Blocked** and point to the matching `CON-*` suite.

## Suite index

### Map (`map/`)

| ID | File | Focus |
|----|------|-------|
| MAP-01 | [map/MAP-01-baseline-load-and-chrome.md](map/MAP-01-baseline-load-and-chrome.md) | Load, Explore, nav, pan/zoom, labels |
| MAP-02 | [map/MAP-02-date-presets.md](map/MAP-02-date-presets.md) | Summer / Winter / Specific Map |
| MAP-03 | [map/MAP-03-type-filters-and-search.md](map/MAP-03-type-filters-and-search.md) | Type filter + animal search |
| MAP-04 | [map/MAP-04-markers-likelihood-stacks.md](map/MAP-04-markers-likelihood-stacks.md) | Likelihood tints, stacks, carousel |
| MAP-05 | [map/MAP-05-tooltips-and-species-overlay.md](map/MAP-05-tooltips-and-species-overlay.md) | Tooltips + More Info overlay |
| MAP-06 | [map/MAP-06-off-display-and-closed-toggles.md](map/MAP-06-off-display-and-closed-toggles.md) | Include off-display / closed toggles |
| MAP-07 | [map/MAP-07-zoomobile-routes.md](map/MAP-07-zoomobile-routes.md) | Zoomobile route radios |
| MAP-08 | [map/MAP-08-closed-exhibits-updates-events.md](map/MAP-08-closed-exhibits-updates-events.md) | Updates, Events, closed exhibits |
| MAP-09 | [map/MAP-09-deep-link-focus.md](map/MAP-09-deep-link-focus.md) | `?focus=` deep link |
| MAP-10 | [map/MAP-10-narrow-layout-smoke.md](map/MAP-10-narrow-layout-smoke.md) | ~720px layout smoke |

### Itinerary (`itinerary/`)

| ID | File | Focus |
|----|------|-------|
| ITIN-01 | [itinerary/ITIN-01-wizard-happy-path.md](itinerary/ITIN-01-wizard-happy-path.md) | Full wizard Finish |
| ITIN-02 | [itinerary/ITIN-02-empty-finish-and-clear.md](itinerary/ITIN-02-empty-finish-and-clear.md) | Empty finish + Clear |
| ITIN-03 | [itinerary/ITIN-03-arrival-departure-early-admission.md](itinerary/ITIN-03-arrival-departure-early-admission.md) | Times + Early Admission |
| ITIN-04 | [itinerary/ITIN-04-schedule-module.md](itinerary/ITIN-04-schedule-module.md) | Schedule module + pills |
| ITIN-05 | [itinerary/ITIN-05-rebuild-and-unschedule-all.md](itinerary/ITIN-05-rebuild-and-unschedule-all.md) | Rebuild / Unschedule all |
| ITIN-06 | [itinerary/ITIN-06-off-display-low-likelihood-confirm.md](itinerary/ITIN-06-off-display-low-likelihood-confirm.md) | Off-display / low likelihood confirm |
| ITIN-07 | [itinerary/ITIN-07-talk-and-encounter-scheduling.md](itinerary/ITIN-07-talk-and-encounter-scheduling.md) | Talks + wild encounters |
| ITIN-08 | [itinerary/ITIN-08-conflict-and-overlap-flows.md](itinerary/ITIN-08-conflict-and-overlap-flows.md) | Conflicts / overlaps |
| ITIN-09 | [itinerary/ITIN-09-attraction-hours-and-transport-prompts.md](itinerary/ITIN-09-attraction-hours-and-transport-prompts.md) | Hours snap + transport prompts |
| ITIN-10 | [itinerary/ITIN-10-bulk-schedule-pressure.md](itinerary/ITIN-10-bulk-schedule-pressure.md) | Short day bulk schedule |
| ITIN-11 | [itinerary/ITIN-11-draft-and-past-date-recovery.md](itinerary/ITIN-11-draft-and-past-date-recovery.md) | Draft + past-date recovery |
| ITIN-12 | [itinerary/ITIN-12-map-path-smoke.md](itinerary/ITIN-12-map-path-smoke.md) | Walk path on itinerary map |

### Console (`console/`)

| ID | File | Focus |
|----|------|-------|
| CON-01 | [console/CON-01-animal-off-on-display.md](console/CON-01-animal-off-on-display.md) | Off/on display + map/itinerary |
| CON-02 | [console/CON-02-visibility-schedule.md](console/CON-02-visibility-schedule.md) | Limited viewing schedule |
| CON-03 | [console/CON-03-animal-viewing-alert.md](console/CON-03-animal-viewing-alert.md) | Viewing alert |
| CON-04 | [console/CON-04-exhibit-closed-open.md](console/CON-04-exhibit-closed-open.md) | Exhibit closed/open |
| CON-05 | [console/CON-05-restaurant-closed-override-schedule.md](console/CON-05-restaurant-closed-override-schedule.md) | Restaurant ops |
| CON-06 | [console/CON-06-restroom-closed-open-alert.md](console/CON-06-restroom-closed-open-alert.md) | Restroom ops |
| CON-07 | [console/CON-07-gift-shop-closed-override-schedule.md](console/CON-07-gift-shop-closed-override-schedule.md) | Gift shop ops |
| CON-08 | [console/CON-08-attraction-closed-override-schedule-hours.md](console/CON-08-attraction-closed-override-schedule-hours.md) | Attraction ops + hours |
| CON-09 | [console/CON-09-transportation-station-and-route.md](console/CON-09-transportation-station-and-route.md) | Stations + route |
| CON-10 | [console/CON-10-guardians-talks.md](console/CON-10-guardians-talks.md) | Guardians talk schedules |
| CON-11 | [console/CON-11-wild-encounters.md](console/CON-11-wild-encounters.md) | Wild encounter schedules |
| CON-12 | [console/CON-12-drinking-fountains.md](console/CON-12-drinking-fountains.md) | Drinking fountains |
| CON-13 | [console/CON-13-updates-crud.md](console/CON-13-updates-crud.md) | Updates CRUD |
| CON-14 | [console/CON-14-create-event.md](console/CON-14-create-event.md) | Create event |
| CON-15 | [console/CON-15-console-validation-matrix.md](console/CON-15-console-validation-matrix.md) | Validation errors |

## Recommended run order

MAP-01 → MAP-10, then ITIN-01 → ITIN-12, then CON-01 → CON-15. Finish writing and attempting one suite before starting the next when executing for the first time.
