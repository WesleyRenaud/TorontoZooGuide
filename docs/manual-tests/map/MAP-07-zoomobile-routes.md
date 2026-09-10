# MAP-07 — Zoomobile routes

**Preconditions:** Explore panel visible with transportation route radios.

**Date under test:** Specific Map (or Current route season).

**Cleanup:** Set route control back to **None**.

---

## Step 1 — None

- **Do:** Select **None** under Zoomobile/transportation routes.
- **Expect:** No Zoomobile route SVG/arrows shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Current Route

- **Do:** Select **Current Route**.
- **Expect:** Route and/or stations appear per current season rules.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Summer Route

- **Do:** Select **Summer Route** (or summer-style option).
- **Expect:** Summer route layer/markers visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Winter Route

- **Do:** Select **Winter Route**.
- **Expect:** Winter route layer/markers visible; differs from summer where designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Station tooltip

- **Do:** Click a Zoomobile station marker.
- **Expect:** Tooltip shows station info (e.g. Zoomobile Station naming).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Back to None

- **Do:** Select **None** again.
- **Expect:** Route layers clear.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Animals still present

- **Do:** Confirm **Animals** still checked.
- **Expect:** Animal markers still present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — No leftover arrows

- **Do:** Pan around former route areas.
- **Expect:** No orphaned route arrows/markers left behind.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Repeat Current once

- **Do:** Toggle Current → None once more.
- **Expect:** Still cleans up reliably.
- **Result:** Pass / Fail / Blocked
- **Notes:**
