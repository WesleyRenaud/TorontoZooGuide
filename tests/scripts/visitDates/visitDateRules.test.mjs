import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateRules } from '../../../scripts/visitDates/visitDateRules.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const referenceToday = makeNoonDate(2026, 5, 15);

test('Test_ParseLocalDate_TestValidIso_ExpectLocalNoon', () => {
   const visitDate = VisitDateRules.parseLocalDate('2026-06-15');

   assert.equal(Number.isNaN(visitDate.getTime()), false);
   assert.equal(visitDate.getFullYear(), 2026);
   assert.equal(visitDate.getMonth(), 5);
   assert.equal(visitDate.getDate(), 15);
   assert.equal(visitDate.getHours(), 12);
});

test('Test_ParseLocalDate_TestInvalidIso_ExpectInvalidDate', () => {
   assert.equal(Number.isNaN(VisitDateRules.parseLocalDate('2026-02-30').getTime()), true);
   assert.equal(Number.isNaN(VisitDateRules.parseLocalDate('2026-13-01').getTime()), true);
   assert.equal(Number.isNaN(VisitDateRules.parseLocalDate('African Rainforest').getTime()), true);
});

test('Test_FormatVisitDateHelpers_TestValidAndInvalid_ExpectDisplayValues', () => {
   assert.equal(VisitDateRules.toISODate(new Date(2026, 5, 15, 23, 59)), '2026-06-15');
   assert.equal(VisitDateRules.getMonth('2026-06-15'), 'JUN');
   assert.equal(VisitDateRules.getDay('2026-06-15'), 15);
   assert.equal(VisitDateRules.getYear('2026-06-15'), 2026);
   assert.equal(VisitDateRules.getMonth('bad-date'), null);
   assert.equal(VisitDateRules.getDay('bad-date'), null);
   assert.equal(VisitDateRules.getYear('bad-date'), null);
   assert.equal(VisitDateRules.isoDateToMonFirstDow('2026-06-15'), 1);
   assert.equal(VisitDateRules.isoDateToMonFirstDow('2026-06-21'), 7);
   assert.equal(VisitDateRules.isoDateToMonFirstDow('bad-date'), 1);
   assert.equal(VisitDateRules.isoDateToMonFirstDow(), VisitDateRules.isoDateToMonFirstDow(VisitDateRules.toISODate(VisitDateRules.getToday())));
});

test('Test_ResolveOptionalStartDate_TestProvidedOrBlank_ExpectKeptOrToday', () => {
   assert.equal(VisitDateRules.resolveOptionalStartDate('2026-06-20'), '2026-06-20');
   assert.equal(VisitDateRules.resolveOptionalStartDate(''), VisitDateRules.toISODate(VisitDateRules.getToday()));
   assert.equal(VisitDateRules.resolveOptionalStartDate(null), VisitDateRules.toISODate(VisitDateRules.getToday()));
});

test('Test_FormatLocalDateLongAndRange_TestVisitDates_ExpectFriendlyText', () => {
   assert.equal(VisitDateRules.formatLocalDateLong('2026-06-15'), 'June 15, 2026');
   assert.equal(VisitDateRules.formatLocalDateLong(''), '');
   assert.equal(VisitDateRules.formatLocalDateLong('bad-date'), '');
   assert.equal(
      VisitDateRules.formatLocalDateRange('2026-06-15', '2026-06-30'),
      'June 15, 2026 - June 30, 2026'
   );
   assert.equal(VisitDateRules.formatLocalDateRange('2026-06-15', null), 'June 15, 2026');
   assert.equal(VisitDateRules.formatLocalDateRange('', '2026-06-30'), '');
});

test('Test_VisitDateRangeBoundaries_TestRelativeToToday_ExpectValidated', () => {
   const today = VisitDateRules.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const afterMax = new Date(VisitDateRules.getMaxDate(2));
   afterMax.setDate(afterMax.getDate() + 1);

   assert.equal(VisitDateRules.toISODate(VisitDateRules.normalizeDate(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59))), VisitDateRules.toISODate(today));
   assert.equal(VisitDateRules.normalizeDate('bad-date'), null);
   assert.equal(VisitDateRules.isBeforeToday(yesterday), true);
   assert.equal(VisitDateRules.isBeforeToday('bad-date'), false);
   assert.equal(VisitDateRules.isAfterMaxDate(afterMax, 2), true);
   assert.equal(VisitDateRules.isAfterMaxDate('bad-date', 2), false);
   assert.equal(VisitDateRules.isWithinNextNDays(VisitDateRules.toISODate(tomorrow), 2), true);
   assert.equal(VisitDateRules.isWithinNextNDays(VisitDateRules.toISODate(afterMax), 2), false);
   assert.equal(VisitDateRules.isWithinNextNDays('bad-date', 2), false);
});

