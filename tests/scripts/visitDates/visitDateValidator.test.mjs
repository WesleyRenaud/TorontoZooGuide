import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { VisitDateRuleHelper } from '../../../scripts/visitDates/visitDateRuleHelper.js';
import { ZooClockTimeHelper } from '../../../scripts/shared/zooClockTimeHelper.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const year = 2026;
const juneMonthIndex = 5;
const day = 15;
const referenceToday = makeNoonDate(year, juneMonthIndex, day);
const iso = VisitDateValidator.toISODate(referenceToday);


test('Test_ParseLocalDate_TestValidIso_ExpectLocalNoon', () => {
   const visitDate = VisitDateValidator.parseLocalDate(iso);

   assert.equal(Number.isNaN(visitDate.getTime()), false);
   assert.equal(visitDate.getFullYear(), year);
   assert.equal(visitDate.getMonth(), juneMonthIndex);
   assert.equal(visitDate.getDate(), day);
   assert.equal(visitDate.getHours(), 12);
});


test('Test_ParseLocalDate_TestFebruaryThirty_ExpectInvalidDate', () => {
   const invalidIso = '2026-02-30';

   const visitDate = VisitDateValidator.parseLocalDate(invalidIso);

   assert.equal(Number.isNaN(visitDate.getTime()), true);
});


test('Test_ParseLocalDate_TestInvalidMonth_ExpectInvalidDate', () => {
   const invalidIso = '2026-13-01';

   const visitDate = VisitDateValidator.parseLocalDate(invalidIso);

   assert.equal(Number.isNaN(visitDate.getTime()), true);
});


test('Test_ParseLocalDate_TestRegionName_ExpectInvalidDate', () => {
   const invalidIso = 'African Rainforest';

   const visitDate = VisitDateValidator.parseLocalDate(invalidIso);

   assert.equal(Number.isNaN(visitDate.getTime()), true);
});


test('Test_ToISODate_TestLocalEvening_ExpectSameCalendarDay', () => {
   const evening = new Date(year, juneMonthIndex, day, 23, 59);

   const formatted = VisitDateValidator.toISODate(evening);

   assert.equal(formatted, iso);
});


test('Test_GetMonth_TestValidIso_ExpectAbbreviated', () => {
   const month = VisitDateValidator.getMonth(iso);

   assert.equal(month, 'JUN');
});


test('Test_GetDay_TestValidIso_ExpectDay', () => {
   const parsedDay = VisitDateValidator.getDay(iso);

   assert.equal(parsedDay, day);
});


test('Test_GetYear_TestValidIso_ExpectYear', () => {
   const parsedYear = VisitDateValidator.getYear(iso);

   assert.equal(parsedYear, year);
});


test('Test_GetMonth_TestInvalidIso_ExpectNull', () => {
   const invalidIso = 'bad-date';

   const month = VisitDateValidator.getMonth(invalidIso);

   assert.equal(month, null);
});


test('Test_GetDay_TestInvalidIso_ExpectNull', () => {
   const invalidIso = 'bad-date';

   const parsedDay = VisitDateValidator.getDay(invalidIso);

   assert.equal(parsedDay, null);
});


test('Test_GetYear_TestInvalidIso_ExpectNull', () => {
   const invalidIso = 'bad-date';

   const parsedYear = VisitDateValidator.getYear(invalidIso);

   assert.equal(parsedYear, null);
});


test('Test_IsoDateToMonFirstDow_TestMonday_ExpectFirst', () => {
   const mondayIso = iso;

   const weekday = VisitDateValidator.isoDateToMonFirstDow(mondayIso);

   assert.equal(weekday, 1);
});


test('Test_IsoDateToMonFirstDow_TestSunday_ExpectSeventh', () => {
   const sundayIso = '2026-06-21';

   const weekday = VisitDateValidator.isoDateToMonFirstDow(sundayIso);

   assert.equal(weekday, 7);
});


test('Test_IsoDateToMonFirstDow_TestInvalidIso_ExpectFirst', () => {
   const invalidIso = 'bad-date';

   const weekday = VisitDateValidator.isoDateToMonFirstDow(invalidIso);

   assert.equal(weekday, 1);
});


test('Test_IsoDateToMonFirstDow_TestMissingIso_ExpectTodayWeekday', () => {
   const weekday = VisitDateValidator.isoDateToMonFirstDow();

   assert.equal(
      weekday,
      VisitDateValidator.isoDateToMonFirstDow(VisitDateValidator.toISODate(VisitDateValidator.getToday()))
   );
});


