# ITIN-12 — Map path smoke on itinerary

**Preconditions:** Scheduled multi-stop day (≥2 scheduled animals/stops).

**Date under test:** Visit date.

**Cleanup:** **Unschedule all items** or clear itinerary.

---

## Step 1 — Multi-stop planner

- **Do:** Ensure Day Planner has ≥2 scheduled stops.
- **Expect:** Pills visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Walk path drawn

- **Do:** Inspect itinerary map.
- **Expect:** Walk path/route overlay drawn.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Pan/zoom path

- **Do:** Pan/zoom the itinerary map.
- **Expect:** Path remains visible/coherent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Unschedule middle

- **Do:** Unschedule a middle stop.
- **Expect:** Path updates (not stale).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Add Zoomobile transport

- **Do:** Add Zoomobile as transportation and schedule/rebuild as needed.
- **Expect:** Transport reflected in legs/path.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Path reflects transport

- **Do:** Inspect path/legs.
- **Expect:** Transport segment distinguishable or walking reduced as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Scenic vs transport

- **Do:** If Zoomobile also exists as scenic attraction, ensure scenic add does not impersonate transport leg.
- **Expect:** Representations distinct.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Unschedule all clears path

- **Do:** **Unschedule all items**.
- **Expect:** Walk path clears.
- **Result:** Pass / Fail / Blocked
- **Notes:**
