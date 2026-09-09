import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryConfirmationRegistry } from '../../../scripts/itinerary/itineraryConfirmationRegistry.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { AttractionOutsideOperatingHoursFragment } from '../../../scripts/itinerary/panel/attractionOutsideOperatingHoursFragment.js';
import { AttractionWithoutAnimalFragment } from '../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ScheduleItemNotOnItineraryFragment } from '../../../scripts/itinerary/panel/scheduleItemNotOnItineraryFragment.js';
import { ShortVisitFragment } from '../../../scripts/itinerary/panel/shortVisitFragment.js';
import { WildEncounterUnscheduleFragment } from '../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';

function _withSuppressedErrorTypes(suppressedErrorTypes, run) {
   const originalSuppressed = ItineraryErrorTypes.suppressedItineraryErrorTypes;
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({ suppressedErrorTypes });
   try {
      return run();
   } finally {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = originalSuppressed;
   }
}

test('Test_GetConfirmationEntry_TestKnownTypes_ExpectMappedFragments', () => {
   assert.equal(
      ItineraryConfirmationRegistry.getConfirmationEntry(ItineraryErrorType.ITEM_NOT_ON_ITINERARY).showConfirmation,
      ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation
   );
   assert.equal(
      ItineraryConfirmationRegistry.getConfirmationEntry(
         ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS
      ).showConfirmation,
      AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation
   );
   assert.equal(
      ItineraryConfirmationRegistry.getConfirmationEntry(
         ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
      ).showConfirmation,
      AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation
   );
   assert.equal(
      ItineraryConfirmationRegistry.getConfirmationEntry(
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
      ).showConfirmation,
      EarlyAdmissionFragment.showEarlyAdmissionConfirmation
   );
   assert.equal(
      ItineraryConfirmationRegistry.getConfirmationEntry(ItineraryErrorType.SAVE_FAILED),
      null
   );
});

test('Test_GetScheduleItemConfirmationEntries_TestOrder_ExpectBeforeWarningsThenAfter', () => {
   const entries = ItineraryConfirmationRegistry.getScheduleItemConfirmationEntries();

   assert.deepEqual(
      entries.map((entry) => entry.confirmFlag),
      [
         'confirmingScheduleItemNotOnItinerary',
         'confirmingAttractionOutsideOperatingHours',
         'confirmingGuardiansTalkUnschedule',
         'confirmingGuardiansTalkWithoutAnimal',
         'confirmingFixedTimeItemLongWait',
         'confirmingWildEncounterUnschedule',
      ]
   );
   assert.equal(
      entries[2].showConfirmation,
      GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation
   );
   assert.equal(
      entries[3].showConfirmation,
      GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation
   );
   assert.equal(
      entries[4].showConfirmation,
      FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation
   );
   assert.equal(
      entries[5].showConfirmation,
      WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation
   );
});

test('Test_GetSetItineraryConfirmationEntries_TestFlags_ExpectConfirmFlags', () => {
   assert.deepEqual(
      ItineraryConfirmationRegistry.getSetItineraryConfirmationEntries().map((entry) => entry.confirmFlag),
      [
         'confirmingGuardiansTalkUnschedule',
         'confirmingGuardiansTalkWithoutAnimal',
         'confirmingAttractionWithoutAnimal',
         'confirmingFixedTimeItemLongWait',
         'confirmingWildEncounterUnschedule',
      ]
   );
});

test('Test_GetTimeChangeConfirmationEntries_TestFragments_ExpectEarlyThenShort', () => {
   const entries = ItineraryConfirmationRegistry.getTimeChangeConfirmationEntries();

   assert.equal(entries[0].showConfirmation, EarlyAdmissionFragment.showEarlyAdmissionConfirmation);
   assert.equal(entries[1].showConfirmation, ShortVisitFragment.showShortVisitConfirmation);
   assert.deepEqual(
      ItineraryConfirmationRegistry.buildTimeChangeConfirmationOptions(entries[0]),
      {
         showConfirmation: EarlyAdmissionFragment.showEarlyAdmissionConfirmation,
         suppressionType: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
         confirmationOptions: {
            confirmingEarlyAdmission: true,
         },
      }
   );
});

test('Test_RequiresConfirmation_TestSuppressed_ExpectFalse', () => {
   _withSuppressedErrorTypes(
      [
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
      ],
      () => {
         assert.equal(
            ItineraryConfirmationRegistry.requiresConfirmation(
               ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
               ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
               ItineraryErrorTypes.isItineraryErrorSuppressed
            ),
            false
         );
         assert.equal(
            ItineraryConfirmationRegistry.requiresConfirmation(
               ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
               ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
               ItineraryErrorTypes.isItineraryErrorSuppressed
            ),
            false
         );
         assert.equal(
            ItineraryConfirmationRegistry.requiresConfirmation(
               ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
               ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
            ),
            true
         );
      }
   );
});

test('Test_BuildConfirmedOptions_TestFlag_ExpectTrue', () => {
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   );

   assert.deepEqual(ItineraryConfirmationRegistry.buildConfirmedOptions(entry)(), {
      confirmingGuardiansTalkUnschedule: true,
   });
   assert.deepEqual(
      ItineraryConfirmationRegistry.buildConfirmedPayload(entry, { date: '2026-06-15' })(),
      {
         date: '2026-06-15',
         confirmingGuardiansTalkUnschedule: true,
      }
   );
});

test('Test_BuildBeforeConfirm_TestSuppressKey_ExpectPersist', async () => {
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   );
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const persisted = [];

   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async (warningType) => {
      persisted.push(warningType);
   };

   try {
      assert.equal(
         ItineraryConfirmationRegistry.buildBeforeConfirm(
            ItineraryConfirmationRegistry.getConfirmationEntry(
               ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS
            )
         ),
         undefined
      );

      const beforeConfirm = ItineraryConfirmationRegistry.buildBeforeConfirm(entry);
      await beforeConfirm({ doNotShowAgain: false });
      assert.deepEqual(persisted, []);
      await beforeConfirm({ doNotShowAgain: true });
      assert.deepEqual(persisted, [ItineraryErrorType.ITEM_NOT_ON_ITINERARY]);
   } finally {
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
   }
});

test('Test_ScheduleItemNotOnItineraryEntry_TestMeta_ExpectSaveFailedAndSuppress', () => {
   const entry = ItineraryConfirmationRegistry.getConfirmationEntry(
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   );

   assert.equal(entry.resolveConfirmErrorAsSaveFailed, true);
   assert.equal(entry.suppressKey, ItineraryErrorType.ITEM_NOT_ON_ITINERARY);
   assert.equal(
      entry.showConfirmation,
      ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation
   );
});