test('Test_ResolveOptionalStartDate_TestProvided_ExpectSame', () => {
   const startDate = '2026-06-20';

   const resolved = VisitDateValidator.resolveOptionalStartDate(startDate);

   assert.equal(resolved, startDate);
});


test('Test_ResolveOptionalStartDate_TestBlank_ExpectToday', () => {
   const startDate = '';

   const resolved = VisitDateValidator.resolveOptionalStartDate(startDate);

   assert.equal(resolved, VisitDateValidator.toISODate(VisitDateValidator.getToday()));
});


test('Test_ResolveOptionalStartDate_TestNull_ExpectToday', () => {
   const startDate = null;

   const resolved = VisitDateValidator.resolveOptionalStartDate(startDate);

   assert.equal(resolved, VisitDateValidator.toISODate(VisitDateValidator.getToday()));
});


test('Test_FormatLocalDateLong_TestValidIso_ExpectFriendlyText', () => {
   const formatted = VisitDateValidator.formatLocalDateLong(iso);

   assert.equal(formatted, 'June 15, 2026');
});


test('Test_FormatLocalDateLong_TestBlank_ExpectEmpty', () => {
   const visitDate = '';

   const formatted = VisitDateValidator.formatLocalDateLong(visitDate);

   assert.equal(formatted, '');
});


test('Test_FormatLocalDateLong_TestInvalidIso_ExpectEmpty', () => {
   const visitDate = 'bad-date';

   const formatted = VisitDateValidator.formatLocalDateLong(visitDate);

   assert.equal(formatted, '');
});


test('Test_FormatLocalDateRange_TestBothDates_ExpectJoined', () => {
   const startDate = iso;
   const endDate = '2026-06-30';

   const formatted = VisitDateValidator.formatLocalDateRange(startDate, endDate);

   assert.equal(
      formatted,
      `${VisitDateValidator.formatLocalDateLong(startDate)} - ${VisitDateValidator.formatLocalDateLong(endDate)}`
   );
});


test('Test_FormatLocalDateRange_TestMissingEnd_ExpectStartOnly', () => {
   const startDate = iso;
   const endDate = null;

   const formatted = VisitDateValidator.formatLocalDateRange(startDate, endDate);

   assert.equal(formatted, VisitDateValidator.formatLocalDateLong(startDate));
});


test('Test_FormatLocalDateRange_TestBlankStart_ExpectEmpty', () => {
   const startDate = '';
   const endDate = '2026-06-30';

   const formatted = VisitDateValidator.formatLocalDateRange(startDate, endDate);

   assert.equal(formatted, '');
});


test('Test_NormalizeDate_TestSameDayEvening_ExpectTodayNoon', () => {
   const today = VisitDateValidator.getToday();
   const evening = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59);

   const normalized = VisitDateValidator.normalizeDate(evening);

   assert.equal(VisitDateValidator.toISODate(normalized), VisitDateValidator.toISODate(today));
});


test('Test_NormalizeDate_TestInvalidIso_ExpectNull', () => {
   const invalidDate = 'bad-date';

   const normalized = VisitDateValidator.normalizeDate(invalidDate);

   assert.equal(normalized, null);
});


test('Test_IsBeforeToday_TestYesterday_ExpectTrue', () => {
   const today = VisitDateValidator.getToday();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   const isBefore = VisitDateValidator.isBeforeToday(yesterday);

   assert.equal(isBefore, true);
});


test('Test_IsBeforeToday_TestInvalidIso_ExpectFalse', () => {
   const invalidDate = 'bad-date';

   const isBefore = VisitDateValidator.isBeforeToday(invalidDate);

   assert.equal(isBefore, false);
});


test('Test_IsAfterMaxDate_TestDayAfterMax_ExpectTrue', () => {
   const daysAhead = 2;
   const afterMax = new Date(VisitDateValidator.getMaxDate(daysAhead));
   afterMax.setDate(afterMax.getDate() + 1);

   const isAfter = VisitDateValidator.isAfterMaxDate(afterMax, daysAhead);

   assert.equal(isAfter, true);
});


test('Test_IsAfterMaxDate_TestInvalidIso_ExpectFalse', () => {
   const daysAhead = 2;
   const invalidDate = 'bad-date';

   const isAfter = VisitDateValidator.isAfterMaxDate(invalidDate, daysAhead);

   assert.equal(isAfter, false);
});


