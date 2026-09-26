import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftModel } from '../../../scripts/itinerary/itineraryDraftModel.js';


test('Test_AsItineraryDraftSource_TestObject_ExpectSameReference', () => {
   const draft = { date: '2026-09-08' };

   const source = ItineraryDraftModel.asItineraryDraftSource(draft);

   assert.equal(source, draft);
});


test('Test_AsItineraryDraftSource_TestNull_ExpectEmptyObject', () => {
   const draft = null;

   const source = ItineraryDraftModel.asItineraryDraftSource(draft);

   assert.deepEqual(source, {});
});


test('Test_AsItineraryDraftSource_TestString_ExpectEmptyObject', () => {
   const draft = 'draft';

   const source = ItineraryDraftModel.asItineraryDraftSource(draft);

   assert.deepEqual(source, {});
});


test('Test_NormalizeItineraryDate_TestString_ExpectString', () => {
   const date = '2026-09-08';

   const normalized = ItineraryDraftModel.normalizeItineraryDate(date);

   assert.equal(normalized, date);
});


test('Test_NormalizeItineraryDate_TestNull_ExpectEmpty', () => {
   const date = null;

   const normalized = ItineraryDraftModel.normalizeItineraryDate(date);

   assert.equal(normalized, '');
});


test('Test_NormalizeItineraryTime_TestString_ExpectString', () => {
   const time = '09:00';

   const normalized = ItineraryDraftModel.normalizeItineraryTime(time);

   assert.equal(normalized, time);
});


test('Test_NormalizeItineraryTime_TestNumber_ExpectEmpty', () => {
   const time = 900;

   const normalized = ItineraryDraftModel.normalizeItineraryTime(time);

   assert.equal(normalized, '');
});


test('Test_CloneItineraryItems_TestArray_ExpectShallowCopy', () => {
   const items = [{ name: 'Zoomobile' }];

   const cloned = ItineraryDraftModel.cloneItineraryItems(items);

   assert.deepEqual(cloned, items);
   assert.notEqual(cloned, items);
});
