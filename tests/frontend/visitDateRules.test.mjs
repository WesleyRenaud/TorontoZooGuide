import assert from 'node:assert/strict';
import test from 'node:test';

import {
   getDay,
   getMonth,
   isoDateToMonFirstDow,
   parseLocalDate,
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
   assert.equal(isoDateToMonFirstDow('2026-06-15'), 1);
   assert.equal(isoDateToMonFirstDow('2026-06-21'), 7);
});
