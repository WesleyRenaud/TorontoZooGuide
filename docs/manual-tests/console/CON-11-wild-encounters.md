# CON-11 — Wild encounters

**Preconditions:** Console open. Known wild encounter from seed.

**Date under test:** **D** in schedule.

**Cleanup:** End schedule; cancel test occurrences.

---

## Step 1 — Set schedule

- **Do:** **Set Wild Encounter schedule** including D.
- **Expect:** Success saved.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map verify

- **Do:** Map D; enable **Wild Encounters** filter.
- **Expect:** Meeting spot / encounter marker visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Itinerary selector

- **Do:** Itinerary Wild Encounters step on D.
- **Expect:** Encounter listed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Cancel occurrence

- **Do:** **Cancel Wild Encounter occurrence** (add occurrence first only if required to have something to cancel).
- **Expect:** Success cancelled.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Cancelled absent

- **Do:** Itinerary/map for that slot.
- **Expect:** Absent as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — End schedule

- **Do:** **End Wild Encounter schedule**.
- **Expect:** Success ended.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Future clear

- **Do:** Future date check.
- **Expect:** Cleared as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Duplicate time optional

- **Do:** Optional duplicate-time validation Notes.
- **Expect:** Optional.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Cleanup

- **Do:** No leftover test schedule.
- **Expect:** Clean.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Final map

- **Do:** Map quiet/expected.
- **Expect:** OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**
