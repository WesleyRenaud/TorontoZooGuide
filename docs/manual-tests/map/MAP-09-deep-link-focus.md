# MAP-09 — Deep link focus

**Preconditions:** Know a seed species (+ optional exhibit), e.g. `African Lion` / Africa Savanna. URL-encode spaces as needed.

**Date under test:** N/A (focus query).

**Cleanup:** End on plain `map.html` without query.

---

## Step 1 — Open focus URL

- **Do:** Open `map.html?focus=African%20Lion` (adjust species) and optional `&exhibit=...`.
- **Expect:** Page loads and attempts focus.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Pan/focus target

- **Do:** Observe map motion/highlight.
- **Expect:** Map pans/focuses toward the target marker.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Filter includes Animals

- **Do:** Check Filter.
- **Expect:** **Animals** is checked (auto-added if needed).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Tooltip or highlight

- **Do:** Observe target marker.
- **Expect:** Tooltip and/or highlight on the focused animal.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Query stripped

- **Do:** Inspect the address bar after focus completes.
- **Expect:** Focus query params removed via history replace.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Refresh clean

- **Do:** Reload the cleaned URL.
- **Expect:** Normal map load without forced focus.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Invalid focus

- **Do:** Open `map.html?focus=NotARealSpecies123`.
- **Expect:** Fails gracefully (no crash); map still usable.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Bottom nav after focus

- **Do:** Use bottom nav to Itinerary then back to Map.
- **Expect:** Navigation still works.
- **Result:** Pass / Fail / Blocked
- **Notes:**
