import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryErrorTypes } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installScheduleItemActionsTestHooks } from './helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps noAvailableSlot', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('noAvailableSlot'),
      /No open time slot/
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps requestedTimeNotAvailable', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('requestedTimeNotAvailable'),
      /That time is not available/
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps itemAlreadyScheduled', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('itemAlreadyScheduled'),
      /already scheduled/i
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps bulkScheduleItineraryAlreadyScheduled', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('bulkScheduleItineraryAlreadyScheduled'),
      /no items to schedule/i
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps unscheduleAllNothingScheduled', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('unscheduleAllNothingScheduled'),
      /no items to unschedule/i
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps activityNotOnDaySchedule', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('activityNotOnDaySchedule'),
      /not scheduled on your visit day/i
   );
});

test('ItineraryErrorTypes.resolveItineraryErrorMessage maps scheduleWindowUnavailable', () => {
   assert.match(
      ItineraryErrorTypes.resolveItineraryErrorMessage('scheduleWindowUnavailable'),
      /Operating hours are unavailable/i
   );
});
