# ITIN-05 — Rebuild and unschedule all

**Preconditions:** Itinerary with multiple scheduled items and a visible walk path on the itinerary map.

**Date under test:** Visit date.

**Cleanup:** Optional reschedule one item so the itinerary is not empty of schedule.

---

## Step 1 — Note baseline

- **Do:** Note existing pills and walk path.
- **Expect:** Baseline recorded.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Rebuild schedule

- **Do:** Click **Rebuild schedule**.
- **Expect:** Pills/path regenerate (may reshuffle times).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Path after rebuild

- **Do:** Inspect itinerary map.
- **Expect:** Walk path present if ≥2 scheduled stops.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Unschedule all

- **Do:** Click **Unschedule all items**.
- **Expect:** Confirm prompt if shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Confirm unschedule all

- **Do:** Confirm if prompted.
- **Expect:** All schedule pills cleared.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Path cleared

- **Do:** Inspect map pane.
- **Expect:** Walk path cleared.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — List retained

- **Do:** Check list view.
- **Expect:** Items remain on itinerary as unscheduled.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Schedule one again

- **Do:** Schedule a single animal.
- **Expect:** Pill returns; path may be absent with one stop.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Stable UI

- **Do:** Toggle list/planner.
- **Expect:** No crash after unschedule-all.
- **Result:** Pass / Fail / Blocked
- **Notes:**
