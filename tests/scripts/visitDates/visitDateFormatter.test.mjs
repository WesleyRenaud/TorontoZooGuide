import assert from 'node:assert/strict';
import test from 'node:test';

import { VisitDateFormatter } from '../../../scripts/visitDates/visitDateFormatter.js';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const _ISO = '2026-06-15';
const _NOON = makeNoonDate(2026, 5, 15);


test('Test_FormatLong_TestIso_ExpectWeekdayMonthDayYear', () => {
   const formatted = VisitDateFormatter.formatLong(_ISO);

   assert.match(formatted, /June 15, 2026/);
});


test('Test_FormatLong_TestDate_ExpectWeekdayMonthDayYear', () => {
   const formatted = VisitDateFormatter.formatLong(_NOON);

   assert.match(formatted, /June 15, 2026/);
});


test('Test_FormatLong_TestEnglishCanada_ExpectSamePhrase', () => {
   const formatted = VisitDateFormatter.formatLong('2026-06-20', 'en-CA');

   assert.equal(
      formatted,
      new Intl.DateTimeFormat('en-CA', {
         weekday: 'long',
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      }).format(new Date(2026, 5, 20))
   );
});


test('Test_FormatLong_TestInvalid_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatLong('not-a-date');

   assert.equal(formatted, '');
});


test('Test_FormatMonthDayYear_TestIso_ExpectMonthDayYear', () => {
   const formatted = VisitDateFormatter.formatMonthDayYear(_ISO);

   assert.equal(formatted, 'June 15, 2026');
});


test('Test_FormatMonthDayYear_TestDate_ExpectMonthDayYear', () => {
   const formatted = VisitDateFormatter.formatMonthDayYear(_NOON);

   assert.equal(formatted, 'June 15, 2026');
});


test('Test_FormatMonthDayYear_TestBlank_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatMonthDayYear('');

   assert.equal(formatted, '');
});


test('Test_FormatMonthDayYear_TestInvalid_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatMonthDayYear('bad-date');

   assert.equal(formatted, '');
});


test('Test_FormatRange_TestBothDates_ExpectJoined', () => {
   const endDate = '2026-06-30';

   const formatted = VisitDateFormatter.formatRange(_ISO, endDate);

   assert.equal(
      formatted,
      `${VisitDateFormatter.formatMonthDayYear(_ISO)} - ${VisitDateFormatter.formatMonthDayYear(endDate)}`
   );
});


test('Test_FormatRange_TestMissingEnd_ExpectStartOnly', () => {
   const formatted = VisitDateFormatter.formatRange(_ISO, null);

   assert.equal(formatted, VisitDateFormatter.formatMonthDayYear(_ISO));
});


test('Test_FormatRange_TestBlankStart_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatRange('', '2026-06-30');

   assert.equal(formatted, '');
});


test('Test_FormatShort_TestCanonicalIso_ExpectShortDate', () => {
   const formatted = VisitDateFormatter.formatShort('2026-10-26');

   assert.equal(
      formatted,
      new Date(2026, 9, 26).toLocaleDateString('en-US', {
         weekday: 'short',
         month: 'short',
         day: 'numeric',
      })
   );
});


test('Test_FormatShort_TestInvalid_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatShort('tomorrow');

   assert.equal(formatted, '');
});


test('Test_FormatShort_TestUnpadded_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatShort('2026-10-5');

   assert.equal(formatted, '');
});


test('Test_Format_TestInvalidDateObject_ExpectEmpty', () => {
   const formatted = VisitDateFormatter.formatLong(new Date(Number.NaN));

   assert.equal(formatted, '');
});
