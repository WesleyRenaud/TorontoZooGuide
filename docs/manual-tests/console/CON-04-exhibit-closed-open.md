# CON-04 — Exhibit closed/open

**Preconditions:** Console open. Choose an exhibit with a visible map overlay (e.g. a pavilion/domain used by several animals).

**Date under test:** **D** = future date in the closure range.

**Cleanup:** End with exhibit **open** for D.

---

## Step 1 — Open close exhibit

- **Do:** Select **Set exhibit as closed**.
- **Expect:** Form opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Fill closure

- **Do:** Pick exhibit, date range covering D, guest message.
- **Expect:** Fields valid.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Submit closed

- **Do:** Submit.
- **Expect:** Success “{exhibit} was set as closed.” (or equivalent).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Map overlay

- **Do:** Open map on Specific Map date D.
- **Expect:** Closed-exhibit overlay/styling appears for that exhibit.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — Itinerary impact

- **Do:** Build/edit itinerary for D involving animals in that exhibit.
- **Expect:** Animals constrained, warned, or harder to plan as designed — note behavior.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Open exhibit op

- **Do:** Select **Set exhibit as open**.
- **Expect:** Form opens.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Submit open

- **Do:** Re-open for range covering D.
- **Expect:** Success open status.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Overlay gone

- **Do:** Refresh map for D.
- **Expect:** Closed overlay absent.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — Itinerary normal

- **Do:** Recheck itinerary animal availability for that exhibit on D.
- **Expect:** Normal selection resumes.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Cleanup

- **Do:** Confirm exhibit open on D.
- **Expect:** No leftover closure.
- **Result:** Pass / Fail / Blocked
- **Notes:**
