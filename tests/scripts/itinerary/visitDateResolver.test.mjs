import assert from 'node:assert/strict';
import { test } from 'node:test';

import { VisitDateResolver } from '../../../scripts/itinerary/visitDateResolver.js';

import { makeNoonDate } from '../helpers/visitDateMock.mjs';

const today = makeNoonDate(2026, 5, 15);
const tomorrow = makeNoonDate(2026, 5, 16);


test('Test_ResolveEarliestSelectableVisitDateNoon_TestBeforeClose_ExpectToday', async () => {
   const closeTime = '19:00';

   const result = await VisitDateResolver.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime }),
      isPastClose: () => false,
   });

   assert.equal(result, today);
});


test('Test_ResolveEarliestSelectableVisitDateNoon_TestAfterClose_ExpectTomorrow', async () => {
   const closeTime = '19:00';
   const addDays = (_date, days) => makeNoonDate(2026, 5, 15 + days);

   const result = await VisitDateResolver.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime }),
      isPastClose: () => true,
      addDays,
   });

   assert.equal(result.getTime(), addDays(today, 1).getTime());
});


test('Test_ResolveEarliestSelectableVisitDateNoon_TestHoursFail_ExpectToday', async () => {
   const result = await VisitDateResolver.resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => {
         throw new Error('network error');
      },
   });

   assert.equal(result, today);
});


test('Test_ResolveEffectiveItineraryHoursDateIso_TestItineraryDate_ExpectPreferred', async () => {
   const date = '2026-06-20';

   const result = await VisitDateResolver.resolveEffectiveItineraryHoursDateIso({
      date: ` ${date} `,
   });

   assert.equal(result, date);
});


test('Test_ResolveEffectiveItineraryHoursDateIso_TestStoredDraft_ExpectUsed', async () => {
   const date = '2026-06-18';

   const result = await VisitDateResolver.resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => ` ${date} `,
      }
   );

   assert.equal(result, date);
});


test('Test_ResolveEffectiveItineraryHoursDateIso_TestNoDates_ExpectEarliest', async () => {
   const date = '2026-06-16';

   const result = await VisitDateResolver.resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => '',
         resolveEarliest: async () => tomorrow,
         toIso: () => date,
      }
   );

   assert.equal(result, date);
});
