import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { VisitDateRuleHelper } from '../../../scripts/visitDates/visitDateRuleHelper.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const referenceToday = makeNoonDate(2026, 5, 15);

test('Test_ParseLocalDate_TestValidIso_ExpectLocalNoon', () => {
   const visitDate = VisitDateValidator.parseLocalDate('2026-06-15');

   assert.equal(Number.isNaN(visitDate.getTime()), false);
   assert.equal(visitDate.getFullYear(), 2026);
   assert.equal(visitDate.getMonth(), 5);
   assert.equal(visitDate.getDate(), 15);
   assert.equal(visitDate.getHours(), 12);
});

test('Test_ParseLocalDate_TestInvalidIso_ExpectInvalidDate', () => {
   assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('2026-02-30').getTime()), true);
   assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('2026-13-01').getTime()), true);
   assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('African Rainforest').getTime()), true);
});

test('Test_FormatVisitDateHelpers_TestValidAndInvalid_ExpectDisplayValues', () => {
   assert.equal(VisitDateValidator.toISODate(new Date(2026, 5, 15, 23, 59)), '2026-06-15');
   assert.equal(VisitDateValidator.getMonth('2026-06-15'), 'JUN');
   assert.equal(VisitDateValidator.getDay('2026-06-15'), 15);
   assert.equal(VisitDateValidator.getYear('2026-06-15'), 2026);
   assert.equal(VisitDateValidator.getMonth('bad-date'), null);
   assert.equal(VisitDateValidator.getDay('bad-date'), null);
   assert.equal(VisitDateValidator.getYear('bad-date'), null);
   assert.equal(VisitDateValidator.isoDateToMonFirstDow('2026-06-15'), 1);
   assert.equal(VisitDateValidator.isoDateToMonFirstDow('2026-06-21'), 7);
   assert.equal(VisitDateValidator.isoDateToMonFirstDow('bad-date'), 1);
   assert.equal(VisitDateValidator.isoDateToMonFirstDow(), VisitDateValidator.isoDateToMonFirstDow(VisitDateValidator.toISODate(VisitDateValidator.getToday())));
});

test('Test_ResolveOptionalStartDate_TestProvidedOrBlank_ExpectKeptOrToday', () => {
   assert.equal(VisitDateValidator.resolveOptionalStartDate('2026-06-20'), '2026-06-20');
   assert.equal(VisitDateValidator.resolveOptionalStartDate(''), VisitDateValidator.toISODate(VisitDateValidator.getToday()));
   assert.equal(VisitDateValidator.resolveOptionalStartDate(null), VisitDateValidator.toISODate(VisitDateValidator.getToday()));
});

test('Test_FormatLocalDateLongAndRange_TestVisitDates_ExpectFriendlyText', () => {
   assert.equal(VisitDateValidator.formatLocalDateLong('2026-06-15'), 'June 15, 2026');
   assert.equal(VisitDateValidator.formatLocalDateLong(''), '');
   assert.equal(VisitDateValidator.formatLocalDateLong('bad-date'), '');
   assert.equal(
      VisitDateValidator.formatLocalDateRange('2026-06-15', '2026-06-30'),
      'June 15, 2026 - June 30, 2026'
   );
   assert.equal(VisitDateValidator.formatLocalDateRange('2026-06-15', null), 'June 15, 2026');
   assert.equal(VisitDateValidator.formatLocalDateRange('', '2026-06-30'), '');
});

test('Test_VisitDateRangeBoundaries_TestRelativeToToday_ExpectValidated', () => {
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const afterMax = new Date(VisitDateValidator.getMaxDate(2));
   afterMax.setDate(afterMax.getDate() + 1);

   assert.equal(VisitDateValidator.toISODate(VisitDateValidator.normalizeDate(new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59))), VisitDateValidator.toISODate(today));
   assert.equal(VisitDateValidator.normalizeDate('bad-date'), null);
   assert.equal(VisitDateValidator.isBeforeToday(yesterday), true);
   assert.equal(VisitDateValidator.isBeforeToday('bad-date'), false);
   assert.equal(VisitDateValidator.isAfterMaxDate(afterMax, 2), true);
   assert.equal(VisitDateValidator.isAfterMaxDate('bad-date', 2), false);
   assert.equal(VisitDateValidator.isWithinNextNDays(VisitDateValidator.toISODate(tomorrow), 2), true);
   assert.equal(VisitDateValidator.isWithinNextNDays(VisitDateValidator.toISODate(afterMax), 2), false);
   assert.equal(VisitDateValidator.isWithinNextNDays('bad-date', 2), false);
});

test('Test_VisitDateRangeBoundaries_TestReferenceToday_ExpectValidated', () => {
   const yesterday = makeNoonDate(2026, 5, 14);
   const tomorrow = makeNoonDate(2026, 5, 16);
   const afterMax = makeNoonDate(2026, 5, 18);

   assert.equal(VisitDateValidator.isBeforeToday(yesterday, referenceToday), true);
   assert.equal(VisitDateValidator.isBeforeToday(tomorrow, referenceToday), false);
   assert.equal(VisitDateValidator.isAfterMaxDate(afterMax, 2, referenceToday), true);
   assert.equal(VisitDateValidator.isAfterMaxDate(tomorrow, 2, referenceToday), false);
   assert.equal(VisitDateValidator.isWithinNextNDays('2026-06-16', 2, referenceToday), true);
   assert.equal(VisitDateValidator.isWithinNextNDays('2026-06-18', 2, referenceToday), false);
   assert.equal(
      VisitDateValidator.toISODate(VisitDateValidator.getMaxDate(2, referenceToday)),
      '2026-06-17'
   );
});

