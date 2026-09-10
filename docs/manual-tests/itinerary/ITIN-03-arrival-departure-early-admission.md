# ITIN-03 — Arrival, departure, early admission

**Preconditions:** Saved itinerary with ≥1 item (ITIN-01). Open Day Planner / time controls.

**Date under test:** Itinerary visit date.

**Cleanup:** Leave valid arrival/departure; Early Admission off unless you intend otherwise.

---

## Step 1 — Valid times

- **Do:** Set a sensible arrival before departure.
- **Expect:** Times accepted; no blocking validation.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Invalid order

- **Do:** Set departure before arrival.
- **Expect:** Validation bubble/error on arrival/departure.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Short visit

- **Do:** Set arrival and departure equal or nearly equal.
- **Expect:** Short-visit handling appears (message or constraint) — note behavior.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Fix window

- **Do:** Restore a valid multi-hour window.
- **Expect:** Validation clears; schedule usable.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Enable Early Admission

- **Do:** Turn on **Early Admission**.
- **Expect:** **Early Admission Hours** / membership-sensory confirmation appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Cancel early admission

- **Do:** Cancel/dismiss the confirmation.
- **Expect:** Early Admission not applied (or reverts) — note.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Confirm early admission

- **Do:** Enable again and confirm membership/sensory requirements.
- **Expect:** Early Admission applied.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Times after EA

- **Do:** Check arrival bounds after Early Admission.
- **Expect:** Times adjust or flag as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Schedule still coherent

- **Do:** View Day Planner pills if any.
- **Expect:** No crash; timeline still coherent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Toggle EA off

- **Do:** Disable Early Admission if possible.
- **Expect:** Returns to standard hours behavior.
- **Result:** Pass / Fail / Blocked
- **Notes:**
