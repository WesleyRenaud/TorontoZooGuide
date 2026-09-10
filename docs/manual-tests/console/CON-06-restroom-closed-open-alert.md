# CON-06 — Restroom closed/open + alert

**Preconditions:** Console open. Known restroom.

**Date under test:** **D** for closed/open.

**Cleanup:** Restroom open; alerts removed.

---

## Step 1 — Close restroom

- **Do:** **Set restroom as closed** for D.
- **Expect:** Success.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map closed behavior

- **Do:** Map D; try with/without **Include closed restrooms**.
- **Expect:** Show/hide matches toggles.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Set alert

- **Do:** **Set restroom alert** (same or another restroom) covering D.
- **Expect:** Success alert.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Map alert badge

- **Do:** Map shows alert badge/styling.
- **Expect:** Alert visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Remove alert

- **Do:** **Remove restroom alert**.
- **Expect:** Success removed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Open restroom

- **Do:** **Set restroom as open**.
- **Expect:** Success open.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Map open

- **Do:** Map D.
- **Expect:** Restroom open/normal.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Include-closed spot-check

- **Do:** Toggle include closed restrooms once more.
- **Expect:** Behaves.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Cleanup

- **Do:** No leftover closure/alert.
- **Expect:** Clean.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Pass criteria

- **Do:** Marker state matches last ops.
- **Expect:** Pass if matched.
- **Result:** Pass / Fail / Blocked
- **Notes:**
