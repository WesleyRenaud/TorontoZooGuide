# MAP-10 — Narrow layout smoke

**Preconditions:** Open `map.html`. Use DevTools responsive mode ≈720px width (or slightly below).

**Date under test:** Specific Map.

**Cleanup:** Restore desktop width.

---

## Step 1 — Resize

- **Do:** Set viewport width to ~720px.
- **Expect:** Layout reflows; page still loads.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Explore usable

- **Do:** Scroll/interact with Explore.
- **Expect:** Explore is usable or scrollable (not completely inaccessible).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Banners

- **Do:** If banners show, read them.
- **Expect:** Banners stack/readable at narrow width.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Tooltip not off-screen

- **Do:** Click an animal marker.
- **Expect:** Tooltip mostly on-screen / usable.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Search usable

- **Do:** Use animal search.
- **Expect:** Can type and see results.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Pan/zoom

- **Do:** Pan and zoom the map.
- **Expect:** Still works.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Date preset control

- **Do:** Change map preset or date.
- **Expect:** Controls remain usable.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Restore desktop

- **Do:** Return to a wide viewport.
- **Expect:** Layout recovers without requiring reload (note if reload needed).
- **Result:** Pass / Fail / Blocked
- **Notes:**