test('Test_ClampToAllowedVisitDate_TestOutOfRange_ExpectClamped', () => {
   const today = VisitDateValidator.getToday();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);
   const maxDate = VisitDateValidator.getMaxDate(2);
   const afterMax = new Date(maxDate);
   afterMax.setDate(maxDate.getDate() + 1);
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   assert.equal(VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate('bad-date', 2)), VisitDateValidator.toISODate(today));
   assert.equal(VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(yesterday, 2)), VisitDateValidator.toISODate(today));
   assert.equal(VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(afterMax, 2)), VisitDateValidator.toISODate(maxDate));
   assert.equal(VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(tomorrow, 2)), VisitDateValidator.toISODate(tomorrow));
});

test('Test_ClampToAllowedVisitDate_TestCustomFloor_ExpectClamped', () => {
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   assert.equal(
      VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(yesterday, 2, tomorrow)),
      VisitDateValidator.toISODate(tomorrow)
   );
   assert.equal(
      VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(today, 2, tomorrow)),
      VisitDateValidator.toISODate(tomorrow)
   );
   assert.equal(
      VisitDateValidator.toISODate(VisitDateValidator.clampToAllowedVisitDate(tomorrow, 2, tomorrow)),
      VisitDateValidator.toISODate(tomorrow)
   );
});

test('Test_ParseZooClockTimeMinutes_TestClockStrings_ExpectMinutes', () => {
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('19:00'), 19 * 60);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('7:00 PM'), 19 * 60);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('12:00 AM'), 0);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('12:00 PM'), 12 * 60);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes(''), null);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('25:00'), null);
});

test('Test_NormalizeScheduleTime_TestClockStrings_ExpectDisplay', () => {
   assert.equal(VisitDateValidator.normalizeScheduleTime('1:00 PM'), '1:00 PM');
   assert.equal(VisitDateValidator.normalizeScheduleTime('15:30'), '3:30 PM');
   assert.equal(VisitDateValidator.normalizeScheduleTime('10:00'), '10:00 AM');
   assert.equal(VisitDateValidator.normalizeScheduleTime(''), null);
   assert.equal(VisitDateValidator.normalizeScheduleTime('not-a-time'), null);
   assert.equal(VisitDateValidator.normalizeItineraryScheduleTime('1:00 PM'), '1:00 PM');
});

test('Test_IsLocalTimeAtOrPastZooClose_TestWallClock_ExpectDetected', () => {
   const closeAtSevenPm = new Date(2026, 4, 10, 19, 0, 0, 0);
   const justBeforeClose = new Date(2026, 4, 10, 18, 59, 0, 0);

   assert.equal(VisitDateValidator.isLocalTimeAtOrPastZooClose('19:00', closeAtSevenPm), true);
   assert.equal(VisitDateValidator.isLocalTimeAtOrPastZooClose('19:00', justBeforeClose), false);
   assert.equal(VisitDateValidator.isLocalTimeAtOrPastZooClose(null, closeAtSevenPm), false);
});

test('Test_AddLocalCalendarDays_TestNoonAnchor_ExpectShifted', () => {
   const anchor = VisitDateValidator.parseLocalDate('2026-06-15');
   const next = VisitDateValidator.addLocalCalendarDays(anchor, 1);
   const prev = VisitDateValidator.addLocalCalendarDays(anchor, -1);

   assert.equal(VisitDateValidator.toISODate(next), '2026-06-16');
   assert.equal(VisitDateValidator.toISODate(prev), '2026-06-14');
});

test('Test_IsVisitDateBeforeEarliestFloor_TestMapFloor_ExpectMatched', () => {
   const today = makeNoonDate(2026, 5, 15);
   const tomorrow = makeNoonDate(2026, 5, 16);

   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('2026-06-15', today), false);
   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('2026-06-15', tomorrow), true);
   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('2026-06-14', today), true);
   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('2026-06-20', today), false);
   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('  ', today), false);
});

test('Test_ParseLocalDate_TestNonIntegerParts_ExpectInvalidDate', () => {
   assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('2026-6.5-15').getTime()), true);
   assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('2026-06-1a').getTime()), true);
});

test('Test_ParseLocalDate_TestInvalidParsedDate_ExpectInvalidDate', () => {
   const original = VisitDateRuleHelper.isValidDate;
   VisitDateRuleHelper.isValidDate = () => false;

   try {
      assert.equal(Number.isNaN(VisitDateValidator.parseLocalDate('2026-06-15').getTime()), true);
   } finally {
      VisitDateRuleHelper.isValidDate = original;
   }
});

test('Test_ParseZooClockTimeMinutes_TestInvalidDisplayHours_ExpectNull', () => {
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('0:00 AM'), null);
   assert.equal(VisitDateValidator.parseZooClockTimeMinutes('13:00 PM'), null);
});

test('Test_AddLocalCalendarDays_TestInvalidBase_ExpectToday', () => {
   const invalid = VisitDateValidator.parseLocalDate('2026-02-30');
   const shifted = VisitDateValidator.addLocalCalendarDays(invalid, 1);

   assert.equal(
      VisitDateValidator.toISODate(shifted),
      VisitDateValidator.toISODate(VisitDateValidator.getToday())
   );
});

test('Test_IsVisitDateBeforeEarliestFloor_TestInvalidInputs_ExpectFalse', () => {
   const today = makeNoonDate(2026, 5, 15);

   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('bad-date', today), false);
   assert.equal(VisitDateValidator.isVisitDateBeforeEarliestFloor('2026-06-15', 'bad-date'), false);
});
