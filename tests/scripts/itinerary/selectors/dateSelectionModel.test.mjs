import assert from 'node:assert/strict';
import test from 'node:test';

import { DateSelectionModel } from '../../../../scripts/itinerary/selectors/dateSelectionModel.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';

import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

const floor = makeNoonDate(2026, 5, 15);

test('Test_FormatVisitDateLong_TestDisplay_ExpectFormatted', () => {
   assert.match(
      DateSelectionModel.formatVisitDateLong(makeNoonDate(2026, 5, 15)),
      /June 15, 2026/
   );
});

test('Test_ReadSavedItineraryVisitDate_TestStoredIso_ExpectLocalNoon', () => {
   assert.deepEqual(
      DateSelectionModel.readSavedItineraryVisitDate(() => '2026-06-20'),
      makeNoonDate(2026, 5, 20)
   );
   assert.equal(DateSelectionModel.readSavedItineraryVisitDate(() => ''), null);
   assert.equal(DateSelectionModel.readSavedItineraryVisitDate(() => 'not-a-date'), null);
});

test('Test_CreateDateSelectionModel_TestOutsideWindow_ExpectRejected', () => {
   const syncedDates = [];
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      syncInputValue: (date) => {
         syncedDates.push(VisitDateValidator.toISODate(date));
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

test('Test_CreateDateSelectionModel_TestDisplayPriority_ExpectPreferred', () => {
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => '2026-06-18',
   });

   assert.equal(VisitDateValidator.toISODate(model.getDisplayDate()), '2026-06-18');

   const modelWithInitial = DateSelectionModel.createDateSelectionModel({
      initialDate: makeNoonDate(2026, 5, 20),
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => '2026-06-18',
   });

   assert.equal(VisitDateValidator.toISODate(modelWithInitial.getDisplayDate()), '2026-06-20');

   const modelWithoutSaved = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => null,
   });

   assert.equal(VisitDateValidator.toISODate(modelWithoutSaved.getDisplayDate()), VisitDateValidator.toISODate(floor));
});

test('Test_CreateDateSelectionModel_TestPersist_ExpectPayload', () => {
   const persistedDates = [];
   const tomorrow = makeNoonDate(2026, 5, 16);
   const model = DateSelectionModel.createDateSelectionModel({
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

test('Test_CreateDateSelectionModel_TestInvalidNormalize_ExpectRejected', () => {
   const originalNormalize = VisitDateValidator.normalizeDate;
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
   });

   let normalizeCalls = 0;
   VisitDateValidator.normalizeDate = (date) => {
      normalizeCalls += 1;
      if (normalizeCalls === 1) {
         return date;
      }

      return null;
   };

   try {
      assert.equal(model.setDate(makeNoonDate(2026, 5, 16)), false);
      assert.equal(model.getDate(), null);
   } finally {
      VisitDateValidator.normalizeDate = originalNormalize;
   }

   assert.equal(model.persistCurrentDate(), null);
});

test('Test_CreateDateSelectionModel_TestSavedOutOfRange_ExpectClamped', () => {
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      getStoredDate: () => '2099-01-01',
   });

   assert.equal(VisitDateValidator.toISODate(model.getDisplayDate()), '2026-06-17');
});

test('Test_CreateDateSelectionModel_TestStaleCurrentDatePayload_ExpectNull', () => {
   let todayCalls = 0;
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => {
         todayCalls += 1;
         // First setDate + persist setDate succeed; buildCurrentDatePayload fails.
         return todayCalls >= 3 ? makeNoonDate(2026, 5, 1) : floor;
      },
      daysAhead: 2,
      setStoredDate: () => {},
   });

   assert.equal(model.setDate(makeNoonDate(2026, 5, 16)), true);
   assert.equal(model.persistCurrentDate(), null);
});
