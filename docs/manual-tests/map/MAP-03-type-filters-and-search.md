# MAP-03 — Type filters and search

**Preconditions:** Open `map.html` on **Specific Map**. Pick a known seed animal (e.g. **African Lion** or **Raccoon**).

**Date under test:** Any Specific Map date where the chosen animal is in seed.

**Cleanup:** Re-check **Animals** in Filter before leaving.

---

## Step 1 — Animals checked by default

- **Do:** Open **Filter:** dropdown.
- **Expect:** **Animals** checkbox is checked; other types are unchecked by default.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Uncheck Animals

- **Do:** Uncheck **Animals**.
- **Expect:** Animal markers disappear from the map.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Recheck Animals

- **Do:** Check **Animals** again.
- **Expect:** Animal markers return.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Enable Restaurants

- **Do:** Check **Restaurants**.
- **Expect:** Restaurant markers appear (in addition to animals).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Disable Restaurants

- **Do:** Uncheck **Restaurants**.
- **Expect:** Restaurant markers hide; animals remain.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Spot-check another type

- **Do:** Briefly enable **Pavilions** or **Attractions**, then disable.
- **Expect:** Corresponding markers show/hide without breaking Animals.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Search query

- **Do:** In **Search animals** / Search… field, type part of the known species name.
- **Expect:** Results list under the search field populates.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Select search result

- **Do:** Click a search result.
- **Expect:** Map pans/focuses to that animal’s marker.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Focus feedback

- **Do:** Observe tooltip or highlight after selection.
- **Expect:** Click tooltip and/or focus styling appears for the target.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Clear via uncheck Animals

- **Do:** Uncheck **Animals** while search results are visible.
- **Expect:** Search results clear or animal results are removed as designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Restore search

- **Do:** Recheck **Animals** and search again.
- **Expect:** Search works again and can focus a marker.
- **Result:** Pass / Fail / Blocked
- **Notes:**
