# Changelog

## Release 1.1

Release 1.1 covers the git history from `8fc78b6 Merge pull request #30 from WesleyRenaud/release/1.0` through `256e675 Merge pull request #50 from WesleyRenaud/improvement/make-updates-collapsable`.

### Guest-facing map updates

- Added an `Updates` module to the Explore panel for date-based guest notices such as closures, new arrivals, departures, animal births, and animal passings.
- Made the Updates module collapsible, with carousel arrows for browsing multiple active updates and additional spacing from search results.
- Added new map data types for drinking fountains, defibrillators, emergency intercoms, guest services, picnic sites, and event sites.
- Added guest-service subtypes for wheelchairs, information, the First Aid & Family Center, and rentals/accessibility.
- Added event-site names for Special Events Center, Wildlife Marquee, Conservation Clubhouse, Learning & Engagement Auditorium, and Canopy Classroom.
- Added picnic and event site markers, map legend entries, and search/filter integration.
- Updated the Toronto Zoo map SVG, legend, icon styling, and restroom icon variants.
- Added Eurasia construction map updates, including partial loop closure messaging and Highland cattle marker updates.
- Fixed Zoomobile route display behavior and Wild Encounter map filtering so unavailable or unscheduled items are not shown for the selected date.

### Wild Encounters, data, and content

- Refreshed stale `release/1.0` data so current map services, Wild Encounters, construction impacts, animal notes, and location alerts better match the latest operating context.
- Added new Wild Encounter data and schedule handling.
- Added Wild Encounter images and date-aware schedule filtering.
- Updated animal and location content, including snow leopard, camel, otter, restaurant alert, and Eurasia construction-related information.

### Console operations and update management

- Added console workflows for creating, ending, and editing date-based updates.
- Added support for update types: `Closure`, `New Arrival`, `Departure`, `Animal Birth`, and `Animal Passing`.
- Added update schema migration from the old ID-based table to a title-and-start-date primary key.
- Added console and backend support for new map services and site types.

### Reliability and polish

- Improved map icon asset organization and standardized marker/icon styling.
- Improved Explore menu component sizing and map marker border treatment.
- Added backend and frontend test coverage for new update, map service, event site, and schedule behaviors.

## Release 1.0

Release 1.0 covers the git history from `0f9bf68 Release/0.1 Complete` through `039d6dd Merge pull request #29 from WesleyRenaud/bug-fix/search-not-working`.

### Guest-facing map and search

- Added dynamic availability and likelihood support for attractions, restaurants, gift shops, and Zoomobile routes.
- Added current, summer, and winter Zoomobile route handling with route markers, route overlays, start/end-date management, and current-route selection fixes.
- Added date-aware map search across animals, pavilions, restaurants, restrooms, gift shops, attractions, Meet the Guardians talks, and Wild Encounters.
- Added map filtering controls, closed-item inclusion controls, closed exhibit overlays, status banners, and richer tooltip/banner synchronization.
- Added custom marker sizing for selected attractions and support for manually adjusted marker positions.
- Increased alert banner width behavior, fixed alert icon scaling with large text, and reduced the size of Explore menu controls.
- Fixed a search crash caused by recursive Explore filter include-flag generation.

### Animal visibility, data, and content

- Reworked animal visibility calculations around species-and-exhibit-specific curves.
- Added exhibit likelihood inputs into animal visibility calculations.
- Updated seasonal exhibit statuses, animal temperature thresholds, seasonal temperature formatting, and the impact of actual forecast temperature versus typical temperature.
- Added or updated animal records, images, and guide content, including African spurred tortoise, domestic goat, river otter, pygmy hippo, polar bear, giraffe, highland cattle, red panda, wrinkled hornbill, and Sumatran tiger status/talk data.
- Added and updated visitor alerts for animals, including giraffe viewing schedule details, polar bear construction visibility, highland cattle Zoomobile-only viewing, and Sumatran tiger off-display status.
- Removed obsolete media, screenshots, `.DS_Store` files, and other unused files.

### Itinerary planning

- Added date-aware itinerary validation when a visitor changes their visit date.
- Added dynamic removal reasons for animals, attractions, Meet the Guardians talks, and Wild Encounters.
- Added visibility change feedback for animals, including reduced and improved projected visibility.
- Added update summary popups and alternative-selection entry points after itinerary validation changes.
- Added batch animal selection by region/exhibit, max-date enforcement, past-date prevention, selector close buttons, and improved empty-section/persistence handling.
- Refactored itinerary draft storage, shape normalization, selectors, map behavior, panel rendering, and validation flow.

### Console operations and administrative workflows

- Added console workflows for setting animals off/on display, visibility schedules, viewing alerts, and alert removal.
- Added attraction, exhibit, restaurant, gift shop, restroom, Zoomobile station, Zoomobile route, Meet the Guardians, and Wild Encounter operations forms.
- Added recurring schedule, weekly availability, end-schedule, cancellation, occurrence-filter, status, and date-picker helpers shared across console panels.
- Added restroom closed/open and restroom alert management.
- Fixed the End Guardians Talk Schedule form endpoint.
- Changed setting an animal viewing alert to update the existing alert for the same species and exhibit instead of appending duplicates.

### Architecture, reliability, and test infrastructure

- Refactored frontend modules into clearer API, asset, banner, focus, itinerary, map, marker, overlay, page, search, tooltip, and visit-date modules.
- Refactored console operations registry, controllers, panels, shared form controllers, and option-loading utilities.
- Added per-request database connections and backend method-spacing checks.
- Added JavaScript and Python linting, a default-port server startup path, and a build script that repopulates the database and runs checks.
- Added GitHub Actions continuous integration.
- Added backend unit tests, frontend unit tests, API normalization tests, search/filter tests, itinerary tests, source/layer request tests, seed schema tests, and coverage tooling.
- Added test coverage reporting and CI enforcement for at least 80% frontend and backend coverage.

## Release 0.1

- Established the first release of Toronto Zoo Guide with the interactive map, animals directory, and itinerary builder.
