import assert from 'node:assert/strict';
import { test } from 'node:test';

import { resolveItineraryErrorMessage } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installScheduleItemActionsTestHooks } from './helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('resolveItineraryErrorMessage maps noAvailableSlot', () => {
   assert.match(
      resolveItineraryErrorMessage('noAvailableSlot'),
      /No open time slot/
   );
});

test('resolveItineraryErrorMessage maps requestedTimeNotAvailable', () => {
   assert.match(
      resolveItineraryErrorMessage('requestedTimeNotAvailable'),
      /That time is not available/
   );
});

test('resolveItineraryErrorMessage maps itemAlreadyScheduled', () => {
   assert.match(
      resolveItineraryErrorMessage('itemAlreadyScheduled'),
      /already scheduled/i
   );
});

test('resolveItineraryErrorMessage maps bulkScheduleItineraryAlreadyScheduled', () => {
   assert.match(
      resolveItineraryErrorMessage('bulkScheduleItineraryAlreadyScheduled'),
      /no items to schedule/i
   );
});

test('resolveItineraryErrorMessage maps unscheduleAllNothingScheduled', () => {
   assert.match(
      resolveItineraryErrorMessage('unscheduleAllNothingScheduled'),
      /no items to unschedule/i
   );
});

test('resolveItineraryErrorMessage maps activityNotOnDaySchedule', () => {
   assert.match(
      resolveItineraryErrorMessage('activityNotOnDaySchedule'),
      /not scheduled on your visit day/i
   );
});

test('resolveItineraryErrorMessage maps scheduleWindowUnavailable', () => {
   assert.match(
      resolveItineraryErrorMessage('scheduleWindowUnavailable'),
      /Operating hours are unavailable/i
   );
});
