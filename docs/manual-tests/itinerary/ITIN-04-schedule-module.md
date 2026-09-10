# ITIN-04 — Schedule module

**Preconditions:** Complete a saved itinerary with several unscheduled animals (from ITIN-01 or new build).

**Date under test:** Same visit date as the itinerary.

**Cleanup:** Optional: **Unschedule all items** before leaving.

---

## Step 1 — Open schedule UI

- **Do:** In the itinerary panel, open the schedule-an-item / scheduling controls.
- **Expect:** Schedule module is visible (type, search, time).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Choose type

- **Do:** Select animal (or matching type for an itinerary item).
- **Expect:** Type filter applies to searchable items.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Search item

- **Do:** Search for an animal already on the itinerary.
- **Expect:** Matching results appear.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Only on my itinerary

- **Do:** Enable **Only show items on my itinerary**.
- **Expect:** Results restricted to itinerary items.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Pick time

- **Do:** Choose a valid time within arrival/departure if set.
- **Expect:** Time accepted.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Optional duration

- **Do:** Set duration if the field is shown.
- **Expect:** Duration accepted or defaults applied.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Schedule succeeds

- **Do:** Submit/schedule the item.
- **Expect:** A scheduled pill appears on the Day Planner timeline.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Unschedule via pill menu

- **Do:** Open the pill menu and unschedule.
- **Expect:** Pill removed; item remains on list unscheduled.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Reschedule

- **Do:** Schedule the same item again at a different time.
- **Expect:** New pill appears at the new time.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Remove if offered

- **Do:** From pill/list menu, remove from itinerary if available.
- **Expect:** Item leaves itinerary (or note if remove is list-only).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — List vs planner sync

- **Do:** Compare list view and Day Planner.
- **Expect:** Scheduled vs unscheduled state matches across views.
- **Result:** Pass / Fail / Blocked
- **Notes:**
