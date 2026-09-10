# ITIN-06 — Off-display / low-likelihood confirm

**Preconditions:** Self-contained. Prefer winter/shoulder visit date for low likelihood, or enable **Include off-display animals**. If impossible from seed alone: Blocked → CON-01.

**Date under test:** Record visit date.

**Cleanup:** Clear itinerary if desired.

---

## Step 1 — Open animal step

- **Do:** In builder, reach **Add Animals**.
- **Expect:** Animal selector visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Include off-display

- **Do:** Enable **Include off-display animals** if testing off-display.
- **Expect:** Toggle on.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Select target animal

- **Do:** Select an off-display or very low-likelihood animal.
- **Expect:** Confirm dialog appears (off-display or below-threshold likelihood message).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Cancel confirm

- **Do:** Cancel/dismiss without adding.
- **Expect:** Animal not added.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Select again

- **Do:** Select the same animal again.
- **Expect:** Confirm appears again.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Confirm add

- **Do:** Confirm add.
- **Expect:** Animal added to selection.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Finish

- **Do:** Finish itinerary with that animal included.
- **Expect:** Build succeeds.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — List cue

- **Do:** Inspect list for status/likelihood cue if any.
- **Expect:** Cue present or note absent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Document Blocked path

- **Do:** If no such animal existed for the date, mark suite Blocked.
- **Expect:** Notes point to CON-01 or alternate date.
- **Result:** Pass / Fail / Blocked
- **Notes:**
