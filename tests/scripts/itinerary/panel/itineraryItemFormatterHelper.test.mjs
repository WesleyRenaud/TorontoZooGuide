import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryItemFormatterHelper } from '../../../../scripts/itinerary/panel/itineraryItemFormatterHelper.js';

test('Test_AsObject_TestValues_ExpectObject', () => {
   const item = { name: 'Carousel' };
   assert.equal(ItineraryItemFormatterHelper.asObject(item), item);
   assert.deepEqual(ItineraryItemFormatterHelper.asObject(null), {});
});

test('Test_NormalizeMaximumDuration_TestValues_ExpectPositiveOrNull', () => {
   assert.equal(ItineraryItemFormatterHelper.normalizeMaximumDuration(30), 30);
   assert.equal(ItineraryItemFormatterHelper.normalizeMaximumDuration(0), null);
   assert.equal(ItineraryItemFormatterHelper.normalizeMaximumDuration('bad'), null);
});

test('Test_NormalizeItineraryNameForSave_TestInputs_ExpectTrimmedName', () => {
   assert.equal(ItineraryItemFormatterHelper.normalizeItineraryNameForSave('  Carousel  '), 'Carousel');
   assert.equal(ItineraryItemFormatterHelper.normalizeItineraryNameForSave({ name: '  Zoomobile  ' }), 'Zoomobile');
});
