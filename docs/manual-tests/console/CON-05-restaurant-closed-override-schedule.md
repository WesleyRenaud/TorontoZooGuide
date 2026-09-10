# CON-05 — Restaurant closed / override / schedule

**Preconditions:** Console open. Known restaurant on map.

**Date under test:** **D** for closed checks; may use alternate dates for override/schedule.

**Cleanup:** Restaurant open on D; remove test overrides/schedules as needed.

---

## Step 1 — Set closed

- **Do:** **Set restaurant as closed** for range covering D + message.
- **Expect:** Success closed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map without include

- **Do:** Map D; **Include closed restaurants** off.
- **Expect:** Restaurant hidden/closed treatment.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Map with include

- **Do:** Enable **Include closed restaurants**.
- **Expect:** Visible + closed message.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Closure override

- **Do:** **Create restaurant closure override** so D (or a sub-range) reopens.
- **Expect:** Success override saved.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Map reflects override

- **Do:** Map on overridden open day.
- **Expect:** Appears open/available as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Opening schedule conflict

- **Do:** **Set restaurant opening schedule** overlapping an existing schedule.
- **Expect:** **Schedule conflict** dialog if overlap exists.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Resolve overlap

- **Do:** Choose **Trim Old Schedules** or **Delete Old Schedules**.
- **Expect:** Schedule saves; note choice.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Map matches schedule

- **Do:** Map on a day implied open by new schedule.
- **Expect:** Open state correct.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Cleanup closed

- **Do:** Ensure D is not left closed unintentionally.
- **Expect:** Open or intentionally documented.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Verify map open

- **Do:** Map D with include-closed off.
- **Expect:** Normal open marker if intended open.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Status messages

- **Do:** Confirm each submit showed success status text.
- **Expect:** Statuses OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Notes

- **Do:** Record overlap choice and restaurant name.
- **Expect:** Notes filled.
- **Result:** Pass / Fail / Blocked
- **Notes:**
