# CON-15 — Console validation matrix

**Preconditions:** Console open. No guest map/itinerary verify required. Use any convenient entities.

**Date under test:** N/A.

**Cleanup:** Delete/revert the one successful submit at the end.

---

## Step 1 — Missing entity

- **Do:** Submit an op that requires an entity with it blank (e.g. closed restaurant without name).
- **Expect:** Validation: entity required style message.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — End before start

- **Do:** Enter end date before start date.
- **Expect:** **End date cannot be before the start date.** (or Invalid start/end).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Daily viewing times

- **Do:** Visibility schedule without start/end times.
- **Expect:** **Daily viewing start and end times are required.**
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Weekly preset locks

- **Do:** Opening schedule: try **weekendsOnly** / holidays checkbox interaction.
- **Expect:** Holidays checkbox locks/behaves per preset.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Attraction hours inverted

- **Do:** **Set attraction hours** with weekday start after end.
- **Expect:** **Weekday start time must be before weekday end time.**
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Hours outside zoo hours

- **Do:** Set attraction hours outside zoo bounds.
- **Expect:** Bounds validation or API invalid hours message.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Duplicate encounter time

- **Do:** Wild encounter schedule with duplicate time rows.
- **Expect:** **Each encounter time can only be added once.**
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Empty required message

- **Do:** Closed op without required guest message if required.
- **Expect:** Validation blocks submit.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Overlap Cancel

- **Do:** Trigger **Schedule conflict** and click Cancel.
- **Expect:** No schedule change applied.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Fix one form valid

- **Do:** Correct one form to valid inputs.
- **Expect:** Ready to submit.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Success submit

- **Do:** Submit successfully.
- **Expect:** Success status shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Cleanup success row

- **Do:** Revert/end/delete that successful test row.
- **Expect:** Clean.
- **Result:** Pass / Fail / Blocked
- **Notes:**
