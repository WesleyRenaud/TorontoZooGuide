# CON-07 — Gift shop closed / override / schedule

**Preconditions:** Console open. Known gift shop. Prefer either override **or** full schedule depth to keep ~10 steps.

**Date under test:** **D** for closed verify.

**Cleanup:** Gift shop open; test overrides/schedules cleaned.

---

## Step 1 — Set closed

- **Do:** **Set gift shop as closed** covering D.
- **Expect:** Success.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map without include

- **Do:** Map; **Include closed gift shops** off.
- **Expect:** Hidden/closed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Map with include

- **Do:** Enable include closed gift shops.
- **Expect:** Visible + message.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Override or schedule

- **Do:** Either **Create gift shop closure override** OR **Set gift shop opening schedule**.
- **Expect:** Success path chosen — note which.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Overlap if schedule

- **Do:** If schedule overlaps, resolve **Schedule conflict**.
- **Expect:** Trim/Delete/Cancel noted.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Map after change

- **Do:** Map on D / open day.
- **Expect:** Matches intended open/closed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Cleanup closed

- **Do:** Re-open if still closed.
- **Expect:** Open.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Verify map

- **Do:** Include-closed off.
- **Expect:** Normal marker if open.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Statuses

- **Do:** Each submit showed success.
- **Expect:** OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Notes

- **Do:** Record gift shop name and path used.
- **Expect:** Notes.
- **Result:** Pass / Fail / Blocked
- **Notes:**
