import assert from 'node:assert/strict';
import test from 'node:test';

import { DateSelectionModel } from '../../../../scripts/itinerary/selectors/dateSelectionModel.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';

import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

const floor = makeNoonDate(2026, 5, 15);


test('Test_FormatVisitDateLong_TestDisplay_ExpectFormatted', () => {
   const date = makeNoonDate(2026, 5, 15);

   const formatted = DateSelectionModel.formatVisitDateLong(date);

   assert.match(formatted, /June 15, 2026/);
});


test('Test_ReadSavedItineraryVisitDate_TestStoredIso_ExpectLocalNoon', () => {
   const isoDate = '2026-06-20';

   const date = DateSelectionModel.readSavedItineraryVisitDate(() => isoDate);

   assert.deepEqual(date, makeNoonDate(2026, 5, 20));
});


test('Test_ReadSavedItineraryVisitDate_TestEmpty_ExpectNull', () => {
   const date = DateSelectionModel.readSavedItineraryVisitDate(() => '');

   assert.equal(date, null);
});


test('Test_ReadSavedItineraryVisitDate_TestInvalid_ExpectNull', () => {
   const date = DateSelectionModel.readSavedItineraryVisitDate(() => 'not-a-date');

   assert.equal(date, null);
});


test('Test_CreateDateSelectionModel_TestYesterday_ExpectRejected', () => {
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      syncInputValue: () => {},
   });
   const yesterday = makeNoonDate(2026, 5, 14);

   const accepted = model.setDate(yesterday);

   assert.equal(accepted, false);
});


test('Test_CreateDateSelectionModel_TestTomorrow_ExpectAccepted', () => {
   const syncedDates = [];
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      syncInputValue: (date) => {
         syncedDates.push(VisitDateValidator.toISODate(date));
      },
   });
   const tomorrow = makeNoonDate(2026, 5, 16);

   const accepted = model.setDate(tomorrow);

   assert.equal(accepted, true);
   assert.deepEqual(syncedDates, [VisitDateValidator.toISODate(tomorrow)]);
});


test('Test_CreateDateSelectionModel_TestBeyondMax_ExpectRejected', () => {
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      daysAhead: 2,
      syncInputValue: () => {},
   });
   const beyondMax = makeNoonDate(2026, 5, 20);

   const accepted = model.setDate(beyondMax);

   assert.equal(accepted, false);
});


test('Test_CreateDateSelectionModel_TestStoredDate_ExpectPreferred', () => {
   const storedDate = '2026-06-18';
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => storedDate,
   });

   const displayDate = model.getDisplayDate();

   assert.equal(VisitDateValidator.toISODate(displayDate), storedDate);
});


test('Test_CreateDateSelectionModel_TestInitialDate_ExpectPreferredOverStored', () => {
   const storedDate = '2026-06-18';
   const initialDate = makeNoonDate(2026, 5, 20);
   const model = DateSelectionModel.createDateSelectionModel({
      initialDate,
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => storedDate,
   });

   const displayDate = model.getDisplayDate();

   assert.equal(VisitDateValidator.toISODate(displayDate), VisitDateValidator.toISODate(initialDate));
});


test('Test_CreateDateSelectionModel_TestNoStoredDate_ExpectFloor', () => {
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getStoredDate: () => null,
   });

   const displayDate = model.getDisplayDate();

   assert.equal(VisitDateValidator.toISODate(displayDate), VisitDateValidator.toISODate(floor));
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

   const payload = model.persistCurrentDate();

   assert.equal(payload.date, VisitDateValidator.toISODate(tomorrow));
   assert.deepEqual(payload.dateObj, tomorrow);
   assert.deepEqual(persistedDates, [VisitDateValidator.toISODate(tomorrow)]);
   assert.equal(model.persistCurrentDate()?.date, VisitDateValidator.toISODate(tomorrow));
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
      const accepted = model.setDate(makeNoonDate(2026, 5, 16));

      assert.equal(accepted, false);
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

   const displayDate = model.getDisplayDate();

   assert.equal(VisitDateValidator.toISODate(displayDate), '2026-06-17');
});


test('Test_CreateDateSelectionModel_TestStaleCurrentDatePayload_ExpectNull', () => {
   let todayCalls = 0;
   const model = DateSelectionModel.createDateSelectionModel({
      earliestDateFloor: floor,
      getTodayFn: () => {
         todayCalls += 1;
         return todayCalls >= 3 ? makeNoonDate(2026, 5, 1) : floor;
      },
      daysAhead: 2,
      setStoredDate: () => {},
   });
   model.setDate(makeNoonDate(2026, 5, 16));

   const payload = model.persistCurrentDate();

   assert.equal(payload, null);
});
