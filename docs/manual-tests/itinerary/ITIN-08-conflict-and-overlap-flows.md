# ITIN-08 — Conflict and overlap flows

**Preconditions:** Itinerary with enough timed items to create overlaps (animals + talk/attraction).

**Date under test:** Visit date.

**Cleanup:** Resolve to a coherent timeline before leaving.

---

## Step 1 — Schedule item A

- **Do:** Schedule first timed item.
- **Expect:** Pill A on timeline.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Schedule overlapping B

- **Do:** Schedule second item at overlapping time.
- **Expect:** Conflict picker or overlap warning appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Conflict picker

- **Do:** Use multi-select non-overlapping resolution if shown.
- **Expect:** Can choose a non-overlapping set.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Proceed without selection

- **Do:** Find **Proceed Anyway** / proceed-without-selection if offered; try once.
- **Expect:** Behavior recorded (allowed or blocked).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Unresolved messaging

- **Do:** Leave a conflict unresolved if UI allows, then try save.
- **Expect:** Clear messaging.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Add more activities prompt

- **Do:** If “add more activities?” style prompt appears, note it.
- **Expect:** Pass/N/A.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — WE overlap if needed

- **Do:** If ITIN-07 did not cover WE overlap, force WE vs animal overlap.
- **Expect:** WE overlap message appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Save issues summary

- **Do:** Trigger **Your Itinerary Has the Following Issues:** if applicable.
- **Expect:** Summary lists issues.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Proceed from save issues

- **Do:** Click **Proceed**.
- **Expect:** Save continues.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — No silent double-book

- **Do:** Inspect final timeline.
- **Expect:** No silent double-booking without prior warning.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Stable after conflicts

- **Do:** Reload itinerary panel.
- **Expect:** State matches last save.
- **Result:** Pass / Fail / Blocked
- **Notes:**
