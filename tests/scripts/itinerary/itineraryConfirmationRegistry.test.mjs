import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryConfirmationRegistry } from '../../../scripts/itinerary/itineraryConfirmationRegistry.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { AttractionOutsideOperatingHoursFragment } from '../../../scripts/itinerary/panel/attractionOutsideOperatingHoursFragment.js';
import { AttractionWithoutAnimalFragment } from '../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { ScheduleItemNotOnItineraryFragment } from '../../../scripts/itinerary/panel/scheduleItemNotOnItineraryFragment.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../scripts/shared/enums/position.js';

function _withSuppressedErrorTypes(suppressedErrorTypes, run) {
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({ suppressedErrorTypes });
   try {
      return run();
   } finally {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
}


test('Test_GetConfirmationEntry_TestItemNotOnItinerary_ExpectFragment', () => {
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(
      entry.showConfirmation,
      ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation
   );
});


test('Test_GetConfirmationEntry_TestAttractionOutsideOperatingHours_ExpectFragment', () => {
   const errorType = ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(
      entry.showConfirmation,
      AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation
   );
});


test('Test_GetConfirmationEntry_TestAttractionWithoutAnimal_ExpectFragment', () => {
   const errorType = ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(
      entry.showConfirmation,
      AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation
   );
});


test('Test_GetConfirmationEntry_TestEarlyAdmission_ExpectFragment', () => {
   const errorType = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(
      entry.showConfirmation,
      EarlyAdmissionFragment.showEarlyAdmissionConfirmation
   );
});


test('Test_GetConfirmationEntry_TestSaveFailed_ExpectNull', () => {
   const errorType = ItineraryErrorType.SAVE_FAILED;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(entry, null);
});


test('Test_GetScheduleItemConfirmationEntries_TestOrder_ExpectBeforeWarningsThenAfter', () => {
   const beforeWarnings = ItineraryConfirmationRegistry.getScheduleItemConfirmationEntriesBeforeWarnings();
   const afterWarnings = ItineraryConfirmationRegistry.getScheduleItemConfirmationEntriesAfterWarnings();

   const entries = ItineraryConfirmationRegistry.getScheduleItemConfirmationEntries();

   assert.deepEqual(entries, [...beforeWarnings, ...afterWarnings]);
});


test('Test_GetSetItineraryConfirmationEntries_TestFlags_ExpectConfirmFlags', () => {
   const expectedFlags = Object.values(
      ItineraryConfirmationRegistry.SET_ITINERARY_CONFIRMATIONS
   ).map((entry) => entry.confirmFlag);

   const flags = ItineraryConfirmationRegistry.getSetItineraryConfirmationEntries().map(
      (entry) => entry.confirmFlag
   );

   assert.deepEqual(flags, expectedFlags);
});


test('Test_GetTimeChangeConfirmationEntries_TestFragments_ExpectEarlyThenShort', () => {
   const earlyAdmission = ItineraryConfirmationRegistry.TIME_CHANGE_CONFIRMATIONS[
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
   ];
   const shortVisit = ItineraryConfirmationRegistry.TIME_CHANGE_CONFIRMATIONS[
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   ];

   const entries = ItineraryConfirmationRegistry.getTimeChangeConfirmationEntries();

   assert.equal(
      entries[Position.FIRST].showConfirmation,
      earlyAdmission.showConfirmation
   );
   assert.equal(
      entries[Position.SECOND].showConfirmation,
      shortVisit.showConfirmation
   );
});


test('Test_BuildTimeChangeConfirmationOptions_TestEarlyAdmission_ExpectOptions', () => {
   const entry = ItineraryConfirmationRegistry.TIME_CHANGE_CONFIRMATIONS[
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
   ];

   const options = ItineraryConfirmationRegistry.buildTimeChangeConfirmationOptions(entry);

   assert.equal(options.showConfirmation, entry.showConfirmation);
   assert.equal(options.suppressionType, entry.suppressKey);
   assert.equal(options.confirmationOptions[entry.confirmFlag], true);
});


test('Test_RequiresConfirmation_TestSuppressedItemNotOnItinerary_ExpectFalse', () => {
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   _withSuppressedErrorTypes([errorType], () => {
      const requiresConfirmation = ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         errorType,
         ItineraryErrorTypes.isItineraryErrorSuppressed
      );

      assert.equal(requiresConfirmation, false);
   });
});


test('Test_RequiresConfirmation_TestSuppressedShortVisit_ExpectFalse', () => {
   const errorType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;

   _withSuppressedErrorTypes([errorType], () => {
      const requiresConfirmation = ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         errorType,
         ItineraryErrorTypes.isItineraryErrorSuppressed
      );

      assert.equal(requiresConfirmation, false);
   });
});


test('Test_RequiresConfirmation_TestUnsuppressedLongWait_ExpectTrue', () => {
   const errorType = ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;

   _withSuppressedErrorTypes(
      [
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      ],
      () => {
         const requiresConfirmation = ItineraryConfirmationRegistry.requiresConfirmation(
            errorType,
            errorType
         );

         assert.equal(requiresConfirmation, true);
      }
   );
});


test('Test_BuildConfirmedOptions_TestFlag_ExpectTrue', () => {
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   const options = ItineraryConfirmationRegistry.buildConfirmedOptions(entry)();

   assert.equal(options[entry.confirmFlag], true);
});


test('Test_BuildConfirmedPayload_TestFlag_ExpectMerged', () => {
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   const date = '2026-06-15';
   const payload = { date };
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   const confirmed = ItineraryConfirmationRegistry.buildConfirmedPayload(entry, payload)();

   assert.equal(confirmed.date, date);
   assert.equal(confirmed[entry.confirmFlag], true);
});


test('Test_BuildBeforeConfirm_TestNoSuppressKey_ExpectUndefined', () => {
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(
      ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS
   );

   const beforeConfirm = ItineraryConfirmationRegistry.buildBeforeConfirm(entry);

   assert.equal(beforeConfirm, undefined);
});


test('Test_BuildBeforeConfirm_TestDoNotShowAgainFalse_ExpectNoPersist', async () => {
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const persisted = [];
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   );
   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async (warningType) => {
      persisted.push(warningType);
   };

   try {
      const beforeConfirm = ItineraryConfirmationRegistry.buildBeforeConfirm(entry);
      await beforeConfirm({ doNotShowAgain: false });

      assert.deepEqual(persisted, []);
   } finally {
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
   }
});


test('Test_BuildBeforeConfirm_TestDoNotShowAgainTrue_ExpectPersist', async () => {
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const persisted = [];
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);
   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async (warningType) => {
      persisted.push(warningType);
   };

   try {
      const beforeConfirm = ItineraryConfirmationRegistry.buildBeforeConfirm(entry);
      await beforeConfirm({ doNotShowAgain: true });

      assert.deepEqual(persisted, [errorType]);
   } finally {
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
   }
});


test('Test_ScheduleItemNotOnItineraryEntry_TestMeta_ExpectSaveFailedAndSuppress', () => {
   const errorType = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(errorType);

   assert.equal(entry.resolveConfirmErrorAsSaveFailed, true);
   assert.equal(entry.suppressKey, errorType);
   assert.equal(
      entry.showConfirmation,
      ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation
   );
});
