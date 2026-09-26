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
   const suppressedErrorType = ItineraryErrorType.SAVE_FAILED;

   _withSuppressedErrorTypes([suppressedErrorType], () => {
      const isSuppressed = ItineraryErrorTypes.isItineraryErrorSuppressed(suppressedErrorType);

      assert.equal(isSuppressed, true);
   });
});


test('Test_SyncSuppressedItineraryErrorTypes_TestUnlisted_ExpectNotSuppressed', () => {
   const suppressedErrorType = ItineraryErrorType.SAVE_FAILED;
   const unlistedErrorType = ItineraryErrorType.SUCCESS;

   _withSuppressedErrorTypes([suppressedErrorType], () => {
      const isSuppressed = ItineraryErrorTypes.isItineraryErrorSuppressed(unlistedErrorType);

      assert.equal(isSuppressed, false);
   });
});


test('Test_SyncSuppressedItineraryErrorTypes_TestMissingConfig_ExpectEmptySuppressed', () => {
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes();

   try {
      const suppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;

      assert.deepEqual(suppressed, []);
   } finally {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
});


test('Test_IsItinerarySuccess_TestSuccess_ExpectTrue', () => {
   const errorType = ItineraryErrorType.SUCCESS;

   const isSuccess = ItineraryErrorTypes.isItinerarySuccess(errorType);

   assert.equal(isSuccess, true);
});


test('Test_IsItinerarySuccess_TestSaveFailed_ExpectFalse', () => {
   const errorType = ItineraryErrorType.SAVE_FAILED;

   const isSuccess = ItineraryErrorTypes.isItinerarySuccess(errorType);

   assert.equal(isSuccess, false);
});


test('Test_RequiresShortVisitConfirmation_TestSuppressed_ExpectFalse', () => {
   const errorType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;

   _withSuppressedErrorTypes([errorType], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresShortVisitConfirmation(errorType);

      assert.equal(requiresConfirmation, false);
   });
});


test('Test_RequiresEarlyAdmissionConfirmation_TestSuppressed_ExpectFalse', () => {
   const errorType = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;

   _withSuppressedErrorTypes([errorType], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(errorType);

      assert.equal(requiresConfirmation, false);
   });
});


test('Test_RequiresScheduleItemNotOnItineraryConfirmation_TestSuppressed_ExpectFalse', () => {
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   _withSuppressedErrorTypes([errorType], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, false);
   });
});


test('Test_RequiresAttractionOutsideOperatingHoursConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresGuardiansTalkUnscheduleConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresFixedTimeItemLongWaitConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresGuardiansTalkWithoutAnimalConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresAttractionWithoutAnimalConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresWildEncounterUnscheduleConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresGuardiansTalkWildEncounterTimeConflictConfirmation_TestActive_ExpectTrue', () => {
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresShortVisitConfirmation_TestUnsuppressed_ExpectTrue', () => {
   const errorType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresShortVisitConfirmation(errorType);

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresEarlyAdmissionConfirmation_TestUnsuppressed_ExpectTrue', () => {
   const errorType = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(errorType);

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_RequiresScheduleItemNotOnItineraryConfirmation_TestUnsuppressed_ExpectTrue', () => {
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   _withSuppressedErrorTypes([], () => {
      const requiresConfirmation = ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(
         errorType
      );

      assert.equal(requiresConfirmation, true);
   });
});


test('Test_ResolveItineraryErrorMessage', () => {
   const strings = Strings.itinerary.errors;
   const cases = [
      [ItineraryErrorType.ITINERARY_DATE_NOT_SET, strings.itineraryDateNotSet],
      [ItineraryErrorType.SAVE_FAILED, strings.saveFailed],
      [ItineraryErrorType.TIME_ORDER_INVALID, strings.timeOrderInvalid],
      [ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, strings.arrivalDepartureTooClose],
      [ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP, strings.earlyAdmissionRequiresMembership],
      [ItineraryErrorType.NO_AVAILABLE_SLOT, strings.noAvailableSlot],
      [ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE, strings.requestedTimeNotAvailable],
      [ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS, strings.attractionOutsideOperatingHours],
      [ItineraryErrorType.ITEM_NOT_ON_ITINERARY, strings.itemNotOnItinerary],
      [ItineraryErrorType.ITEM_ALREADY_SCHEDULED, strings.itemAlreadyScheduled],
      [ItineraryErrorType.TIME_OUT_OF_BOUNDS, strings.timeOutOfBounds],
      [ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE, strings.activityNotOnDaySchedule],
      [ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE, strings.scheduleWindowUnavailable],
      [ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED, strings.bulkScheduleItineraryAlreadyScheduled],
      [ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED, strings.unscheduleAllNothingScheduled],
      ['unknown', strings.generic],
   ];

   cases.forEach(([errorType, message]) => {
      const resolved = ItineraryErrorTypes.resolveItineraryErrorMessage(errorType);

      assert.equal(resolved, message);
   });
});


test('Test_NormalizeItineraryErrorType_TestExplicitType_ExpectTrimmed', () => {
   const errorType = ItineraryErrorType.SAVE_FAILED;
   const value = `  ${errorType}  `;

   const normalized = ItineraryErrorTypes.normalizeItineraryErrorType(value, true);

   assert.equal(normalized, errorType);
});


test('Test_NormalizeItineraryErrorType_TestLegacyFailure_ExpectSaveFailed', () => {
   const errorType = '';
   const legacySuccess = false;

   const normalized = ItineraryErrorTypes.normalizeItineraryErrorType(errorType, legacySuccess);

   assert.equal(normalized, ItineraryErrorType.SAVE_FAILED);
});


test('Test_NormalizeItineraryErrorType_TestLegacySuccess_ExpectSuccess', () => {
   const errorType = '';
   const legacySuccess = true;

   const normalized = ItineraryErrorTypes.normalizeItineraryErrorType(errorType, legacySuccess);

   assert.equal(normalized, ItineraryErrorType.SUCCESS);
});


test('Test_NormalizeItineraryErrorTypeFromResponse_TestDelegates_ExpectNormalize', () => {
   const original = ItineraryErrorTypes.normalizeItineraryErrorType;
   const status = 'x';
   const success = false;
   ItineraryErrorTypes.normalizeItineraryErrorType = (nextStatus, nextSuccess) => (
      `${nextStatus}:${nextSuccess}`
   );

   try {
      const normalized = ItineraryErrorTypes.normalizeItineraryErrorTypeFromResponse({
         status,
         success,
      });

      assert.equal(normalized, `${status}:${success}`);
   } finally {
      ItineraryErrorTypes.normalizeItineraryErrorType = original;
   }
});
