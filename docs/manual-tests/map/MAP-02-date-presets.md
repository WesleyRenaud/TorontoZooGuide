# MAP-02 — Date presets

**Preconditions:** MAP-01 baseline OK. Open `map.html`.

**Date under test:** Exercise **Summer Map**, **Winter Map**, and **Specific Map**.

**Cleanup:** Leave preset on **Specific Map** when finished.

---

## Step 1 — Select Summer Map

- **Do:** In the map controls dropdown, choose **Summer Map**.
- **Expect:** Preset switches to **Summer Map**.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Summer date control

- **Do:** Observe `#mapDate` / date field.
- **Expect:** Date input is hidden or not used for free picking (summer uses fixed seasonal anchor).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Summer markers context

- **Do:** Note animal/amenity marker set and Explore **Updates** if shown.
- **Expect:** Map content reflects summer context (differs from mid-winter where species/amenities are seasonal).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Select Winter Map

- **Do:** Choose **Winter Map**.
- **Expect:** Preset switches to **Winter Map**.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Winter date control

- **Do:** Observe the date field again.
- **Expect:** Date picking stays locked/hidden as designed for winter preset.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Winter vs summer difference

- **Do:** Compare markers/Updates to what you saw on Summer Map.
- **Expect:** At least some seasonal difference is visible (animals, closed exhibits, updates, or Zoomobile season) — note what changed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Select Specific Map

- **Do:** Choose **Specific Map**.
- **Expect:** Preset switches; date field becomes available.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Open date picker

- **Do:** Click the date input.
- **Expect:** Flatpickr (or date UI) opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Pick mid-season date

- **Do:** Choose a mid-season date (e.g. a day in May or September).
- **Expect:** Date applies; map refetches.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Refresh for that date

- **Do:** Watch markers and Updates/Events after the date change.
- **Expect:** Markers and Updates/Events refresh for the selected date without requiring a full page reload.
- **Result:** Pass / Fail / Blocked
- **Notes:**