test('Test_IsWithinNextNDays_TestTomorrow_ExpectTrue', () => {
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const daysAhead = 2;

   const isWithin = VisitDateValidator.isWithinNextNDays(VisitDateValidator.toISODate(tomorrow), daysAhead);

   assert.equal(isWithin, true);
});


test('Test_IsWithinNextNDays_TestAfterMax_ExpectFalse', () => {
   const daysAhead = 2;
   const afterMax = new Date(VisitDateValidator.getMaxDate(daysAhead));
   afterMax.setDate(afterMax.getDate() + 1);

   const isWithin = VisitDateValidator.isWithinNextNDays(VisitDateValidator.toISODate(afterMax), daysAhead);

   assert.equal(isWithin, false);
});


test('Test_IsWithinNextNDays_TestInvalidIso_ExpectFalse', () => {
   const daysAhead = 2;
   const invalidDate = 'bad-date';

   const isWithin = VisitDateValidator.isWithinNextNDays(invalidDate, daysAhead);

   assert.equal(isWithin, false);
});


test('Test_IsBeforeToday_TestReferenceYesterday_ExpectTrue', () => {
   const yesterday = makeNoonDate(year, juneMonthIndex, day - 1);

   const isBefore = VisitDateValidator.isBeforeToday(yesterday, referenceToday);

   assert.equal(isBefore, true);
});


test('Test_IsBeforeToday_TestReferenceTomorrow_ExpectFalse', () => {
   const tomorrow = makeNoonDate(year, juneMonthIndex, day + 1);

   const isBefore = VisitDateValidator.isBeforeToday(tomorrow, referenceToday);

   assert.equal(isBefore, false);
});


test('Test_IsAfterMaxDate_TestReferenceAfterMax_ExpectTrue', () => {
   const daysAhead = 2;
   const afterMax = makeNoonDate(year, juneMonthIndex, day + 3);

   const isAfter = VisitDateValidator.isAfterMaxDate(afterMax, daysAhead, referenceToday);

   assert.equal(isAfter, true);
});


test('Test_IsAfterMaxDate_TestReferenceTomorrow_ExpectFalse', () => {
   const daysAhead = 2;
   const tomorrow = makeNoonDate(year, juneMonthIndex, day + 1);

   const isAfter = VisitDateValidator.isAfterMaxDate(tomorrow, daysAhead, referenceToday);

   assert.equal(isAfter, false);
});


test('Test_IsWithinNextNDays_TestReferenceTomorrow_ExpectTrue', () => {
   const daysAhead = 2;
   const tomorrowIso = '2026-06-16';

   const isWithin = VisitDateValidator.isWithinNextNDays(tomorrowIso, daysAhead, referenceToday);

   assert.equal(isWithin, true);
});


test('Test_IsWithinNextNDays_TestReferenceAfterMax_ExpectFalse', () => {
   const daysAhead = 2;
   const afterMaxIso = '2026-06-18';

   const isWithin = VisitDateValidator.isWithinNextNDays(afterMaxIso, daysAhead, referenceToday);

   assert.equal(isWithin, false);
});


test('Test_GetMaxDate_TestReferenceToday_ExpectTwoDaysAhead', () => {
   const daysAhead = 2;

   const maxDate = VisitDateValidator.getMaxDate(daysAhead, referenceToday);

   assert.equal(VisitDateValidator.toISODate(maxDate), '2026-06-17');
});


test('Test_ClampToAllowedVisitDate_TestInvalidIso_ExpectToday', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();

   const clamped = VisitDateValidator.clampToAllowedVisitDate('bad-date', daysAhead);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(today));
});


test('Test_ClampToAllowedVisitDate_TestYesterday_ExpectToday', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(yesterday, daysAhead);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(today));
});


test('Test_ClampToAllowedVisitDate_TestAfterMax_ExpectMax', () => {
   const daysAhead = 2;
   const maxDate = VisitDateValidator.getMaxDate(daysAhead);
   const afterMax = new Date(maxDate);
   afterMax.setDate(maxDate.getDate() + 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(afterMax, daysAhead);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(maxDate));
});


test('Test_ClampToAllowedVisitDate_TestTomorrow_ExpectTomorrow', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(tomorrow, daysAhead);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(tomorrow));
});


