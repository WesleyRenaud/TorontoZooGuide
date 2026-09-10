# CON-14 — Create event

**Preconditions:** Console open. Note: ending events may be unavailable — document in Notes.

**Date under test:** **D** inside event dates; also test a date outside range.

**Cleanup:** Note leftover event if it cannot be ended from console.

---

## Step 1 — Create event

- **Do:** **Create event** with name, location, description, optional link, dates covering D.
- **Expect:** Success created.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map Events shows

- **Do:** Map Explore → **Events** on D.
- **Expect:** Event visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Open link

- **Do:** If link present, open/check it.
- **Expect:** Link works or N/A.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Outside range

- **Do:** Set map date outside event range.
- **Expect:** Event absent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Inside range again

- **Do:** Return map date to D.
- **Expect:** Event present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — No itinerary required

- **Do:** Skip itinerary.
- **Expect:** Map-only verify OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Endability Notes

- **Do:** Check whether console can end/delete event.
- **Expect:** Notes.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Pass

- **Do:** Create + map date gating verified.
- **Expect:** Pass.
- **Result:** Pass / Fail / Blocked
- **Notes:**
