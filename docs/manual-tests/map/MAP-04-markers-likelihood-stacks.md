# MAP-04 — Markers, likelihood, stacks

**Preconditions:** Open `map.html` on **Specific Map**. Prefer a shoulder-season date (e.g. late March or November) for mixed likelihood tints.

**Date under test:** Record the Specific Map date used.

**Cleanup:** None.

---

## Step 1 — Pick mixed-likelihood date

- **Do:** Set Specific Map to a shoulder-season date.
- **Expect:** Date applies; markers reload.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Likelihood tint

- **Do:** Compare an animal icon tint to a peak-summer date for the same species (toggle date).
- **Expect:** Tint/likelihood styling differs where the seasonal curve is not flat — note species checked.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Find stack or skip

- **Do:** Look for a stacked/count marker at shared coordinates.
- **Expect:** If none in seed: **Blocked** — stacking covered when shared coords exist; continue other steps.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Click stack

- **Do:** Click a stacked marker (if present).
- **Expect:** Multi-item UI / carousel appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Carousel UI

- **Do:** Confirm multiple items are listed or carouseled.
- **Expect:** More than one entity is represented.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Advance carousel

- **Do:** Use next/prev on the carousel if present.
- **Expect:** Each item becomes identifiable (name/type).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Amenity styling spot-check

- **Do:** Enable **Restaurants** or **Gift Shops** or **Attractions**; spot-check open/closed or likelihood styling.
- **Expect:** Markers render with expected open/closed or likelihood treatment.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Limited-viewing / alert badge

- **Do:** If seed has limited viewing or alerts, find `marker-has-limited-viewing` / badge styling.
- **Expect:** Badge visible if data exists; else **Blocked** → CON-02/CON-03.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Zoom stability

- **Do:** Zoom in/out around markers.
- **Expect:** Markers stay anchored; not orphaned off-map incorrectly.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Return to Specific Map

- **Do:** Leave a mid-season Specific Map date selected.
- **Expect:** Map remains usable.
- **Result:** Pass / Fail / Blocked
- **Notes:**
