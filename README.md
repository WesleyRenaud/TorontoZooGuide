# Toronto Zoo Guide

Version 1.2.0

Toronto Zoo Guide is a customer-facing web app designed to help guests plan and navigate a day at the Toronto Zoo. Version 1.2.0 focuses on four core experiences:

- an interactive map for live exploration of the zoo grounds
- date-based updates for guest-facing notices and closures
- an animals section for browsing exhibits and species details
- an itinerary builder for planning a visit around a specific date

This README covers the guest-facing functionality in those areas. It intentionally does not document internal console or operations tools.

For release history, see [CHANGELOG.md](CHANGELOG.md).

## Version 1.2.0 Highlights

Version 1.2.0 expands the date-aware planning experience.

Highlights include:

- an itinerary day planner that places saved items into a schedule-aware view
- scheduled Meet the Guardians talks and Wild Encounters in itinerary planning
- support for talks with different times on different weekdays
- post-close map and itinerary date behavior based on live zoo hours
- current-day weather handling for animal visibility on the map
- more precise opening schedules and closure overrides for attractions, restaurants, and gift shops

## What the App Helps Visitors Do

Toronto Zoo Guide is built to answer the main questions a guest has before or during a visit:

- What animals, buildings, restaurants, attractions, and events can I find today?
- Where are they on the map?
- Which experiences are available on my visit date?
- Are there current updates, closures, arrivals, or animal notices I should know about?
- Which animals are more likely to be visible on a given day?
- How can I save a shortlist of things I want to see?

The app uses date-aware data so the information shown to the visitor can change depending on the selected visit date.

## Navigation

The app uses a persistent bottom navigation bar so visitors can move between the main customer pages:

- `Map`
- `Animals`
- `Meet The Guardians`
- `Wild Encounters`
- `Itinerary`

The `Meet The Guardians` and `Wild Encounters` links open the official Toronto Zoo pages. The custom in-app experiences described here are the `Map`, `Animals`, and `Itinerary` pages.

## Map Page

The map page is the main exploration surface in the app. It combines a zoo map, date-based filtering, search, and interactive markers.

### Core map experience

Visitors can:

- view the zoo on an interactive map
- pan and zoom around the grounds
- switch between different map modes
- search for animals and points of interest
- click markers to open detailed information cards
- focus the map on specific search results

### Map modes

The map selector supports three viewing modes:

- `Summer Map` for a summer-oriented view
- `Winter Map` for a winter-oriented view
- `Specific Map` for a specific visit date selected by the visitor

When `Specific Map` is selected, the visitor can choose a date with a calendar picker. The map then refreshes using that date context.

### Date-aware behavior

The map page is built around the selected date.

Depending on the chosen day, the app can adjust:

- animal visibility
- closed exhibits shown on the map
- restaurant availability
- gift shop availability
- attraction availability
- drinking fountain availability
- Meet the Guardians talk availability
- Wild Encounter availability
- Zoomobile route selection
- active guest updates

For dates within the near-term weather window, the app also attempts to account for actual or forecast temperature so animal visibility can be more relevant to real conditions. Current-day map views use current weather, while future near-term dates use forecast data.

When the current local time is at or after the zoo's closing time, default map and itinerary date behavior moves to the next visit day.

### Explore panel controls

The left-hand Explore panel gives visitors direct control over what appears on the map.

Available toggles include:

- `Show region/pavilion text` to show or hide map label text
- `Include off display animals`
- `Include closed restaurants`
- `Include closed restrooms`
- `Include closed gift shops`
- `Include closed attractions`

These controls let the user decide whether the map should show only currently available options or also include items that may not be open or visible.

### Updates

The Explore panel can show an `Updates` module when there are active notices for the selected date.

Updates can include:

- closures
- new arrivals
- departures
- animal births
- animal passings

If more than one update is active, visitors can step through them with arrow controls. The Updates module can also be collapsed to keep the Explore panel compact while preserving the current map context.

### Zoomobile route controls

The map includes a dedicated Zoomobile route selector with four options:

- `None`
- `Current Route`
- `Summer Route`
- `Winter Route`

