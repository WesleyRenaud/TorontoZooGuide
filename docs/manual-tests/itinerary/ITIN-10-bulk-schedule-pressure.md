# ITIN-10 — Bulk schedule pressure

**Preconditions:** Clear itinerary. Plan to select many animals via regions and a short visit window.

**Date under test:** Busy in-season date.

**Cleanup:** Clear itinerary after.

---

## Step 1 — Large animal set

- **Do:** On **Add Animals by Region**, select multiple regions; keep many animals.
- **Expect:** Large selection created.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Short visit window

- **Do:** After finish (or in planner), set arrival/departure to a short window (e.g. 2 hours).
- **Expect:** Short window set.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Build/finish

- **Do:** Finish/build so bulk schedule runs.
- **Expect:** Bulk scheduling runs.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Unscheduled leftovers

- **Do:** Inspect list vs planner.
- **Expect:** Some animals remain list-only unscheduled.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Not enough time messaging

- **Do:** Look for not-enough-day-time / save-issues messaging.
- **Expect:** Messaging present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Save issues Proceed

- **Do:** If **Your Itinerary Has the Following Issues:** appears, click **Proceed**.
- **Expect:** Proceed works.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Lengthen day

- **Do:** Widen arrival–departure substantially.
- **Expect:** Window updated.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Rebuild

- **Do:** Click **Rebuild schedule**.
- **Expect:** More items schedule successfully than before.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Sanity

- **Do:** Confirm no crash with large lists.
- **Expect:** UI remains responsive enough to use.
- **Result:** Pass / Fail / Blocked
- **Notes:**
