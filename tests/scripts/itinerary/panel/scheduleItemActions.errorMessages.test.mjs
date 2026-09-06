import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsNoAvailableSlot_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('noAvailableSlot'),
      /No open time slot/
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsRequestedTimeNotAvailable_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('requestedTimeNotAvailable'),
      /That time is not available/
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsItemAlreadyScheduled_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('itemAlreadyScheduled'),
      /already scheduled/i
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsBulkScheduleItineraryAlreadyScheduled_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('bulkScheduleItineraryAlreadyScheduled'),
      /no items to schedule/i
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsUnscheduleAllNothingScheduled_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('unscheduleAllNothingScheduled'),
      /no items to unschedule/i
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsActivityNotOnDaySchedule_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('activityNotOnDaySchedule'),
      /not scheduled on your visit day/i
   );
});

test('Test_ItineraryErrorTypes_TestItineraryErrorTypesResolveItineraryErrorMessageMapsScheduleWindowUnavailable_ExpectOk', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('scheduleWindowUnavailable'),
      /Operating hours are unavailable/i
   );
});
