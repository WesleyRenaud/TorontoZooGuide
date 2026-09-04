import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryApi } from '../../../scripts/api/itineraryApi.js';
import { ItineraryEventTypes } from '../../../scripts/itinerary/itineraryEventTypes.js';
import { mockJsonResponse } from '../helpers/fetchMock.mjs';

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

test('Test_Behavior_TestItineraryApiGetItineraryRequestMapsVisitBoundaryEventTypesFromBackendC_ExpectOk', async () => {
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

test('Test_BuildSchedulableEventTypes_TestExcludesVisitBoundaryTypesFromConfig_ExpectOk', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
      visitBoundaryEventTypes: {
         arrival: 'arrival',
         departure: 'departure',
      },
   };

   assert.deepEqual(ItineraryEventTypes.buildSchedulableEventTypes(itineraryConfig), [
      'breakfast',
      'break',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ]);
   assert.equal(
      ItineraryEventTypes.isItineraryVisitBoundaryEventType(
         'arrival',
         itineraryConfig.visitBoundaryEventTypes
      ),
      true
   );
   assert.equal(
      ItineraryEventTypes.isItineraryVisitBoundaryEventType(
         'lunch',
         itineraryConfig.visitBoundaryEventTypes
      ),
      false
   );
});

test('Test_NormalizeVisitBoundaryEventTypes_TestToleratesMissingConfig_ExpectOk', () => {
   assert.deepEqual(ItineraryEventTypes.normalizeVisitBoundaryEventTypes(), {
      arrival: '',
      departure: '',
   });
});

test('Test_Generic_TestItineraryEventsSkipRemoveConfirmationWhenConfigured_ExpectOk', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
   };

   assert.equal(
      ItineraryEventTypes.isScheduleItemEventType('lunch', itineraryConfig.eventTypes),
      true
   );
   assert.equal(
      ItineraryEventTypes.isScheduleItemEventType('break', itineraryConfig.eventTypes),
      true
   );
   assert.equal(
      ItineraryEventTypes.isScheduleItemEventType('animals', itineraryConfig.eventTypes),
      false
   );
   assert.equal(
      ItineraryEventTypes.requiresRemoveItineraryItemConfirmation('lunch', itineraryConfig),
      false
   );
   assert.equal(
      ItineraryEventTypes.requiresRemoveItineraryItemConfirmation('animals', itineraryConfig),
      true
   );
   assert.equal(
      ItineraryEventTypes.requiresRemoveItineraryItemConfirmation('guardians_talks', itineraryConfig),
      true
   );
   assert.equal(ItineraryEventTypes.isScheduleItemEventType('lunch'), false);
   assert.equal(ItineraryEventTypes.requiresRemoveItineraryItemConfirmation('lunch', null), true);
});
