import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftModel } from '../../../scripts/itinerary/itineraryDraftModel.js';

test('Test_AsItineraryDraftSource_TestObjectAndNonObject_ExpectObject', () => {
   const draft = { date: '2026-09-08' };

   assert.equal(ItineraryDraftModel.asItineraryDraftSource(draft), draft);
   assert.deepEqual(ItineraryDraftModel.asItineraryDraftSource(null), {});
   assert.deepEqual(ItineraryDraftModel.asItineraryDraftSource('draft'), {});
});

test('Test_NormalizeItineraryDate_TestStringAndOther_ExpectStringOrEmpty', () => {
   assert.equal(ItineraryDraftModel.normalizeItineraryDate('2026-09-08'), '2026-09-08');
   assert.equal(ItineraryDraftModel.normalizeItineraryDate(null), '');
});

test('Test_NormalizeItineraryTime_TestStringAndOther_ExpectStringOrEmpty', () => {
   assert.equal(ItineraryDraftModel.normalizeItineraryTime('09:00'), '09:00');
   assert.equal(ItineraryDraftModel.normalizeItineraryTime(900), '');
});

test('Test_CloneItineraryItems_TestArray_ExpectShallowCopy', () => {
   const items = [{ name: 'Zoomobile' }];
   const cloned = ItineraryDraftModel.cloneItineraryItems(items);

   assert.deepEqual(cloned, items);
   assert.notEqual(cloned, items);
});
