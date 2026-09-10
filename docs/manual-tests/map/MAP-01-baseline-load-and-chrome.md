# MAP-01 — Baseline load and chrome

**Preconditions:** `npm run seed`, `npm start`, browser DevTools console open. Open `http://localhost:8000/map.html`.

**Date under test:** Default **Specific Map** (whatever date the picker shows after load).

**Cleanup:** None.

---

## Step 1 — Open map page

- **Do:** Navigate to `map.html`.
- **Expect:** Page loads; zoo map SVG appears in the map mount; no hard failure / blank page.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Check browser console

- **Do:** Inspect the DevTools console for load errors.
- **Expect:** No uncaught errors related to map SVG, markers, or bootstrap (benign 3rd-party noise OK — note it).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Explore panel visible

- **Do:** Look at the left **Explore** panel.
- **Expect:** Panel titled **Explore** is visible with toggles, Filter, and search.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Bottom nav links

- **Do:** Inspect the bottom nav.
- **Expect:** Links include **Map**, **Animals**, Meet the Guardians (external), Wild Encounters (external), and **Itinerary**.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Pan map

- **Do:** Click-drag the map canvas.
- **Expect:** Map pans; markers move with the map.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Zoom map

- **Do:** Zoom in and out (scroll/pinch/controls as available).
- **Expect:** Map zooms; markers remain attached to locations.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Show region/pavilion text on

- **Do:** Enable **Show region/pavilion text** if it is not already on (it may default checked).
- **Expect:** Region/pavilion labels appear on the map.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Show region/pavilion text off

- **Do:** Disable **Show region/pavilion text**.
- **Expect:** Those labels hide again.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Default animal markers

- **Do:** With default filters (Animals checked), observe the map.
- **Expect:** Animal markers are visible on **Specific Map**; map mount is not empty/broken.
- **Result:** Pass / Fail / Blocked
- **Notes:**
