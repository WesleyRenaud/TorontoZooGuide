import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorTypesHelper } from '../../../scripts/itinerary/itineraryErrorTypesHelper.js';
import { Strings } from '../../../scripts/strings.js';

function _withErrorTypes(config, run) {
   const originalTypes = ItineraryErrorTypes.itineraryErrorTypes;
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig(config);
   try {
      return run();
   } finally {
      ItineraryErrorTypes.itineraryErrorTypes = originalTypes;
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
}

test('Test_UpdateItineraryErrorTypesFromConfig_TestConfig_ExpectFrozenTypes', () => {
   _withErrorTypes(
      {
         errorTypes: { SUCCESS: 'ok', SAVE_FAILED: 'save_failed' },
         suppressedErrorTypes: ['save_failed'],
      },
      () => {
         assert.deepEqual(ItineraryErrorTypes.getItineraryErrorTypes(), {
            SUCCESS: 'ok',
            SAVE_FAILED: 'save_failed',
         });
         assert.equal(Object.isFrozen(ItineraryErrorTypes.getItineraryErrorTypes()), true);
         assert.equal(ItineraryErrorTypes.isItineraryErrorSuppressed('save_failed'), true);
         assert.equal(ItineraryErrorTypes.isItinerarySuccess('ok'), true);
      }
   );
});

test('Test_RequiresConfirmations_TestSuppressedAndActive_ExpectFlags', () => {
   _withErrorTypes(
      {
         errorTypes: {
            ARRIVAL_DEPARTURE_TOO_CLOSE: 'close',
            EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'early',
            ITEM_NOT_ON_ITINERARY: 'missing',
            ATTRACTION_OUTSIDE_OPERATING_HOURS: 'hours',
            GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'talk_unschedule',
            FIXED_TIME_ITEM_LONG_WAIT: 'long_wait',
            GUARDIANS_TALK_WITHOUT_ANIMAL: 'talk_animal',
            ATTRACTION_WITHOUT_ANIMAL: 'attraction_animal',
            WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: 'wild_unschedule',
            GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: 'conflict',
         },
         suppressedErrorTypes: ['close', 'early', 'missing'],
      },
      () => {
         assert.equal(ItineraryErrorTypes.requiresShortVisitConfirmation('close'), false);
         assert.equal(ItineraryErrorTypes.requiresEarlyAdmissionConfirmation('early'), false);
         assert.equal(ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation('missing'), false);
         assert.equal(ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation('hours'), true);
         assert.equal(ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation('talk_unschedule'), true);
         assert.equal(ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation('long_wait'), true);
         assert.equal(ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation('talk_animal'), true);
         assert.equal(ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation('attraction_animal'), true);
         assert.equal(ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation('wild_unschedule'), true);
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation('conflict'),
            true
         );
      }
   );
});

test('Test_ResolveItineraryErrorMessage_TestKnownAndUnknown_ExpectStrings', () => {
   _withErrorTypes(
      {
         errorTypes: {
            ITINERARY_DATE_NOT_SET: 'date',
            SAVE_FAILED: 'save',
            TIME_ORDER_INVALID: 'order',
            ARRIVAL_DEPARTURE_TOO_CLOSE: 'close',
            EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'early',
            NO_AVAILABLE_SLOT: 'slot',
            REQUESTED_TIME_NOT_AVAILABLE: 'requested',
            ATTRACTION_OUTSIDE_OPERATING_HOURS: 'hours',
            ITEM_NOT_ON_ITINERARY: 'missing',
            ITEM_ALREADY_SCHEDULED: 'scheduled',
            TIME_OUT_OF_BOUNDS: 'bounds',
            ACTIVITY_NOT_ON_DAY_SCHEDULE: 'activity',
            SCHEDULE_WINDOW_UNAVAILABLE: 'window',
            BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED: 'bulk',
            UNSCHEDULE_ALL_NOTHING_SCHEDULED: 'nothing',
         },
         suppressedErrorTypes: [],
      },
      () => {
         const strings = Strings.itinerary.errors;
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('date'), strings.itineraryDateNotSet);
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('save'), strings.saveFailed);
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('order'), strings.timeOrderInvalid);
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('close'), strings.arrivalDepartureTooClose);
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('early'),
            strings.earlyAdmissionRequiresMembership
         );
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('slot'), strings.noAvailableSlot);
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('requested'),
            strings.requestedTimeNotAvailable
         );
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('hours'),
            strings.attractionOutsideOperatingHours
         );
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('missing'), strings.itemNotOnItinerary);
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('scheduled'), strings.itemAlreadyScheduled);
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('bounds'), strings.timeOutOfBounds);
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('activity'),
            strings.activityNotOnDaySchedule
         );
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('window'),
            strings.scheduleWindowUnavailable
         );
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('bulk'),
            strings.bulkScheduleItineraryAlreadyScheduled
         );
         assert.equal(
            ItineraryErrorTypes.resolveItineraryErrorMessage('nothing'),
            strings.unscheduleAllNothingScheduled
         );
         assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('unknown'), strings.generic);
      }
   );
});

test('Test_NormalizeItineraryErrorTypeFromResponse_TestDelegates_ExpectHelper', () => {
   const original = ItineraryErrorTypesHelper.normalizeItineraryErrorType;
   ItineraryErrorTypesHelper.normalizeItineraryErrorType = (status, success) => `${status}:${success}`;
   try {
      assert.equal(
         ItineraryErrorTypes.normalizeItineraryErrorTypeFromResponse({ status: 'x', success: false }),
         'x:false'
      );
   } finally {
      ItineraryErrorTypesHelper.normalizeItineraryErrorType = original;
   }
});
