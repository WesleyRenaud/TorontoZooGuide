# CON-09 — Transportation station + current route

**Preconditions:** Console open. Zoomobile stations exist on map.

**Date under test:** **D** for station closure; route range covering D.

**Cleanup:** Stations open; restore prior transportation route if known.

---

## Step 1 — Close station

- **Do:** **Set transportation station as closed** for D.
- **Expect:** Success.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map station closed

- **Do:** Map D with Zoomobile route visible.
- **Expect:** Station closed/missing/messaged.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Open station

- **Do:** **Set transportation station as open**.
- **Expect:** Success.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Set Summer route

- **Do:** **Set current transportation route** — choose **Summer**, date range including D.
- **Expect:** Success “Transportation route was set to …”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Map summer

- **Do:** Map Explore → Summer/Current as applicable.
- **Expect:** Summer route layer/stations.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Set Winter route

- **Do:** Set route to **Winter** for a range.
- **Expect:** Success.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Map winter

- **Do:** Map shows winter route treatment.
- **Expect:** Winter differs from summer where designed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Itinerary transport

- **Do:** If itinerary transport options change with route, spot-check.
- **Expect:** Noted or N/A.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Restore route

- **Do:** Set route back to the previous/current intended season.
- **Expect:** Restored.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Cleanup stations

- **Do:** Confirm stations open on D.
- **Expect:** Open.
- **Result:** Pass / Fail / Blocked
- **Notes:**