test('Test_ClampToAllowedVisitDate_TestCustomFloorYesterday_ExpectFloor', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);
   const yesterday = new Date(today);
   yesterday.setDate(today.getDate() - 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(yesterday, daysAhead, tomorrow);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(tomorrow));
});


test('Test_ClampToAllowedVisitDate_TestCustomFloorToday_ExpectFloor', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(today, daysAhead, tomorrow);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(tomorrow));
});


test('Test_ClampToAllowedVisitDate_TestCustomFloorTomorrow_ExpectTomorrow', () => {
   const daysAhead = 2;
   const today = VisitDateValidator.getToday();
   const tomorrow = new Date(today);
   tomorrow.setDate(today.getDate() + 1);

   const clamped = VisitDateValidator.clampToAllowedVisitDate(tomorrow, daysAhead, tomorrow);

   assert.equal(VisitDateValidator.toISODate(clamped), VisitDateValidator.toISODate(tomorrow));
});


test('Test_ParseZooClockTimeMinutes_TestTwentyFourHour_ExpectMinutes', () => {
   const time = '19:00';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, ZooClockTimeHelper.parseMinutes(time));
});


test('Test_ParseZooClockTimeMinutes_TestEveningDisplay_ExpectMinutes', () => {
   const time = '7:00 PM';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, ZooClockTimeHelper.parseMinutes(time));
});


test('Test_ParseZooClockTimeMinutes_TestMidnight_ExpectZero', () => {
   const time = '12:00 AM';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, ZooClockTimeHelper.parseMinutes(time));
});


test('Test_ParseZooClockTimeMinutes_TestNoon_ExpectMinutes', () => {
   const time = '12:00 PM';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, ZooClockTimeHelper.parseMinutes(time));
});


test('Test_ParseZooClockTimeMinutes_TestBlank_ExpectNull', () => {
   const time = '';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, null);
});


test('Test_ParseZooClockTimeMinutes_TestInvalidHour_ExpectNull', () => {
   const time = '25:00';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, null);
});


test('Test_NormalizeScheduleTime_TestDisplay_ExpectSame', () => {
   const time = '1:00 PM';

   const normalized = VisitDateValidator.normalizeScheduleTime(time);

   assert.equal(normalized, time);
});


test('Test_NormalizeScheduleTime_TestAfternoonTwentyFourHour_ExpectDisplay', () => {
   const time = '15:30';

   const normalized = VisitDateValidator.normalizeScheduleTime(time);

   assert.equal(normalized, '3:30 PM');
});


test('Test_NormalizeScheduleTime_TestMorningTwentyFourHour_ExpectDisplay', () => {
   const time = '10:00';

   const normalized = VisitDateValidator.normalizeScheduleTime(time);

   assert.equal(normalized, '10:00 AM');
});


test('Test_NormalizeScheduleTime_TestBlank_ExpectNull', () => {
   const time = '';

   const normalized = VisitDateValidator.normalizeScheduleTime(time);

   assert.equal(normalized, null);
});


test('Test_NormalizeScheduleTime_TestInvalid_ExpectNull', () => {
   const time = 'not-a-time';

   const normalized = VisitDateValidator.normalizeScheduleTime(time);

   assert.equal(normalized, null);
});


test('Test_NormalizeItineraryScheduleTime_TestDisplay_ExpectSame', () => {
   const time = '1:00 PM';

   const normalized = VisitDateValidator.normalizeItineraryScheduleTime(time);

   assert.equal(normalized, time);
});


test('Test_IsLocalTimeAtOrPastZooClose_TestAtClose_ExpectTrue', () => {
   const closeTime = '19:00';
   const closeAtSevenPm = new Date(year, 4, 10, 19, 0, 0, 0);

   const isPast = VisitDateValidator.isLocalTimeAtOrPastZooClose(closeTime, closeAtSevenPm);

   assert.equal(isPast, true);
});


test('Test_IsLocalTimeAtOrPastZooClose_TestJustBefore_ExpectFalse', () => {
   const closeTime = '19:00';
   const justBeforeClose = new Date(year, 4, 10, 18, 59, 0, 0);

   const isPast = VisitDateValidator.isLocalTimeAtOrPastZooClose(closeTime, justBeforeClose);

   assert.equal(isPast, false);
});