test('Test_VisitDateRangeBoundaries_TestReferenceToday_ExpectValidated', () => {
   const yesterday = makeNoonDate(2026, 5, 14);
   const tomorrow = makeNoonDate(2026, 5, 16);
   const afterMax = makeNoonDate(2026, 5, 18);

   assert.equal(VisitDateRules.isBeforeToday(yesterday, referenceToday), true);
   assert.equal(VisitDateRules.isBeforeToday(tomorrow, referenceToday), false);
   assert.equal(VisitDateRules.isAfterMaxDate(afterMax, 2, referenceToday), true);
   assert.equal(VisitDateRules.isAfterMaxDate(tomorrow, 2, referenceToday), false);
   assert.equal(VisitDateRules.isWithinNextNDays('2026-06-16', 2, referenceToday), true);
   assert.equal(VisitDateRules.isWithinNextNDays('2026-06-18', 2, referenceToday), false);
   assert.equal(
      VisitDateRules.toISODate(VisitDateRules.getMaxDate(2, referenceToday)),
      '2026-06-17'
   );
});

test('Test_ClampToAllowedVisitDate_TestOutOfRange_ExpectClamped', () => {
   const today = VisitDateRules.getToday();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const maxDate = VisitDateRules.getMaxDate(2);
   const afterMax = new Date(maxDate);
   afterMax.setDate(maxDate.getDate() + 1);
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   assert.equal(VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate('bad-date', 2)), VisitDateRules.toISODate(today));
   assert.equal(VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(yesterday, 2)), VisitDateRules.toISODate(today));
   assert.equal(VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(afterMax, 2)), VisitDateRules.toISODate(maxDate));
   assert.equal(VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(tomorrow, 2)), VisitDateRules.toISODate(tomorrow));
});

test('Test_ClampToAllowedVisitDate_TestCustomFloor_ExpectClamped', () => {
   const today = VisitDateRules.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   assert.equal(
      VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(yesterday, 2, tomorrow)),
      VisitDateRules.toISODate(tomorrow)
   );
   assert.equal(
      VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(today, 2, tomorrow)),
      VisitDateRules.toISODate(tomorrow)
   );
   assert.equal(
      VisitDateRules.toISODate(VisitDateRules.clampToAllowedVisitDate(tomorrow, 2, tomorrow)),
      VisitDateRules.toISODate(tomorrow)
   );
});

test('Test_ParseZooClockTimeMinutes_TestClockStrings_ExpectMinutes', () => {
   assert.equal(VisitDateRules.parseZooClockTimeMinutes('19:00'), 19 * 60);
   assert.equal(VisitDateRules.parseZooClockTimeMinutes('7:00 PM'), 19 * 60);
   assert.equal(VisitDateRules.parseZooClockTimeMinutes('12:00 AM'), 0);
   assert.equal(VisitDateRules.parseZooClockTimeMinutes('12:00 PM'), 12 * 60);
   assert.equal(VisitDateRules.parseZooClockTimeMinutes(''), null);
   assert.equal(VisitDateRules.parseZooClockTimeMinutes('25:00'), null);
});

test('Test_NormalizeScheduleTime_TestClockStrings_ExpectDisplay', () => {
   assert.equal(VisitDateRules.normalizeScheduleTime('1:00 PM'), '1:00 PM');
   assert.equal(VisitDateRules.normalizeScheduleTime('15:30'), '3:30 PM');
   assert.equal(VisitDateRules.normalizeScheduleTime('10:00'), '10:00 AM');
   assert.equal(VisitDateRules.normalizeScheduleTime(''), null);
   assert.equal(VisitDateRules.normalizeScheduleTime('not-a-time'), null);
   assert.equal(VisitDateRules.normalizeItineraryScheduleTime('1:00 PM'), '1:00 PM');
});

test('Test_IsLocalTimeAtOrPastZooClose_TestWallClock_ExpectDetected', () => {
   const closeAtSevenPm = new Date(2026, 4, 10, 19, 0, 0, 0);
   const justBeforeClose = new Date(2026, 4, 10, 18, 59, 0, 0);

   assert.equal(VisitDateRules.isLocalTimeAtOrPastZooClose('19:00', closeAtSevenPm), true);
   assert.equal(VisitDateRules.isLocalTimeAtOrPastZooClose('19:00', justBeforeClose), false);
   assert.equal(VisitDateRules.isLocalTimeAtOrPastZooClose(null, closeAtSevenPm), false);
});

test('Test_AddLocalCalendarDays_TestNoonAnchor_ExpectShifted', () => {
   const anchor = VisitDateRules.parseLocalDate('2026-06-15');
   const next = VisitDateRules.addLocalCalendarDays(anchor, 1);
   const prev = VisitDateRules.addLocalCalendarDays(anchor, -1);

   assert.equal(VisitDateRules.toISODate(next), '2026-06-16');
   assert.equal(VisitDateRules.toISODate(prev), '2026-06-14');
});

test('Test_IsVisitDateBeforeEarliestFloor_TestMapFloor_ExpectMatched', () => {
   const today = makeNoonDate(2026, 5, 15);
   const tomorrow = makeNoonDate(2026, 5, 16);

   assert.equal(VisitDateRules.isVisitDateBeforeEarliestFloor('2026-06-15', today), false);
   assert.equal(VisitDateRules.isVisitDateBeforeEarliestFloor('2026-06-15', tomorrow), true);
   assert.equal(VisitDateRules.isVisitDateBeforeEarliestFloor('2026-06-14', today), true);
   assert.equal(VisitDateRules.isVisitDateBeforeEarliestFloor('2026-06-20', today), false);
   assert.equal(VisitDateRules.isVisitDateBeforeEarliestFloor('  ', today), false);
});
