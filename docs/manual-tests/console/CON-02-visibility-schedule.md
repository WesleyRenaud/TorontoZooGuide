# CON-02 — Visibility schedule

**Preconditions:** Console open. Pick species/exhibit used on map.

**Date under test:** **D** inside the visibility schedule date range.

**Cleanup:** Run **Remove visibility schedule** before ending.

---

## Step 1 — Open set schedule

- **Do:** Select **Set animal visibility schedule**.
- **Expect:** Form opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Fill window

- **Do:** Set daily viewing start/end, **Schedule start date** / **Last day of schedule** covering D, **Message**.
- **Expect:** Fields valid.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Submit

- **Do:** Submit.
- **Expect:** Success “… viewing schedule updated.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Map limited-viewing cue

- **Do:** Map on D; find animal marker badge/limited-viewing styling.
- **Expect:** Limited-viewing cue present.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Tooltip/message

- **Do:** Open tooltip.
- **Expect:** Viewing message visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Itinerary window

- **Do:** On itinerary for D, schedule the animal inside vs outside the daily window if practical.
- **Expect:** Respects or warns — note behavior.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Remove schedule

- **Do:** Select **Remove visibility schedule** for same species/exhibit.
- **Expect:** Form OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Submit remove

- **Do:** Submit.
- **Expect:** Success “… no longer has a visibility schedule.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Map cue gone

- **Do:** Map on D.
- **Expect:** Limited-viewing cue gone.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Itinerary normal

- **Do:** Scheduling behaves without limited-window constraint.
- **Expect:** Normal.
- **Result:** Pass / Fail / Blocked
- **Notes:**
