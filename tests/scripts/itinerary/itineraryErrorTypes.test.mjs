import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../scripts/strings.js';

function _withSuppressedErrorTypes(suppressedErrorTypes, run) {
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({ suppressedErrorTypes });
   try {
      return run();
   } finally {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
}

test('Test_SyncSuppressedItineraryErrorTypes_TestSuppressed_ExpectHydrated', () => {
   _withSuppressedErrorTypes([ItineraryErrorType.SAVE_FAILED], () => {
      assert.equal(ItineraryErrorTypes.isItineraryErrorSuppressed(ItineraryErrorType.SAVE_FAILED), true);
      assert.equal(ItineraryErrorTypes.isItineraryErrorSuppressed(ItineraryErrorType.SUCCESS), false);
   });
});

test('Test_SyncSuppressedItineraryErrorTypes_TestMissingConfig_ExpectEmptySuppressed', () => {
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes();
   try {
      assert.deepEqual(ItineraryErrorTypes.suppressedItineraryErrorTypes, []);
   } finally {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
});

test('Test_IsItinerarySuccess_TestStatuses_ExpectSuccessOnly', () => {
   assert.equal(ItineraryErrorTypes.isItinerarySuccess(ItineraryErrorType.SUCCESS), true);
   assert.equal(ItineraryErrorTypes.isItinerarySuccess(ItineraryErrorType.SAVE_FAILED), false);
});

test('Test_RequiresConfirmations_TestSuppressedAndActive_ExpectFlags', () => {
   _withSuppressedErrorTypes(
      [
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ],
      () => {
         assert.equal(
            ItineraryErrorTypes.requiresShortVisitConfirmation(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(ItineraryErrorType.ITEM_NOT_ON_ITINERARY),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation(
               ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(
               ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(
               ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation(ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(
               ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(
               ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
            ),
            true
         );
      }
   );
});

test('Test_RequiresConfirmations_TestUnsuppressed_ExpectFlags', () => {
   _withSuppressedErrorTypes([], () => {
      assert.equal(
         ItineraryErrorTypes.requiresShortVisitConfirmation(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE),
         true
      );
      assert.equal(
         ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP),
         true
      );
      assert.equal(
         ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(ItineraryErrorType.ITEM_NOT_ON_ITINERARY),
         true
      );
   });
});

test('Test_ResolveItineraryErrorMessage_TestKnownAndUnknown_ExpectStrings', () => {
   const strings = Strings.itinerary.errors;

   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ITINERARY_DATE_NOT_SET),
      strings.itineraryDateNotSet
   );
   assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.SAVE_FAILED), strings.saveFailed);
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.TIME_ORDER_INVALID),
      strings.timeOrderInvalid
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE),
      strings.arrivalDepartureTooClose
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP),
      strings.earlyAdmissionRequiresMembership
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.NO_AVAILABLE_SLOT),
      strings.noAvailableSlot
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE),
      strings.requestedTimeNotAvailable
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS),
      strings.attractionOutsideOperatingHours
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ITEM_NOT_ON_ITINERARY),
      strings.itemNotOnItinerary
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ITEM_ALREADY_SCHEDULED),
      strings.itemAlreadyScheduled
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.TIME_OUT_OF_BOUNDS),
      strings.timeOutOfBounds
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE),
      strings.activityNotOnDaySchedule
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE),
      strings.scheduleWindowUnavailable
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED),
      strings.bulkScheduleItineraryAlreadyScheduled
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage(ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED),
      strings.unscheduleAllNothingScheduled
   );
   assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('unknown'), strings.generic);
});

test('Test_NormalizeItineraryErrorType_TestExplicitType_ExpectTrimmed', () => {
   assert.equal(
      ItineraryErrorTypes.normalizeItineraryErrorType('  saveFailed  ', true),
      'saveFailed'
   );
});

test('Test_NormalizeItineraryErrorType_TestLegacySuccessFlag_ExpectMapped', () => {
   assert.equal(
      ItineraryErrorTypes.normalizeItineraryErrorType('', false),
      'saveFailed'
   );
   assert.equal(
      ItineraryErrorTypes.normalizeItineraryErrorType('', true),
      'success'
   );
});

test('Test_NormalizeItineraryErrorTypeFromResponse_TestDelegates_ExpectNormalize', () => {
   const original = ItineraryErrorTypes.normalizeItineraryErrorType;
   ItineraryErrorTypes.normalizeItineraryErrorType = (status, success) => `${status}:${success}`;
   try {
      assert.equal(
         ItineraryErrorTypes.normalizeItineraryErrorTypeFromResponse({ status: 'x', success: false }),
         'x:false'
      );
   } finally {
      ItineraryErrorTypes.normalizeItineraryErrorType = original;
   }
});
