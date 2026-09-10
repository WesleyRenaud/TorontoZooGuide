# CON-08 — Attraction closed / override / schedule / hours

**Preconditions:** Console open. Pick a named attraction with hours (e.g. Conservation Carousel or Zoomobile-related attraction).

**Date under test:** **D** = future date used for closed + itinerary checks.

**Cleanup:** Restore open state and sensible hours; remove test closures/overrides.

---

## Step 1 — Set attraction hours

- **Do:** Open **Set attraction hours**. Set weekday and weekend/holiday start/end within zoo hours.
- **Expect:** Form validates.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Submit hours

- **Do:** Submit.
- **Expect:** Success “{name} attraction hours were saved.”
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Itinerary hours snap

- **Do:** On itinerary for a day those hours apply, schedule the attraction outside its open window.
- **Expect:** UI snaps to nearest valid time or warns — note which.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Set attraction closed

- **Do:** Open **Set attraction as closed** for range covering D + message.
- **Expect:** Submit success closed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Map closed

- **Do:** Map on D with **Include closed attractions** unchecked then checked.
- **Expect:** Hidden/closed without include; visible + message with include.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Itinerary closed confirm

- **Do:** Try adding the attraction on D.
- **Expect:** **Attraction May Be Closed** / closed confirm appears.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Override or reopen

- **Do:** Use **Create attraction closure override** or set open / end closure so D is effectively open.
- **Expect:** Success status.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Opening schedule

- **Do:** Open **Set attraction opening schedule**; set a weekly pattern.
- **Expect:** Saves, or **Schedule conflict** dialog if overlapping (**Trim Old Schedules** / **Delete Old Schedules**).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Resolve overlap if shown

- **Do:** If overlap dialog appears, choose Trim or Delete and confirm.
- **Expect:** Schedule saves; note choice.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Map open state

- **Do:** Map on D.
- **Expect:** Attraction appears open/normal without needing include-closed.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 11 — Hours still valid

- **Do:** Spot-check itinerary scheduling still respects hours.
- **Expect:** Snap/hours behavior still coherent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 12 — Cleanup

- **Do:** Remove test closure/override; leave attraction open.
- **Expect:** Guest map clean for D.
- **Result:** Pass / Fail / Blocked
- **Notes:**
