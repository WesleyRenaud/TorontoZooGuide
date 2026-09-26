import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateRuleHelper } from '../../../scripts/visitDates/visitDateRuleHelper.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';


test('Test_CreateInvalidDate_TestDefault_ExpectNaN', () => {
   const date = VisitDateRuleHelper.createInvalidDate();

   assert.equal(Number.isNaN(date.getTime()), true);
});


test('Test_IsValidDate_TestNoonDate_ExpectTrue', () => {
   const date = makeNoonDate(2026, 5, 15);

   const isValid = VisitDateRuleHelper.isValidDate(date);

   assert.equal(isValid, true);
});


test('Test_IsValidDate_TestInvalidDate_ExpectFalse', () => {
   const date = VisitDateRuleHelper.createInvalidDate();

   const isValid = VisitDateRuleHelper.isValidDate(date);

   assert.equal(isValid, false);
});


test('Test_IsValidDate_TestNull_ExpectFalse', () => {
   const date = null;

   const isValid = VisitDateRuleHelper.isValidDate(date);

   assert.equal(isValid, false);
});


test('Test_CreateLocalNoonDate_TestParts_ExpectNoon', () => {
   const year = 2026;
   const monthIndex = 5;
   const day = 15;

   const date = VisitDateRuleHelper.createLocalNoonDate(year, monthIndex, day);

   assert.equal(date.getFullYear(), year);
   assert.equal(date.getMonth(), monthIndex);
   assert.equal(date.getDate(), day);
   assert.equal(date.getHours(), VisitDateRuleHelper.LOCAL_NOON_HOUR);
});


test('Test_MatchesDateParts_TestSameDay_ExpectTrue', () => {
   const year = 2026;
   const monthIndex = 5;
   const day = 15;
   const date = makeNoonDate(year, monthIndex, day);

   const matches = VisitDateRuleHelper.matchesDateParts(date, {
      year,
      monthIndex,
      day,
   });

   assert.equal(matches, true);
});


test('Test_MatchesDateParts_TestDifferentDay_ExpectFalse', () => {
   const year = 2026;
   const monthIndex = 5;
   const day = 15;
   const date = makeNoonDate(year, monthIndex, day);

   const matches = VisitDateRuleHelper.matchesDateParts(date, {
      year,
      monthIndex,
      day: day + 1,
   });

   assert.equal(matches, false);
});


test('Test_CreateAllowedVisitDateRange_TestReferenceToday_ExpectBounds', () => {
   const today = makeNoonDate(2026, 5, 15);
   const expectedMax = new Date(today);
   expectedMax.setDate(today.getDate() + VisitDateValidator.DEFAULT_DAYS_AHEAD);

   const range = VisitDateRuleHelper.createAllowedVisitDateRange(
      VisitDateValidator.DEFAULT_DAYS_AHEAD,
      today
   );

   assert.equal(range.today.getTime(), today.getTime());
   assert.equal(range.maxDate.getTime(), expectedMax.getTime());
});