When a route is selected, the map can display the route overlay and the relevant Zoomobile stations.

### Type filtering

The `Filter` control is a multi-select dropdown that lets visitors choose which categories are displayed and searchable on the map.

Available categories include:

- Animals
- Pavilions
- Restaurants
- Restrooms
- Gift Shops
- Attractions
- Meet The Guardians Talks
- Wild Encounters
- Zoomobile Stations
- Drinking Fountains
- Defibrillators
- Emergency Intercoms
- Guest Services
- Picnic Sites
- Event Sites

This makes the map usable for both broad exploration and narrow task-based searches, such as finding only restaurants or only talks.

### Search on the map

The map page includes a search field for finding content quickly.

Search behavior includes:

- live search as the visitor types
- support for multiple content types, based on the current filter settings
- result cards with a title and a short subtitle
- a `View on Map` action for each result

If the visitor clicks `View on Map`, the app refreshes the visible layers if needed and then centers attention on the selected result.

### Interactive markers

Map markers are interactive and support both hover and click behaviors.

On hover, the user gets a quick label. On click, the user gets a larger tooltip card with more detail.

If multiple items share the same location, the tooltip becomes a carousel so the user can step through each item at that map point.

### Tooltip details by content type

The map tooltips are tailored to the item type.

Animal markers can show:

- species name
- exhibit
- enclosure type
- projected likelihood of seeing the animal
- an entry point into the full species overlay

Attraction markers can show:

- attraction name
- whether it is free with admission or an extra charge
- seasonal schedule information when available
- description text
- an external details link

Restaurant markers can show:

- restaurant name
- location or sub-location
- description text
- a direct menu link when available

Meet the Guardians markers can show:

- talk name
- location
- start time
- a general description of the talk experience

Talk schedules can vary by weekday, so the time shown reflects the selected date.

Wild Encounter markers can show:

- encounter name
- meeting spot
- time of day
- an external details link

The map can also show service and site markers for:

- Zoomobile stations
- drinking fountains
- defibrillators
- emergency intercoms
- guest services such as wheelchairs, information, First Aid & Family Center, and rentals/accessibility
- picnic sites
- event sites

### Animal detail overlay from the map

When a visitor clicks an animal name inside a map tooltip, the app opens a dedicated species overlay without leaving the page.

This overlay is designed to give a deeper animal profile and can include:

- the animal image
- common name
- Latin name
- exhibit name
- seasonal viewing summary
- seasonal viewing information
- general viewing tips
- seasonal viewing tips
- identification notes
- habitat and range
- diet and feeding information
- behaviour and social information
- adaptations
- reproduction and life cycle details
- Toronto Zoo-specific notes for that species

### Availability messaging on the map

The map page can surface status banners tied to the currently opened tooltip item. These status messages help explain when something is unavailable or less reliable on the selected date.

This includes messaging for:

- off-display animals
- closed restaurants
- closed gift shops
- closed attractions
- active guest updates

### Closed exhibit overlays

The map can also visually mark closed exhibits directly on the SVG map layer, helping visitors understand why certain areas or experiences may be unavailable on the selected day.

## Animals Page

The animals page is a browse-first directory of the zoo's animal collection. It is structured so visitors can move from broad categories to detailed species pages.

### Region-first browsing

The first screen presents zoo regions as large visual buttons. This gives visitors a simple starting point based on where animals live in the zoo.

Regions include:

- Africa
- Americas
- Australasia
- Canadian Domain
- Discovery Zone
- Eurasia Wilds
- Indo-Malaya
- Tundra Trek

### Region and exhibit drill-down

The animals experience supports two navigation patterns:

- for regions with multiple exhibits, the visitor first chooses an exhibit
- for regions that act as a single animal area, the visitor goes directly to the animal list

This keeps the browsing structure aligned with how the zoo is organized physically.

### Animal listing view

Inside an exhibit, the user sees a list of animals for that exhibit.

Each animal appears as a visual list button with species artwork, making the page approachable for casual browsing as well as destination-driven use.

The page also includes back navigation at each step, so the visitor can move:

