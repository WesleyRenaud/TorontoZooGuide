# ITIN-02 — Empty finish and clear

**Preconditions:** Clear any existing itinerary. Open `itinerary.html`.

**Date under test:** Any valid future date.

**Cleanup:** End with empty itinerary.

---

## Step 1 — Open builder with no items

- **Do:** Start the wizard and advance through steps without selecting animals/attractions/talks/encounters/transport.
- **Expect:** Wizard allows advancing with empty selections.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Finish empty

- **Do:** Click **Finish**.
- **Expect:** **No Items Selected** (or equivalent) blocks a successful empty itinerary.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Acknowledge empty state

- **Do:** Dismiss the empty-finish message.
- **Expect:** Back in builder; can still edit.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Add one animal

- **Do:** Add ≥1 animal on **Add Animals**.
- **Expect:** Animal is selected.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Finish with item

- **Do:** Click **Finish**.
- **Expect:** Itinerary saves/builds successfully.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Clear itinerary

- **Do:** Click **Clear**.
- **Expect:** **Clear Itinerary?** confirmation appears with the remove-all message.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Confirm clear

- **Do:** Confirm the clear.
- **Expect:** Itinerary returns to empty state.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Wizard usable again

- **Do:** Open **Edit Itinerary** / **Build Itinerary** again.
- **Expect:** Wizard starts cleanly (e.g. **Set Visit Date**).
- **Result:** Pass / Fail / Blocked
- **Notes:**
