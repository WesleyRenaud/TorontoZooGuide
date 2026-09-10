# CON-10 — Guardians talks

**Preconditions:** Console open. Known talk location + talk name from seed.

**Date under test:** **D** included in schedule / occurrence.

**Cleanup:** End schedules; cancel leftover occurrences; map quiet for talk on D if intended.

---

## Step 1 — Set schedule

- **Do:** **Set Meet the Guardians talk schedule** with **Location**, **Talk name**, recurring **Talk times**, range including D (**Stops being offered on** as needed).
- **Expect:** Success schedule saved.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map talk visible

- **Do:** Map D; enable **Meet The Guardians Talks** filter.
- **Expect:** Talk marker/tooltip present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Itinerary lists talk

- **Do:** Itinerary builder on D; Meet the Guardians step.
- **Expect:** Talk offered.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Add occurrence

- **Do:** **Add Meet the Guardians talk occurrence** for a date/time.
- **Expect:** Success added.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Cancel occurrence

- **Do:** **Cancel Meet the Guardians talk occurrence**.
- **Expect:** Success cancelled.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Cancelled absent

- **Do:** Itinerary/map for cancelled slot.
- **Expect:** Cancelled occurrence absent as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — End schedule

- **Do:** **End Meet the Guardians talk schedule**.
- **Expect:** Success ended.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Future clear

- **Do:** Check a future date that was only covered by ended schedule.
- **Expect:** Talks cleared as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Duplicate time Notes

- **Do:** Optionally resubmit duplicate time to see error.
- **Expect:** Error string noted (optional).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Cleanup

- **Do:** No unintended live schedules left for test talk.
- **Expect:** Clean.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Final map

- **Do:** Map filter talks on D.
- **Expect:** Quiet/expected state.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Record names

- **Do:** Notes: talk + location + D.
- **Expect:** Notes.
- **Result:** Pass / Fail / Blocked
- **Notes:**
