import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryItemFormatterHelper } from '../../../../scripts/itinerary/panel/itineraryItemFormatterHelper.js';


test('Test_AsObject_TestObject_ExpectSameReference', () => {
   const carousel = { name: 'Conservation Carousel' };

   const object = ItineraryItemFormatterHelper.asObject(carousel);

   assert.equal(object, carousel);
});


test('Test_AsObject_TestNull_ExpectEmptyObject', () => {
   const value = null;

   const object = ItineraryItemFormatterHelper.asObject(value);

   assert.deepEqual(object, {});
});


test('Test_NormalizeMaximumDuration_TestPositive_ExpectNumber', () => {
   const value = 30;

   const duration = ItineraryItemFormatterHelper.normalizeMaximumDuration(value);

   assert.equal(duration, value);
});


test('Test_NormalizeMaximumDuration_TestZero_ExpectNull', () => {
   const value = 0;

   const duration = ItineraryItemFormatterHelper.normalizeMaximumDuration(value);

   assert.equal(duration, null);
});


test('Test_NormalizeMaximumDuration_TestNonNumeric_ExpectNull', () => {
   const value = 'bad';

   const duration = ItineraryItemFormatterHelper.normalizeMaximumDuration(value);

   assert.equal(duration, null);
});


test('Test_NormalizeItineraryNameForSave_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Conservation Carousel';
   const value = `  ${name}  `;

   const saved = ItineraryItemFormatterHelper.normalizeItineraryNameForSave(value);

   assert.equal(saved, name);
});


test('Test_NormalizeItineraryNameForSave_TestObject_ExpectTrimmedName', () => {
   const name = 'Zoomobile';
   const value = { name: `  ${name}  ` };

   const saved = ItineraryItemFormatterHelper.normalizeItineraryNameForSave(value);

   assert.equal(saved, name);
});
