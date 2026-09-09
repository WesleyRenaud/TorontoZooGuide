import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorTypesHelper } from '../../../scripts/itinerary/itineraryErrorTypesHelper.js';
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
   _withSuppressedErrorTypes(['saveFailed'], () => {
      assert.equal(ItineraryErrorTypes.isItineraryErrorSuppressed('saveFailed'), true);
      assert.equal(ItineraryErrorTypes.isItineraryErrorSuppressed('success'), false);
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
   assert.equal(ItineraryErrorTypes.isItinerarySuccess('success'), true);
   assert.equal(ItineraryErrorTypes.isItinerarySuccess('saveFailed'), false);
});

test('Test_RequiresConfirmations_TestSuppressedAndActive_ExpectFlags', () => {
   _withSuppressedErrorTypes(
      [
         'arrivalDepartureTooClose',
         'earlyAdmissionRequiresMembership',
         'itemNotOnItinerary',
      ],
      () => {
         assert.equal(
            ItineraryErrorTypes.requiresShortVisitConfirmation('arrivalDepartureTooClose'),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresEarlyAdmissionConfirmation('earlyAdmissionRequiresMembership'),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation('itemNotOnItinerary'),
            false
         );
         assert.equal(
            ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation(
               'attractionOutsideOperatingHours'
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(
               'guardiansTalkWillUnscheduleItems'
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation('fixedTimeItemLongWait'),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(
               'guardiansTalkWithoutAnimal'
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation('attractionWithoutAnimal'),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(
               'wildEncounterWillUnscheduleItems'
            ),
            true
         );
         assert.equal(
            ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(
               'guardiansTalkWildEncounterTimeConflict'
            ),
            true
         );
      }
   );
});

test('Test_RequiresConfirmations_TestUnsuppressed_ExpectFlags', () => {
   _withSuppressedErrorTypes([], () => {
      assert.equal(
         ItineraryErrorTypes.requiresShortVisitConfirmation('arrivalDepartureTooClose'),
         true
      );
      assert.equal(
         ItineraryErrorTypes.requiresEarlyAdmissionConfirmation('earlyAdmissionRequiresMembership'),
         true
      );
      assert.equal(
         ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation('itemNotOnItinerary'),
         true
      );
   });
});

test('Test_ResolveItineraryErrorMessage_TestKnownAndUnknown_ExpectStrings', () => {
   const strings = Strings.itinerary.errors;

   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('itineraryDateNotSet'),
      strings.itineraryDateNotSet
   );
   assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('saveFailed'), strings.saveFailed);
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('timeOrderInvalid'),
      strings.timeOrderInvalid
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('arrivalDepartureTooClose'),
      strings.arrivalDepartureTooClose
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('earlyAdmissionRequiresMembership'),
      strings.earlyAdmissionRequiresMembership
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('noAvailableSlot'),
      strings.noAvailableSlot
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('requestedTimeNotAvailable'),
      strings.requestedTimeNotAvailable
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('attractionOutsideOperatingHours'),
      strings.attractionOutsideOperatingHours
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('itemNotOnItinerary'),
      strings.itemNotOnItinerary
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('itemAlreadyScheduled'),
      strings.itemAlreadyScheduled
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('timeOutOfBounds'),
      strings.timeOutOfBounds
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('activityNotOnDaySchedule'),
      strings.activityNotOnDaySchedule
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('scheduleWindowUnavailable'),
      strings.scheduleWindowUnavailable
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('bulkScheduleItineraryAlreadyScheduled'),
      strings.bulkScheduleItineraryAlreadyScheduled
   );
   assert.equal(
      ItineraryErrorTypes.resolveItineraryErrorMessage('unscheduleAllNothingScheduled'),
      strings.unscheduleAllNothingScheduled
   );
   assert.equal(ItineraryErrorTypes.resolveItineraryErrorMessage('unknown'), strings.generic);
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
