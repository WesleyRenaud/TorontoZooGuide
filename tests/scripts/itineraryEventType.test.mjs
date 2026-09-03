import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryApi } from '../../scripts/api/itineraryApi.js';
import {
   buildSchedulableEventTypes,
   isItineraryVisitBoundaryEventType,
   isScheduleItemEventType,
   normalizeVisitBoundaryEventTypes,
   requiresRemoveItineraryItemConfirmation,
} from '../../scripts/itinerary/itineraryEventTypes.js';
import { mockJsonResponse } from './helpers/fetchMock.mjs';

const BACKEND_ITINERARY_CONFIG = {
   animal_visibility_change_threshold: 20,
   itinerary_animal_min_likelihood: 40,
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

test('ItineraryApi.getItineraryRequest maps visit boundary event types from backend config', async () => {
   globalThis.fetch = async () => mockJsonResponse({
      itinerary: { date: '2026-06-20' },
      itinerary_config: BACKEND_ITINERARY_CONFIG,
   });

   const result = await ItineraryApi.getItineraryRequest();

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

test('generic itinerary events skip remove confirmation when configured', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
   };

   assert.equal(
      isScheduleItemEventType('lunch', itineraryConfig.eventTypes),
      true
   );
   assert.equal(
      isScheduleItemEventType('break', itineraryConfig.eventTypes),
      true
   );
   assert.equal(
      isScheduleItemEventType('animals', itineraryConfig.eventTypes),
      false
   );
   assert.equal(
      requiresRemoveItineraryItemConfirmation('lunch', itineraryConfig),
      false
   );
   assert.equal(
      requiresRemoveItineraryItemConfirmation('animals', itineraryConfig),
      true
   );
   assert.equal(
      requiresRemoveItineraryItemConfirmation('guardians_talks', itineraryConfig),
      true
   );
   assert.equal(isScheduleItemEventType('lunch'), false);
   assert.equal(requiresRemoveItineraryItemConfirmation('lunch', null), true);
});
