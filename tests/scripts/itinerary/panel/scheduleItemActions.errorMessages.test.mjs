import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { Strings } from '../../../../scripts/strings.js';
import { installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();


test('Test_ResolveItineraryErrorMessage_TestNoAvailableSlot_ExpectMessage', () => {
   const errorType = ItineraryErrorType.NO_AVAILABLE_SLOT;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestRequestedTimeNotAvailable_ExpectMessage', () => {
   const errorType = ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestItemAlreadyScheduled_ExpectMessage', () => {
   const errorType = ItineraryErrorType.ITEM_ALREADY_SCHEDULED;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestBulkAlreadyScheduled_ExpectMessage', () => {
   const errorType = ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestUnscheduleAllNothingScheduled_ExpectMessage', () => {
   const errorType = ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestActivityNotOnDaySchedule_ExpectMessage', () => {
   const errorType = ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});


test('Test_ResolveItineraryErrorMessage_TestScheduleWindowUnavailable_ExpectMessage', () => {
   const errorType = ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE;

   const message = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

   assert.equal(
      message,
      Strings.itinerary.errors[ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType]]
   );
});
