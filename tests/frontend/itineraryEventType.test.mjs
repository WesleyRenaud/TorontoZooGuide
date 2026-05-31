import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { getItineraryRequest } from '../../scripts/api/itineraryApi.js';
import {
   buildSchedulableEventTypes,
   isItineraryVisitBoundaryEventType,
   normalizeVisitBoundaryEventTypes,
} from '../../scripts/itinerary/itineraryEventTypes.js';

const BACKEND_ITINERARY_CONFIG = {
   animal_visibility_change_threshold: 20,
   itinerary_event_types: [
      'arrival',
      'breakfast',
      'break',
      'departure',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ],
   itinerary_visit_boundary_event_types: {
      arrival: 'arrival',
      departure: 'departure',
   },
   itinerary_error_types: {
      SUCCESS: 'success',
   },
   suppressed_error_types: [],
};

afterEach(() => {
   delete globalThis.fetch;
});

function mockJsonResponse(payload) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify(payload),
   };
}

test('getItineraryRequest maps visit boundary event types from backend config', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      itinerary: { date: '2026-06-20' },
      itinerary_config: BACKEND_ITINERARY_CONFIG,
   });

   const result = await getItineraryRequest();

   assert.deepEqual(result.itineraryConfig.visitBoundaryEventTypes, {
      arrival: 'arrival',
      departure: 'departure',
   });
});

test('buildSchedulableEventTypes excludes visit boundary types from config', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
      visitBoundaryEventTypes: {
         arrival: 'arrival',
         departure: 'departure',
      },
   };

   assert.deepEqual(buildSchedulableEventTypes(itineraryConfig), [
      'breakfast',
      'break',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ]);
   assert.equal(
      isItineraryVisitBoundaryEventType(
         'arrival',
         itineraryConfig.visitBoundaryEventTypes
      ),
      true
   );
   assert.equal(
      isItineraryVisitBoundaryEventType(
         'lunch',
         itineraryConfig.visitBoundaryEventTypes
      ),
      false
   );
});

test('normalizeVisitBoundaryEventTypes tolerates missing config', () => {
   assert.deepEqual(normalizeVisitBoundaryEventTypes(), {
      arrival: '',
      departure: '',
   });
});
