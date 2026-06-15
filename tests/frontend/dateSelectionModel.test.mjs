import assert from 'node:assert/strict';
import test from 'node:test';

import {
   createDateSelectionModel,
   formatVisitDateLong,
   readSavedItineraryVisitDate,
} from '../../scripts/itinerary/selectors/dateSelectionModel.js';
import {
   toISODate,
} from '../../scripts/visitDates/visitDateRules.js';

function makeNoonDate(year, monthIndex, day) {
   return new Date(year, monthIndex, day, 12, 0, 0, 0);
}

const floor = makeNoonDate(2026, 5, 15);

test('formatVisitDateLong formats a visit date for display', () => {
   assert.match(
      formatVisitDateLong(makeNoonDate(2026, 5, 15)),
      /June 15, 2026/
   );
});

test('readSavedItineraryVisitDate parses stored ISO dates at local noon', () => {
   assert.deepEqual(
      readSavedItineraryVisitDate(() => '2026-06-20'),
      makeNoonDate(2026, 5, 20)
   );
   assert.equal(readSavedItineraryVisitDate(() => ''), null);
   assert.equal(readSavedItineraryVisitDate(() => 'not-a-date'), null);
});

test('createDateSelectionModel rejects dates outside the allowed window', () => {
   const syncedDates = [];
   const model = createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      syncInputValue: (date) => {
         syncedDates.push(toISODate(date));
      },
   });

   const yesterday = makeNoonDate(2026, 5, 14);
   const tomorrow = makeNoonDate(2026, 5, 16);
   const beyondMax = makeNoonDate(2026, 5, 20);

   assert.equal(model.setDate(yesterday), false);
   assert.equal(model.setDate(tomorrow), true);
   assert.equal(model.setDate(beyondMax), false);
   assert.deepEqual(syncedDates, ['2026-06-16']);
});

test('createDateSelectionModel prefers initial, saved, and floor dates for display', () => {
   const model = createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => '2026-06-18',
   });

   assert.equal(toISODate(model.getDisplayDate()), '2026-06-18');

   const modelWithInitial = createDateSelectionModel({
      initialDate: makeNoonDate(2026, 5, 20),
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => '2026-06-18',
   });

   assert.equal(toISODate(modelWithInitial.getDisplayDate()), '2026-06-20');

   const modelWithoutSaved = createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => null,
   });

   assert.equal(toISODate(modelWithoutSaved.getDisplayDate()), toISODate(floor));
});

test('createDateSelectionModel persists the current date and returns payload data', () => {
   const persistedDates = [];
   const tomorrow = makeNoonDate(2026, 5, 16);
   const model = createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      setStoredDate: (isoDate) => {
         persistedDates.push(isoDate);
      },
   });

   model.setDate(tomorrow);

   assert.deepEqual(model.persistCurrentDate(), {
      date: '2026-06-16',
      dateObj: tomorrow,
   });
   assert.deepEqual(persistedDates, ['2026-06-16']);
   assert.equal(model.persistCurrentDate()?.date, '2026-06-16');
});

test('createDateSelectionModel clamps saved display dates to the allowed range', () => {
   const model = createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      getStoredDate: () => '2099-01-01',
   });

   assert.equal(toISODate(model.getDisplayDate()), '2026-06-17');
});
