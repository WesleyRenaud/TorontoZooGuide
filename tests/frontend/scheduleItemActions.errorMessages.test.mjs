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

test('resolveItineraryErrorMessage maps bulkScheduleAnimalsAlreadyScheduled', () => {
   assert.match(
      resolveItineraryErrorMessage('bulkScheduleAnimalsAlreadyScheduled'),
      /already scheduled/
   );
});
