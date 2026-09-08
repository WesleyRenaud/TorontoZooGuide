import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateRuleHelper } from '../../../scripts/visitDates/visitDateRuleHelper.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';

test('Test_CreateInvalidDate_TestDefault_ExpectNaN', () => {
   assert.equal(Number.isNaN(VisitDateRuleHelper.createInvalidDate().getTime()), true);
});

test('Test_IsValidDate_TestValues_ExpectBoolean', () => {
   assert.equal(VisitDateRuleHelper.isValidDate(makeNoonDate(2026, 5, 15)), true);
   assert.equal(VisitDateRuleHelper.isValidDate(VisitDateRuleHelper.createInvalidDate()), false);
   assert.equal(VisitDateRuleHelper.isValidDate(null), false);
});

test('Test_CreateLocalNoonDate_TestParts_ExpectNoon', () => {
   const date = VisitDateRuleHelper.createLocalNoonDate(2026, 5, 15);
   assert.equal(date.getFullYear(), 2026);
   assert.equal(date.getMonth(), 5);
   assert.equal(date.getDate(), 15);
   assert.equal(date.getHours(), VisitDateRuleHelper.LOCAL_NOON_HOUR);
});

test('Test_MatchesDateParts_TestSameDay_ExpectTrue', () => {
   const date = makeNoonDate(2026, 5, 15);
   assert.equal(VisitDateRuleHelper.matchesDateParts(date, {
      year: 2026,
      monthIndex: 5,
      day: 15,
   }), true);
   assert.equal(VisitDateRuleHelper.matchesDateParts(date, {
      year: 2026,
      monthIndex: 5,
      day: 16,
   }), false);
});

test('Test_CreateAllowedVisitDateRange_TestReferenceToday_ExpectBounds', () => {
   const today = makeNoonDate(2026, 5, 15);
   const range = VisitDateRuleHelper.createAllowedVisitDateRange(
      VisitDateValidator.DEFAULT_DAYS_AHEAD,
      today
   );

   assert.equal(range.today.getTime(), today.getTime());
   const expectedMax = new Date(today);
   expectedMax.setDate(today.getDate() + VisitDateValidator.DEFAULT_DAYS_AHEAD);
   assert.equal(range.maxDate.getTime(), expectedMax.getTime());
});
