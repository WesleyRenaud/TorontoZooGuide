import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   resolveEarliestSelectableVisitDateNoon,
   resolveEffectiveItineraryHoursDateIso,
} from '../../scripts/itinerary/visitDateEarliest.js';

import { makeNoonDate } from './helpers/visitDateMock.mjs';

const today = makeNoonDate(2026, 5, 15);
const tomorrow = makeNoonDate(2026, 5, 16);

test('resolveEarliestSelectableVisitDateNoon returns today before zoo close', async () => {
   const result = await resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime: '19:00' }),
      isPastClose: () => false,
   });

   assert.equal(result, today);
});

test('resolveEarliestSelectableVisitDateNoon returns tomorrow after zoo close', async () => {
   const addDays = (_date, days) => makeNoonDate(2026, 5, 15 + days);
   const result = await resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => ({ closeTime: '19:00' }),
      isPastClose: () => true,
      addDays,
   });

   assert.equal(result.getTime(), addDays(today, 1).getTime());
});

test('resolveEarliestSelectableVisitDateNoon falls back to today when zoo hours fail', async () => {
   const result = await resolveEarliestSelectableVisitDateNoon({
      getTodayFn: () => today,
      getZooHoursFn: async () => {
         throw new Error('network error');
      },
   });

   assert.equal(result, today);
});

test('resolveEffectiveItineraryHoursDateIso prefers the itinerary date', async () => {
   const result = await resolveEffectiveItineraryHoursDateIso({
      date: ' 2026-06-20 ',
   });

   assert.equal(result, '2026-06-20');
});

test('resolveEffectiveItineraryHoursDateIso uses the stored draft date when itinerary date is missing', async () => {
   const result = await resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => ' 2026-06-18 ',
      }
   );

   assert.equal(result, '2026-06-18');
});

test('resolveEffectiveItineraryHoursDateIso falls back to the earliest selectable visit date', async () => {
   const result = await resolveEffectiveItineraryHoursDateIso(
      {},
      {
         getStoredDate: () => '',
         resolveEarliest: async () => tomorrow,
         toIso: () => '2026-06-16',
      }
   );

   assert.equal(result, '2026-06-16');
});
