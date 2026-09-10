# CON-13 — Updates CRUD

**Preconditions:** Console open.

**Date under test:** **D** inside update active range.

**Cleanup:** End update so it is inactive after test (or note leftover).

---

## Step 1 — Create update

- **Do:** **Create update** with **Title**, **Description**, **Type** (e.g. New Arrival), **Start date** covering D, optional **No longer applies on**.
- **Expect:** Success created.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 2 — Map Updates shows it

- **Do:** Map Explore → **Updates** on D.
- **Expect:** Update visible.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 3 — Edit update

- **Do:** **Edit update** description/type/end.
- **Expect:** Success edited.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 4 — Map reflects edit

- **Do:** Refresh Updates on D.
- **Expect:** Edited content shown.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 5 — End update

- **Do:** **End update** effective on/before D as designed.
- **Expect:** Success ended.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 6 — Map inactive

- **Do:** Updates on D.
- **Expect:** No longer listed as active (or ended treatment).
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 7 — Inside vs outside range

- **Do:** Before ending, flip map date inside/outside range once.
- **Expect:** Presence matches range.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 8 — Cleanup

- **Do:** Ensure test update ended.
- **Expect:** Clean enough for other suites.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 9 — No crash

- **Do:** Carousel/collapse still works.
- **Expect:** OK.
- **Result:** Pass / Fail / Blocked
- **Notes:**

## Step 10 — Pass

- **Do:** CRUD + map verify done.
- **Expect:** Pass.
- **Result:** Pass / Fail / Blocked
- **Notes:**
