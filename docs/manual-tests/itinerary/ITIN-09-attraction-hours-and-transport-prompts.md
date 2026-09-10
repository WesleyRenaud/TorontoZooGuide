# ITIN-09 — Attraction hours and transport prompts

**Preconditions:** Seed attraction with hours; Zoomobile or dual-role attraction/transport if available.

**Date under test:** Visit date when attraction is open if possible.

**Cleanup:** Clear or leave a simple itinerary.

---

## Step 1 — Add attraction

- **Do:** Add an attraction in the wizard.
- **Expect:** Attraction selected.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Schedule outside hours

- **Do:** After finish, schedule it outside operating hours.
- **Expect:** Snap to nearest valid time and/or warning.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Confirm snap

- **Do:** Note the resulting time.
- **Expect:** Time inside operating window or explicit override noted.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Closed-day confirm

- **Do:** If visit date is closed for that attraction, attempt add.
- **Expect:** **Attraction May Be Closed** confirm **or** N/A.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Attraction also transportation

- **Do:** Add Zoomobile (or dual-role) via path that shows **Add as Attraction?**
- **Expect:** Prompt appears with scenic vs transport messaging.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Choose as attraction

- **Do:** Confirm add-as-attraction path.
- **Expect:** Listed as attraction.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Add as transportation

- **Do:** Use **Add as Transportation?** path (retry/alternate add).
- **Expect:** Listed as transportation.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — List representations

- **Do:** Inspect list sections.
- **Expect:** Attraction vs transportation representations are distinct and correct.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Hours validation bubble

- **Do:** If manual time edit exists, enter invalid hours.
- **Expect:** Validation bubble shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Finish/save stable

- **Do:** Save/finish remaining changes.
- **Expect:** No crash; itinerary stable.
- **Result:** Pass / Fail / Blocked
- **Notes:**
