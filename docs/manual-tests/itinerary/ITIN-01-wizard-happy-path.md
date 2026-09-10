# ITIN-01 — Wizard happy path

**Preconditions:** `npm run clear:itinerary` if needed. Open `itinerary.html`. Prefer a future in-season visit date with animals offered.

**Date under test:** Chosen future visit date (record it).

**Cleanup:** `npm run clear:itinerary` or **Clear Itinerary?** when done.

---

## Step 1 — Open itinerary

- **Do:** Open `itinerary.html`. Use **Edit Itinerary** / **Build Itinerary** to open the builder if needed.
- **Expect:** Itinerary page loads; builder can be opened.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Set Visit Date

- **Do:** Complete **Set Visit Date** and continue.
- **Expect:** Date is accepted; next wizard step appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Add Animals by Region

- **Do:** On **Add Animals by Region**, select at least one region/exhibit and continue.
- **Expect:** Selection is kept; proceed to animals.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Add Animals

- **Do:** On **Add Animals**, add ≥1 animal.
- **Expect:** Animal appears selected in the builder.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Add Attractions

- **Do:** On **Add Attractions**, add 0 or 1 attraction and continue.
- **Expect:** Step completes (empty OK).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Meet the Guardians

- **Do:** On the Meet the Guardians step, add a talk if listed, else continue.
- **Expect:** Pass with Notes “none offered” if empty for the date.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Wild Encounters

- **Do:** On **Wild Encounters**, add one if listed, else continue.
- **Expect:** Pass with Notes “none offered” if empty.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Add Transportation

- **Do:** On **Add Transportation**, add or skip, then continue toward finish.
- **Expect:** Step completes.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Finish with items

- **Do:** Click **Finish** with ≥1 total selected item.
- **Expect:** Finish succeeds (not **No Items Selected**).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — List view

- **Do:** Click **List View** and confirm sections.
- **Expect:** Sections show selected animals (and other types if chosen); **List View** control is available.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Day Planner view

- **Do:** Switch to **Day Planner View** if not already shown.
- **Expect:** Day Planner / timeline UI is available (**Arrival time**, **Departure time**, scheduled/unscheduled sections).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Map pane markers

- **Do:** Look at the itinerary map pane.
- **Expect:** Planned item markers appear on the map.
- **Result:** Pass / Fail / Blocked
- **Notes:**