- from animal detail back to the exhibit animal list
- from exhibit list back to the region list

### Animal detail page

Selecting an animal opens a dedicated species information page.

The detail page includes:

- a large animal image
- the animal's common name
- the animal's Latin name when available
- the exhibit name
- rich informational sections drawn from the animal record

The information sections can include:

- Seasonal Viewing Summary
- Seasonal Viewing Information
- General Viewing Tips
- Seasonal Viewing Tips
- Identification
- Habitat And Range
- Diet And Feeding
- Behaviour And Life Cycle
- Adaptations
- Reproduction And Life Cycle
- Animals At The Zoo

This page is meant to work as both a planning aid before a visit and an educational reference during the visit.

### View on Map from animal detail

Each animal detail page includes a `View on Map` button.

This sends the visitor directly to the map page and passes the selected species and exhibit into the map experience, so the map can focus on that animal without requiring the user to search again.

## Itinerary Page

The itinerary page is the planning workflow in the app. It combines a date-based planning wizard, a saved itinerary panel, and a map that displays only the selected itinerary items.

### Main purpose

The itinerary experience helps a visitor:

- choose a visit date
- select what they want to prioritize
- save those selections into a single plan
- review and edit the plan later
- see the selected items plotted on the zoo map

### Automatic first-run builder

If the visitor has not created an itinerary yet, the page automatically opens the itinerary builder. This removes friction and takes the user directly into the planning flow.

### Itinerary builder workflow

The builder is a guided overlay with multiple steps.

The steps are:

1. Set Visit Date
2. Add Animals by Region
3. Add Animals
4. Add Attractions
5. Meet the Guardians
6. Wild Encounters

The visitor can move forward step by step, go back, or finish early once they are satisfied with the current selection.

### Visit date selection

The first step asks the visitor to choose a visit date.

Date behavior in version 1.2.0 includes:

- calendar-based selection
- no manual text entry required
- dates limited to today through the allowed future booking window
- persistence of the selected date while building
- post-close defaults that move new planning sessions to the next visit day

The selected visit date becomes the basis for itinerary validation and availability filtering.

### Adding animals by region and exhibit

After setting the date, the user can bulk-select animal areas by region and exhibit.

This step allows visitors to:

- select whole regions
- select individual exhibits inside a region
- quickly seed the itinerary with animals tied to those chosen exhibits

This is useful for guests who plan geographically first, rather than species first.

### Adding individual animals

The next step supports direct animal search.

Animal selection features include:

- live search against the selected visit date
- animal thumbnails when available
- exhibit subtitles for context
- add and remove controls for each result
- an optional `Include off-display animals` toggle

When off-display animals are included, the selector can warn the visitor before adding an animal with a low projected viewing likelihood on that date.

The animal results can also show warning indicators for lower visibility.

### Adding attractions

The attractions step lets the visitor search for attractions and add them to the plan.

Features include:

- live attraction search
- attraction artwork when available
- clear labeling for `Free With Admission` versus `Extra Charge`
- a `More Info` link when the attraction provides one
- an optional `Include closed attractions` toggle

If the visitor includes closed attractions, the app warns before adding an attraction that is closed on the selected date.

### Adding Meet the Guardians talks

The Meet the Guardians step allows talk-based planning.

Each result can include:

- talk name
- location
- time of day
- event image

Talk times are date-aware and can differ by weekday. This helps visitors schedule educational talks around their route through the zoo.

### Adding Wild Encounters

The Wild Encounters step supports premium or scheduled encounter planning.

Each result can include:

- encounter name
- meeting spot
- time of day
- image
- external information link

This makes it possible for visitors to include special experiences alongside standard exhibit visits.

### Day planner view

Saved itineraries include a day planner view that arranges scheduled items around zoo hours.

The day planner can show:

- early admission and regular opening context when available
- scheduled Meet the Guardians talks
- scheduled Wild Encounters
- selected animals and attractions that do not have fixed times
- empty sections when there are no scheduled or unscheduled items

This gives the visitor a more practical view of when fixed-time experiences happen during the visit.

### Finishing and saving an itinerary

When the itinerary is finished, the app saves:

