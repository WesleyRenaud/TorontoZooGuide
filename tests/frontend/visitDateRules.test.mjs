import assert from 'node:assert/strict';
import test from 'node:test';

import {
   addLocalCalendarDays,
   clampToAllowedVisitDate,
   getDay,
   getMaxDate,
   getMonth,
   getToday,
   isoDateToMonFirstDow,
   isAfterMaxDate,
   isBeforeToday,
   isLocalTimeAtOrPastZooClose,
   isWithinNextNDays,
   normalizeDate,
   parseLocalDate,
   parseZooClockTimeMinutes,
   toISODate,
} from '../../scripts/visitDates/visitDateRules.js';

test('parses a valid visit date at local noon', () => {
   const visitDate = parseLocalDate('2026-06-15');

   assert.equal(Number.isNaN(visitDate.getTime()), false);
   assert.equal(visitDate.getFullYear(), 2026);
   assert.equal(visitDate.getMonth(), 5);
   assert.equal(visitDate.getDate(), 15);
   assert.equal(visitDate.getHours(), 12);
});

test('rejects malformed and impossible visit dates', () => {
   assert.equal(Number.isNaN(parseLocalDate('2026-02-30').getTime()), true);
   assert.equal(Number.isNaN(parseLocalDate('2026-13-01').getTime()), true);
   assert.equal(Number.isNaN(parseLocalDate('African Rainforest').getTime()), true);
});

test('formats visit dates for API and calendar display', () => {
   assert.equal(toISODate(new Date(2026, 5, 15, 23, 59)), '2026-06-15');
   assert.equal(getMonth('2026-06-15'), 'JUN');
   assert.equal(getDay('2026-06-15'), 15);
   assert.equal(getMonth('bad-date'), null);
   assert.equal(getDay('bad-date'), null);
   assert.equal(isoDateToMonFirstDow('2026-06-15'), 1);
   assert.equal(isoDateToMonFirstDow('2026-06-21'), 7);
   assert.equal(isoDateToMonFirstDow('bad-date'), 1);
   assert.equal(isoDateToMonFirstDow(), isoDateToMonFirstDow(toISODate(getToday())));
});

test('normalizes and validates visit date range boundaries', () => {
   const today = getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const afterMax = new Date(getMaxDate(2));
   afterMax.setDate(afterMax.getDate() + 1);

   assert.equal(toISODate(normalizeDate(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59))), toISODate(today));
   assert.equal(normalizeDate('bad-date'), null);
   assert.equal(isBeforeToday(yesterday), true);
   assert.equal(isBeforeToday('bad-date'), false);
   assert.equal(isAfterMaxDate(afterMax, 2), true);
   assert.equal(isAfterMaxDate('bad-date', 2), false);
   assert.equal(isWithinNextNDays(toISODate(tomorrow), 2), true);
   assert.equal(isWithinNextNDays(toISODate(afterMax), 2), false);
   assert.equal(isWithinNextNDays('bad-date', 2), false);
});

test('clamps visit dates to the allowed range', () => {
   const today = getToday();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const maxDate = getMaxDate(2);
   const afterMax = new Date(maxDate);
   afterMax.setDate(maxDate.getDate() + 1);
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   assert.equal(toISODate(clampToAllowedVisitDate('bad-date', 2)), toISODate(today));
   assert.equal(toISODate(clampToAllowedVisitDate(yesterday, 2)), toISODate(today));
   assert.equal(toISODate(clampToAllowedVisitDate(afterMax, 2)), toISODate(maxDate));
   assert.equal(toISODate(clampToAllowedVisitDate(tomorrow, 2)), toISODate(tomorrow));
});

test('clamps visit dates using a custom earliest floor', () => {
   const today = getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   assert.equal(
      toISODate(clampToAllowedVisitDate(yesterday, 2, tomorrow)),
      toISODate(tomorrow)
   );
   assert.equal(
      toISODate(clampToAllowedVisitDate(today, 2, tomorrow)),
      toISODate(tomorrow)
   );
   assert.equal(
      toISODate(clampToAllowedVisitDate(tomorrow, 2, tomorrow)),
      toISODate(tomorrow)
   );
});

test('parses zoo clock strings to minutes from midnight', () => {
   assert.equal(parseZooClockTimeMinutes('19:00'), 19 * 60);
   assert.equal(parseZooClockTimeMinutes('7:00 PM'), 19 * 60);
   assert.equal(parseZooClockTimeMinutes('12:00 AM'), 0);
   assert.equal(parseZooClockTimeMinutes('12:00 PM'), 12 * 60);
   assert.equal(parseZooClockTimeMinutes(''), null);
   assert.equal(parseZooClockTimeMinutes('25:00'), null);
});

test('detects local wall-clock at or after zoo close', () => {
   const closeAtSevenPm = new Date(2026, 4, 10, 19, 0, 0, 0);
   const justBeforeClose = new Date(2026, 4, 10, 18, 59, 0, 0);

   assert.equal(isLocalTimeAtOrPastZooClose('19:00', closeAtSevenPm), true);
   assert.equal(isLocalTimeAtOrPastZooClose('19:00', justBeforeClose), false);
   assert.equal(isLocalTimeAtOrPastZooClose(null, closeAtSevenPm), false);
});

test('adds local calendar days from a local-noon anchor', () => {
   const anchor = parseLocalDate('2026-06-15');
   const next = addLocalCalendarDays(anchor, 1);
   const prev = addLocalCalendarDays(anchor, -1);

   assert.equal(toISODate(next), '2026-06-16');
   assert.equal(toISODate(prev), '2026-06-14');
});
