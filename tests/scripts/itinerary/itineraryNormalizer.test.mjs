import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';

test('Test_NormalizeItinerary_TestWithConfig_ExpectActiveAndConfig', () => {
   const config = {
      eventTypes: ['lunch'],
      errorTypes: { SUCCESS: 'success' },
      suppressedErrorTypes: [],
   };

   const normalized = ItineraryNormalizer.normalizeItinerary({
      date: '2026-06-15',
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      itineraryConfig: config,
   });

   assert.equal(normalized.itineraryConfig, config);
   assert.equal(normalized.isActive, true);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});

test('Test_NormalizeItinerary_TestScheduledEvents_ExpectPreserved', () => {
   const normalized = ItineraryNormalizer.normalizeItinerary({
      date: '2026-06-15',
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   });

   assert.deepEqual(normalized.events, [{
      event_type: 'lunch',
      start_time: '12:00',
      end_time: '12:40',
   }]);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});

test('Test_NormalizeItinerary_TestDateOnly_ExpectActiveSavedContent', () => {
   const normalized = ItineraryNormalizer.normalizeItinerary({
      date: '2026-06-15',
   });

   assert.equal(normalized.isActive, true);
   assert.equal(ItineraryNormalizer.isItineraryEmpty(normalized), false);
});

test('Test_NormalizeItinerary_TestMissingCollections_ExpectEmptyDefaults', () => {
   const normalized = ItineraryNormalizer.normalizeItinerary({
      animals: 'not-an-array',
      attractions: null,
   });

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