- visit date
- selected animals
- selected attractions
- selected Meet the Guardians talks
- selected Wild Encounters

If the visitor tries to finish with nothing selected, the app blocks completion and explains that at least one item must be added.

### Unsaved changes protection

If the visitor tries to close the builder after making changes, the app prompts them to either:

- save changes
- discard changes

This reduces accidental loss of planning work.

### Date-change validation

A core itinerary feature is date-based validation.

When the visit date changes, the app re-checks the existing itinerary against the newly selected day. It can then:

- remove items that are no longer available
- retain items that are still valid
- detect animals with reduced projected visibility
- detect animals with improved projected visibility

This is important because availability can vary by season, daily schedules, and closures.

### Itinerary update summary popup

If a date change affects the itinerary, the app can show an update popup summarizing what changed.

That popup can report:

- animals removed from the itinerary
- attractions removed from the itinerary
- Meet the Guardians talks removed from the itinerary
- Wild Encounters removed from the itinerary
- animals that are still included but now have reduced visibility
- animals that are still included and now have improved visibility

For changed items, the popup can also offer `View Alternatives` actions that reopen the relevant builder step so the visitor can replace what was lost.

### Saved itinerary panel

Once an itinerary exists, the left panel on the itinerary page becomes a structured summary of the plan.

The saved panel includes:

- an `Edit Itinerary` button
- a `Clear` button with confirmation
- a visit date card
- separate sections for Animals, Attractions, Meet the Guardians, and Wild Encounters
- access to a schedule-oriented day planner view

Each section shows a count and supports section editing.

### Section editing

The visitor can edit the itinerary at two levels:

- edit the entire itinerary from the main action bar
- edit a specific section directly from that section header

The visit date also has its own `Edit` action.

### Expandable and scrollable sections

Each itinerary section is collapsible. If a section contains more than a few items, it becomes internally scrollable so the page remains compact and usable on smaller screens.

### Item cards inside the itinerary

Saved itinerary entries are displayed as cards with item-specific details.

Depending on the item type, cards can show:

- image thumbnails
- exhibit names
- location details
- meeting spots
- times
- pricing labels
- availability alerts
- direct `More Info` links

Animal cards may also show projected visibility changes or date-related unavailability messages.

### Itinerary map behavior

The itinerary page includes its own map view.

Instead of showing the full zoo dataset, this map renders only the items currently saved in the itinerary:

- selected animals
- selected attractions
- selected Meet the Guardians talks
- selected Wild Encounters

This gives the visitor a focused visual plan rather than a full exploration map.

The itinerary map still supports:

- zooming and panning
- hover labels
- click tooltips
- animal detail overlays from map tooltips

### Clearing an itinerary

The `Clear` action removes all current selections after confirmation.

That includes:

- animals
- attractions
- Meet the Guardians talks
- Wild Encounters

After clearing, the page returns to its empty planning state.

## Current Scope

Toronto Zoo Guide delivers a strong planning and exploration workflow, with an emphasis on date-aware guest guidance.

The current release is especially focused on:

- helping guests discover what is available on a given day
- surfacing important date-based updates in the Explore panel
- making fixed-time talks and encounters easier to plan around
- connecting species education with navigation
- keeping planning practical through availability checks and visibility guidance
- making saved plans easy to review and revise

## Customer-Facing Summary

For a visitor, the app can be understood simply:

- use `Map` to explore what is around the zoo and what is available on a certain date
- use `Animals` to browse species and learn more about them
- use `Itinerary` to build a personalized visit plan and see that plan on the map

## Linting

The repo now includes separate linting for JavaScript and Python.

- install JavaScript lint dependencies with `npm install`
- install the Python lint dependency with `python3 -m pip install -r requirements-dev.txt`
- run JavaScript linting with `npm run lint:js`
- run Python linting with `npm run lint:py`
- run both with `npm run lint`

The JavaScript lint setup uses ESLint and is configured for the browser-based module structure in `scripts/`, including the CDN-loaded globals used by the app. The Python lint setup uses Ruff plus project-specific checks for typing, house style, and import ordering.
