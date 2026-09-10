# MAP-05 — Tooltips and species overlay

**Preconditions:** Animals filter on. Know a searchable species (e.g. **African Lion**).

**Date under test:** Specific Map date where the species is shown.

**Cleanup:** Close any open overlay/tooltip.

---

## Step 1 — Hover tooltip

- **Do:** Hover an animal marker.
- **Expect:** Hover tooltip (`#hoverTooltip`) appears with identifying text.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Click tooltip

- **Do:** Click the animal marker.
- **Expect:** Click tooltip (`#tooltip`) opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Tooltip essentials

- **Do:** Read the click tooltip.
- **Expect:** Shows species name and exhibit/essentials (likelihood line may appear).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — More Info

- **Do:** Click **More Info** (or equivalent) from the tooltip.
- **Expect:** Species overlay (`#speciesOverlay`) opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Overlay content

- **Do:** Inspect overlay content.
- **Expect:** Detail content loads (not blank/error-only).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Close overlay

- **Do:** Click the overlay close control.
- **Expect:** Overlay hides.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Amenity or pavilion tooltip

- **Do:** Enable **Restaurants** or **Pavilions**; click a non-animal marker.
- **Expect:** Type-appropriate tooltip appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Dismiss tooltip

- **Do:** Click empty map or dismiss control.
- **Expect:** Tooltip closes.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Replace tooltip

- **Do:** Quickly click another marker.
- **Expect:** Tooltip content switches cleanly to the new target.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Hover after click

- **Do:** Hover a different marker after dismissing click tooltip.
- **Expect:** Hover tooltip still works.
- **Result:** Pass / Fail / Blocked
- **Notes:**
