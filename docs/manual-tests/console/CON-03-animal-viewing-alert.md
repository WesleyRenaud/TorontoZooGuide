# CON-03 — Animal viewing alert

**Preconditions:** Console open. Species visible on map.

**Date under test:** **D** in alert range.

**Cleanup:** **Remove animal viewing alert**.

---

## Step 1 — Set alert

- **Do:** Open **Set animal viewing alert**; species/exhibit, dates covering D, alert text.
- **Expect:** Form valid.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Submit alert

- **Do:** Submit.
- **Expect:** Success “… was given a viewing alert.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Map shows alert

- **Do:** Map tooltip/banner for that animal on D.
- **Expect:** Alert text shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Remove alert

- **Do:** Open **Remove animal viewing alert**.
- **Expect:** Form OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Submit remove

- **Do:** Submit.
- **Expect:** Success “Viewing alert removed…”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Map clear

- **Do:** Map on D.
- **Expect:** Alert gone.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Map-only impact OK

- **Do:** No itinerary required for Pass if map verified.
- **Expect:** Noted.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Cleanup

- **Do:** Confirm no alert remains.
- **Expect:** Clean.
- **Result:** Pass / Fail / Blocked
- **Notes:**
