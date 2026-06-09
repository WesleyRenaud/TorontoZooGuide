import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   isItineraryEmpty,
   normalizeItinerary,
} from '../../scripts/itinerary/itineraryService.js';
import { installItineraryServiceTestHooks } from './helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('normalizeItinerary exposes itineraryConfig and active state', () => {
   const config = {
      eventTypes: ['lunch'],
      errorTypes: { SUCCESS: 'success' },
      suppressedErrorTypes: [],
   };

   const normalized = normalizeItinerary({
      date: '2026-06-15',
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      itineraryConfig: config,
   });

   assert.equal(normalized.itineraryConfig, config);
   assert.equal(normalized.isActive, true);
   assert.equal(isItineraryEmpty(normalized), false);
});

test('normalizeItinerary preserves scheduled generic events', () => {
   const normalized = normalizeItinerary({
      date: '2026-06-15',
      events: [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }],
   });

   assert.deepEqual(normalized.events, [{
      event_type: 'lunch',
      start_time: '12:00',
      end_time: '12:40',
   }]);
   assert.equal(isItineraryEmpty(normalized), false);
});

test('normalizeItinerary treats missing collections as empty', () => {
   const normalized = normalizeItinerary({
      animals: 'not-an-array',
      attractions: null,
   });

   assert.deepEqual(normalized.animals, []);
   assert.deepEqual(normalized.attractions, []);
   assert.deepEqual(normalized.events, []);
   assert.equal(normalized.itineraryConfig, null);
   assert.equal(normalized.isActive, false);
});
