import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_NormalizeItinerary_TestWithConfig_ExpectActiveAndConfig', () => {
   const config = {
      eventTypes: ['lunch'],
      errorTypes: { SUCCESS: 'success' },
      suppressedErrorTypes: [],
   };
   const date = '2026-06-15';
   const animal = { species: 'Amur Tiger', exhibit: 'Tundra Trek' };

   const normalized = ItineraryNormalizer.normalizeItinerary({
      date,
      animals: [animal],
      itineraryConfig: config,
   });

   assert.equal(normalized.itineraryConfig, config);
   assert.equal(normalized.isActive, true);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});


test('Test_NormalizeItinerary_TestScheduledEvents_ExpectPreserved', () => {
   const date = '2026-06-15';
   const event = { event_type: 'lunch', start_time: '12:00', end_time: '12:40' };

   const normalized = ItineraryNormalizer.normalizeItinerary({
      date,
      events: [event],
   });

   assert.deepEqual(normalized.events[Position.FIRST], event);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});


test('Test_NormalizeItinerary_TestDateOnly_ExpectActiveSavedContent', () => {
   const date = '2026-06-15';

   const normalized = ItineraryNormalizer.normalizeItinerary({ date });

   assert.equal(normalized.date, date);
   assert.equal(normalized.isActive, true);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});


test('Test_NormalizeItinerary_TestMissingCollections_ExpectEmptyDefaults', () => {
   const source = {
      animals: 'not-an-array',
      attractions: null,
   };

   const normalized = ItineraryNormalizer.normalizeItinerary(source);

   assert.deepEqual(normalized.animals, []);
   assert.deepEqual(normalized.attractions, []);
   assert.deepEqual(normalized.events, []);
   assert.equal(normalized.itineraryConfig, null);
   assert.deepEqual(normalized.itineraryPath, {
      stops: [],
      legs: [],
      points: [],
   });
   assert.equal(normalized.isActive, false);
});
