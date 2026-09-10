# CON-01 — Animal off/on display

**Preconditions:** Seeded DB. Open `console-operations.html`. Pick an outdoor animal guests can find on the map (e.g. **Raccoon** / **Canadian Domain**).

**Date under test:** **D** = a specific future date (record YYYY-MM-DD). Use D on map and itinerary verifies.

**Cleanup:** End with animal **on display** for D (run **Set animal as on display** if needed).

---

## Step 1 — Open off-display op

- **Do:** Select **Set animal as off display**.
- **Expect:** Form opens with species/exhibit fields.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Choose species/exhibit

- **Do:** Autocomplete species + exhibit.
- **Expect:** Valid pair selected.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Scope outdoor only

- **Do:** Set viewing scope to **Outdoor only**.
- **Expect:** Scope saved in the form.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Date range + reason

- **Do:** Set start ≤ D (**Last day** blank or ≥ D). Enter **Reason**.
- **Expect:** Fields valid; blank **Last day** means until manually on-display.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Submit off display

- **Do:** Submit the form.
- **Expect:** Success status like “{species} in {exhibit} was set as off display.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Map without include

- **Do:** Open `map.html`, **Specific Map**, date D. Leave **Include off display animals** unchecked.
- **Expect:** Animal absent or not shown as normally on-display (per product rules).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Map with include

- **Do:** Enable **Include off display animals**.
- **Expect:** Animal appears and/or off-display banner/message is shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Itinerary confirm

- **Do:** On `itinerary.html` for date D, try adding the animal (enable **Include off-display animals** if needed).
- **Expect:** Off-display / low-likelihood confirm appears, or animal listing reflects off-display — note which.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Set on display

- **Do:** In console, open **Set animal as on display** for the same species/exhibit/scope.
- **Expect:** Form accepts the pair.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Submit on display

- **Do:** Submit.
- **Expect:** Success status like “… was set as on display.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Map restored

- **Do:** On map for D with include-off-display **off**.
- **Expect:** Animal shows as a normal on-display marker again.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Cleanup confirmed

- **Do:** Confirm no leftover off-display for D.
- **Expect:** Guest map/itinerary behave as on-display.
- **Result:** Pass / Fail / Blocked
- **Notes:**
