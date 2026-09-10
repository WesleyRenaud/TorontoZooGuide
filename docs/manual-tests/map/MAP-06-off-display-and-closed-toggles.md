# MAP-06 — Off-display and closed include toggles

**Preconditions:** Self-contained: use Specific Map dates where seed already yields off-display animals or closed amenities. **Do not use console.** If unreachable, mark steps **Blocked** → CON-01 / CON-05 / CON-06 / CON-07 / CON-08.

**Date under test:** Record date(s) attempted.

**Cleanup:** Leave include toggles unchecked.

---

## Step 1 — Baseline

- **Do:** Note marker set with all include-* toggles off.
- **Expect:** Baseline recorded.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Include off display animals on

- **Do:** Enable **Include off display animals**.
- **Expect:** Additional animals and/or off-display banners appear **or** Blocked if seed has none for this date.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Off-display feedback

- **Do:** If animals appeared, inspect tooltip/banner.
- **Expect:** Off-display messaging present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Include off display off

- **Do:** Disable the toggle.
- **Expect:** Those animals hide again.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Include closed restaurants

- **Do:** Enable **Include closed restaurants**.
- **Expect:** Closed restaurants appear **or** Blocked.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Restaurants off

- **Do:** Disable **Include closed restaurants**.
- **Expect:** Extra closed restaurants hide.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Include closed restrooms

- **Do:** Enable then disable **Include closed restrooms**.
- **Expect:** Show/hide works **or** Blocked.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Include closed gift shops

- **Do:** Enable then disable **Include closed gift shops**.
- **Expect:** Show/hide works **or** Blocked.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Include closed attractions

- **Do:** Enable then disable **Include closed attractions**.
- **Expect:** Show/hide works **or** Blocked.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Banner readability

- **Do:** With any include toggle that shows banners, read banner text.
- **Expect:** Banners readable; layout not fully broken.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — No console used

- **Do:** Confirm this suite did not open console-operations.
- **Expect:** Self-contained requirement met.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Reset toggles

- **Do:** Uncheck all include-* toggles.
- **Expect:** Map back to default inclusion behavior.
- **Result:** Pass / Fail / Blocked
- **Notes:**
