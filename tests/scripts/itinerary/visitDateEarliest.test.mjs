import assert from 'node:assert/strict';
import { test } from 'node:test';

import { VisitDateEarliest } from '../../../scripts/itinerary/visitDateEarliest.js';

import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const today = makeNoonDate(2026, 5, 15);
const tomorrow = makeNoonDate(2026, 5, 16);

test('Test_ResolveEarliestSelectableVisitDateNoon_TestBeforeClose_ExpectToday', async () => {
   const result = await VisitDateEarliest.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime: '19:00' }),
      isPastClose: () => false,
   });

   assert.equal(result, today);
});

test('Test_ResolveEarliestSelectableVisitDateNoon_TestAfterClose_ExpectTomorrow', async () => {
   const addDays = (_date, days) => makeNoonDate(2026, 5, 15 + days);
   const result = await VisitDateEarliest.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime: '19:00' }),
      isPastClose: () => true,
      addDays,
   });

   assert.equal(result.getTime(), addDays(today, 1).getTime());
});

test('Test_ResolveEarliestSelectableVisitDateNoon_TestHoursFail_ExpectToday', async () => {
   const result = await VisitDateEarliest.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => {
         throw new Error('network error');
      },
   });

   assert.equal(result, today);
});

test('Test_ResolveEffectiveItineraryHoursDateIso_TestItineraryDate_ExpectPreferred', async () => {
   const result = await VisitDateEarliest.resolveEffectiveItineraryHoursDateIso({
      date: ' 2026-06-20 ',
   });

   assert.equal(result, '2026-06-20');
});

test('Test_ResolveEffectiveItineraryHoursDateIso_TestStoredDraft_ExpectUsed', async () => {
   const result = await VisitDateEarliest.resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => ' 2026-06-18 ',
      }
   );

   assert.equal(result, '2026-06-18');
});

test('Test_ResolveEffectiveItineraryHoursDateIso_TestNoDates_ExpectEarliest', async () => {
   const result = await VisitDateEarliest.resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => '',
         resolveEarliest: async () => tomorrow,
         toIso: () => '2026-06-16',
      }
   );

   assert.equal(result, '2026-06-16');
});
