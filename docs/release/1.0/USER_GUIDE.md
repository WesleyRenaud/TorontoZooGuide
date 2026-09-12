# Toronto Zoo Guide — User guide (1.0)

How to use the guest app: Map, Animals, and Itinerary. A short Console appendix at the end is for zoo staff.

Local demo: `npm run seed`, `npm start`, then open `http://localhost:8000/map.html`.

---

## 1. Map

Open **Map** from the bottom nav.

### Explore panel

The left **Explore** panel controls what appears on the zoo map.

- Use **Filter:** to enable types such as **Animals**, **Attractions**, **Restaurants**, **Restrooms**, **Gift Shops**, **Meet The Guardians Talks**, **Wild Encounters**, and **Drinking Fountains**.
- Search within the enabled types.
- Toggle **Include off display animals** and **Include closed …** when you need markers that are normally hidden.
- Under Zoomobile / routes, choose **None**, **Current Route**, **Summer**, or **Winter**.
- **Updates** and **Events** (when present) always reflect **today’s** real calendar date, even if **Specific Map** is set to another day.

### Date presets

- **Summer Map** / **Winter Map** — seasonal snapshot of what is typically open and on display.
- **Specific Map** — pick a calendar day. Animal and attraction markers refresh for that day; Updates / Events stay on today.

Pan and zoom the map freely. Tap a marker for a tooltip / banner; use **More Info** when offered.

---

## 2. Animals

Open **Animals** from the bottom nav to browse or search the directory. From a species page, **View on Map** jumps to that animal’s marker on the map.

---

## 3. Itinerary

Open **Itinerary** from the bottom nav.

### Build a plan

1. Click **Build Itinerary** (or **Edit Itinerary** if you already have a plan).
2. **Set Visit Date**.
3. Add animals (by search and/or by region), then attractions, Meet the Guardians talks, Wild Encounters, and transportation as you like.
4. Click **Finish**.

Closing the builder with unsaved edits asks **Save Changes?** — choose **Save** to keep them or **Discard** to throw them away.

**Clear** removes the whole plan after **Clear Itinerary?** confirmation.

### List View and Day Planner

- **List View** — everything on your plan, grouped (animals, attractions, talks, encounters, transportation).
- **Day Planner View** — timed pills on a day timeline, plus walking path on the itinerary map.

Use **Schedule an item** to place something at a time. **Rebuild schedule** lays out unscheduled animals automatically. **Unschedule all items** clears the day plan without removing items from the itinerary list.

If you schedule something that is not on the plan yet, **Add to Itinerary?** appears; confirm with **Add to Schedule**.

### Talks, encounters, and conflicts

Fixed-time talks and wild encounters land on the Day Planner at their offered times when you finish the builder.

If two offerings cannot both keep their full windows, Finish shows **Your Itinerary Has the Following Issues:** with **Schedule Conflicts**.

- Same start time: pick one activity (or proceed with none).
- Partial overlap: selecting both can open **Adjust Activity Times?** with the message *“These selections overlap in time. We’ll fit them into your day by shortening some activities, with Wild Encounters taking priority.”* **Proceed** keeps both with adjusted times; **Cancel** leaves the second unselected.

Adding a talk or encounter whose fixed time overlaps items already on the Day Planner shows **Add Guardians Talk?** or **Add Wild Encounter?** — confirm with **Update Plan** to place the fixed time and reshuffle the walk. If nothing on the day overlaps that slot, Finish saves without that prompt.

### Zoomobile: attraction vs transportation

- On **Add Attractions**, selecting **Zoomobile** asks **Add as Attraction?** (scenic timed stop you can schedule yourself).
- On **Add Transportation**, selecting **Zoomobile** asks **Add as Transportation?** (used to cut walking when the day is bulk-scheduled).

After **Finish** / **Rebuild schedule**, transportation Zoomobile appears under **Transportation** on the list and as ride pills on Day Planner (station lines such as **Main Zoomobile Station → …**). Removing it warns that remaining items will be rescheduled without it.

### Closed attractions and off-display animals

- **Include closed attractions** (builder) or map toggles reveal closed venues; adding one asks **Attraction May Be Closed**.
- **Include off-display animals** can show animals that may not be viewable; adding one asks **Animal May Be Off Display**.

### Arrival, departure, and early admission

On Day Planner, set arrival and departure. Very short windows may ask **Short Visit?**. Times before normal zoo open may ask **Early Admission Hours** (members / sensory hours).

If your saved visit date is in the past, **Itinerary Date Has Passed** lets you pick a new date or clear the plan.

---

## 4. Console (staff)

Open `http://localhost:8000/console-operations.html` for live operations: animal off/on display, visibility schedules, alerts, exhibit and amenity open/closed, attraction hours and closure overrides, Zoomobile station/route, guardians talk and wild encounter schedules, drinking fountains, updates, and events.

Each console change should be checked on **Map** and/or **Itinerary** for **today** (guest pages), then cleaned up. See the Console suites in the [manual test hub](../../manual-tests/index.html) and [RELEASE.md](RELEASE.md).

---

## Related

- [RELEASE.md](RELEASE.md) — 1.0 scope and QA map
- [Manual tests README](../../manual-tests/README.md) — how to run pass/fail suites