test('Test_IsLocalTimeAtOrPastZooClose_TestMissingClose_ExpectFalse', () => {
   const closeTime = null;
   const closeAtSevenPm = new Date(year, 4, 10, 19, 0, 0, 0);

   const isPast = VisitDateValidator.isLocalTimeAtOrPastZooClose(closeTime, closeAtSevenPm);

   assert.equal(isPast, false);
});


test('Test_AddLocalCalendarDays_TestNoonAnchor_ExpectShifted', () => {
   const anchor = VisitDateValidator.parseLocalDate(iso);
   const next = VisitDateValidator.addLocalCalendarDays(anchor, 1);
   const prev = VisitDateValidator.addLocalCalendarDays(anchor, -1);

   assert.equal(VisitDateValidator.toISODate(next), '2026-06-16');
   assert.equal(VisitDateValidator.toISODate(prev), '2026-06-14');
});


test('Test_IsVisitDateBeforeEarliestFloor_TestSameDay_ExpectFalse', () => {
   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(iso, referenceToday);

   assert.equal(isBefore, false);
});


test('Test_IsVisitDateBeforeEarliestFloor_TestTomorrowFloor_ExpectTrue', () => {
   const tomorrow = makeNoonDate(year, juneMonthIndex, day + 1);

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(iso, tomorrow);

   assert.equal(isBefore, true);
});


test('Test_IsVisitDateBeforeEarliestFloor_TestYesterday_ExpectTrue', () => {
   const yesterdayIso = '2026-06-14';

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(yesterdayIso, referenceToday);

   assert.equal(isBefore, true);
});


test('Test_IsVisitDateBeforeEarliestFloor_TestLaterDate_ExpectFalse', () => {
   const laterIso = '2026-06-20';

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(laterIso, referenceToday);

   assert.equal(isBefore, false);
});


test('Test_IsVisitDateBeforeEarliestFloor_TestBlank_ExpectFalse', () => {
   const visitDate = '  ';

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(visitDate, referenceToday);

   assert.equal(isBefore, false);
});


test('Test_ParseLocalDate_TestFractionalMonth_ExpectInvalidDate', () => {
   const invalidIso = '2026-6.5-15';

   const visitDate = VisitDateValidator.parseLocalDate(invalidIso);

   assert.equal(Number.isNaN(visitDate.getTime()), true);
});


test('Test_ParseLocalDate_TestNonNumericDay_ExpectInvalidDate', () => {
   const invalidIso = '2026-06-1a';

   const visitDate = VisitDateValidator.parseLocalDate(invalidIso);

   assert.equal(Number.isNaN(visitDate.getTime()), true);
});


test('Test_ParseLocalDate_TestInvalidParsedDate_ExpectInvalidDate', () => {
   const original = VisitDateRuleHelper.isValidDate;
   VisitDateRuleHelper.isValidDate = () => false;

   try {
      const visitDate = VisitDateValidator.parseLocalDate(iso);

      assert.equal(Number.isNaN(visitDate.getTime()), true);
   } finally {
      VisitDateRuleHelper.isValidDate = original;
   }
});


test('Test_ParseZooClockTimeMinutes_TestZeroHourAm_ExpectNull', () => {
   const time = '0:00 AM';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, null);
});


test('Test_ParseZooClockTimeMinutes_TestThirteenHourPm_ExpectNull', () => {
   const time = '13:00 PM';

   const minutes = VisitDateValidator.parseZooClockTimeMinutes(time);

   assert.equal(minutes, null);
});


test('Test_AddLocalCalendarDays_TestInvalidBase_ExpectToday', () => {
   const invalid = VisitDateValidator.parseLocalDate('2026-02-30');

   const shifted = VisitDateValidator.addLocalCalendarDays(invalid, 1);

   assert.equal(
      VisitDateValidator.toISODate(shifted),
      VisitDateValidator.toISODate(VisitDateValidator.getToday())
   );
});


test('Test_IsVisitDateBeforeEarliestFloor_TestInvalidVisitDate_ExpectFalse', () => {
   const invalidIso = 'bad-date';

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(invalidIso, referenceToday);

   assert.equal(isBefore, false);
});


test('Test_IsVisitDateBeforeEarliestFloor_TestInvalidFloor_ExpectFalse', () => {
   const invalidFloor = 'bad-date';

   const isBefore = VisitDateValidator.isVisitDateBeforeEarliestFloor(iso, invalidFloor);

   assert.equal(isBefore, false);
});
