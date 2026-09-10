# ITIN-11 — Draft and past-date recovery

**Preconditions:** Ability to use localStorage draft and past-date recovery UI. May require setting visit date to a past day after save, or using recovery entry points the app provides.

**Date under test:** Start future; then exercise past recovery.

**Cleanup:** `npm run clear:itinerary` + clear itinerary-config if sticky.

---

## Step 1 — Mid-wizard draft

- **Do:** Start builder, set date, select animals; do not finish.
- **Expect:** Draft in progress.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Refresh

- **Do:** Reload `itinerary.html`.
- **Expect:** Page reloads.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Draft restored

- **Do:** Re-open builder.
- **Expect:** Draft restored from localStorage (selections/date retained).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Complete save

- **Do:** Finish to save itinerary.
- **Expect:** Saved itinerary present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Trigger past-date recovery

- **Do:** Cause past-date recovery (set visit date in the past if UI allows, or open app when saved date is past).
- **Expect:** Past-date recovery UI appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Choose new date

- **Do:** Choose a new future date.
- **Expect:** Recovery continues.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Removed-items popup

- **Do:** Review animals added/removed, talks unavailable, times adjusted, etc.
- **Expect:** Popup sections match changes.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Keep vs remove

- **Do:** Use **Keep** / remove choices where offered.
- **Expect:** Choices apply.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Alternate clear path

- **Do:** On another run, choose clear itinerary from recovery if available.
- **Expect:** Empty itinerary result.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Don’t show again

- **Do:** If suppression checkbox exists, note behavior.
- **Expect:** Pass/N/A.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Coherent result

- **Do:** Inspect itinerary after accepting recovery.
- **Expect:** New date itinerary coherent.
- **Result:** Pass / Fail / Blocked
- **Notes:**
