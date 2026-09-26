import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
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
   const date = '2026-06-20';
   globalThis.fetch = async () => mockJsonResponse({
      itinerary: { date },
      itinerary_config: BACKEND_ITINERARY_CONFIG,
   });

   const result = await ItineraryClient.getItineraryRequest();

   assert.deepEqual(
      result.itineraryConfig.visitBoundaryEventTypes,
      BACKEND_ITINERARY_CONFIG.itinerary_visit_boundary_event_types
   );
});


test('Test_BuildSchedulableEventTypes_TestExcludesVisitBoundaryTypesFromConfig_ExpectOk', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
      visitBoundaryEventTypes: BACKEND_ITINERARY_CONFIG.itinerary_visit_boundary_event_types,
   };

   const eventTypes = ItineraryEventTypes.buildSchedulableEventTypes(itineraryConfig);

   assert.deepEqual(eventTypes, [
      'breakfast',
      'break',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ]);
});


test('Test_IsItineraryVisitBoundaryEventType_TestArrival_ExpectTrue', () => {
   const visitBoundaryEventTypes = BACKEND_ITINERARY_CONFIG.itinerary_visit_boundary_event_types;
   const eventType = visitBoundaryEventTypes.arrival;

   const isBoundary = ItineraryEventTypes.isItineraryVisitBoundaryEventType(
      eventType,
      visitBoundaryEventTypes
   );

   assert.equal(isBoundary, true);
});


test('Test_IsItineraryVisitBoundaryEventType_TestLunch_ExpectFalse', () => {
   const visitBoundaryEventTypes = BACKEND_ITINERARY_CONFIG.itinerary_visit_boundary_event_types;
   const eventType = 'lunch';

   const isBoundary = ItineraryEventTypes.isItineraryVisitBoundaryEventType(
      eventType,
      visitBoundaryEventTypes
   );

   assert.equal(isBoundary, false);
});


test('Test_NormalizeVisitBoundaryEventTypes_TestToleratesMissingConfig_ExpectOk', () => {
   const visitBoundaryEventTypes = ItineraryEventTypes.normalizeVisitBoundaryEventTypes();

   assert.deepEqual(visitBoundaryEventTypes, {
      arrival: '',
      departure: '',
   });
});


test('Test_IsScheduleItemEventType_TestLunch_ExpectTrue', () => {
   const eventTypes = BACKEND_ITINERARY_CONFIG.itinerary_event_types;
   const eventType = 'lunch';

   const isEventType = ItineraryEventTypes.isScheduleItemEventType(eventType, eventTypes);

   assert.equal(isEventType, true);
});


test('Test_IsScheduleItemEventType_TestBreak_ExpectTrue', () => {
   const eventTypes = BACKEND_ITINERARY_CONFIG.itinerary_event_types;
   const eventType = 'break';

   const isEventType = ItineraryEventTypes.isScheduleItemEventType(eventType, eventTypes);

   assert.equal(isEventType, true);
});


test('Test_IsScheduleItemEventType_TestAnimals_ExpectFalse', () => {
   const eventTypes = BACKEND_ITINERARY_CONFIG.itinerary_event_types;
   const eventType = 'animals';

   const isEventType = ItineraryEventTypes.isScheduleItemEventType(eventType, eventTypes);

   assert.equal(isEventType, false);
});


test('Test_RequiresRemoveItineraryItemConfirmation_TestLunch_ExpectFalse', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
   };
   const itemType = 'lunch';

   const requiresConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation(
      itemType,
      itineraryConfig
   );

   assert.equal(requiresConfirmation, false);
});


test('Test_RequiresRemoveItineraryItemConfirmation_TestAnimals_ExpectTrue', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
   };
   const itemType = 'animals';

   const requiresConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation(
      itemType,
      itineraryConfig
   );

   assert.equal(requiresConfirmation, true);
});


test('Test_RequiresRemoveItineraryItemConfirmation_TestGuardiansTalks_ExpectTrue', () => {
   const itineraryConfig = {
      eventTypes: BACKEND_ITINERARY_CONFIG.itinerary_event_types,
   };
   const itemType = 'guardians_talks';

   const requiresConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation(
      itemType,
      itineraryConfig
   );

   assert.equal(requiresConfirmation, true);
});


test('Test_IsScheduleItemEventType_TestMissingConfig_ExpectFalse', () => {
   const eventType = 'lunch';

   const isEventType = ItineraryEventTypes.isScheduleItemEventType(eventType);

   assert.equal(isEventType, false);
});


test('Test_RequiresRemoveItineraryItemConfirmation_TestNullConfig_ExpectTrue', () => {
   const itemType = 'lunch';

   const requiresConfirmation = ItineraryEventTypes.requiresRemoveItineraryItemConfirmation(
      itemType,
      null
   );

   assert.equal(requiresConfirmation, true);
});
