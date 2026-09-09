import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../../scripts/api/itineraryClient.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryService } from '../../../../scripts/itinerary/itineraryService.js';
import { PersistItineraryWarningSuppressor } from '../../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { AttractionOutsideOperatingHoursFragment } from '../../../../scripts/itinerary/panel/attractionOutsideOperatingHoursFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsFragment } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsFragment.js';
import { ScheduleItemConfirmationController } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationController.js';
import { ScheduleItemConfirmationFlowHelper } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationFlowHelper.js';
import { ScheduleItemNotOnItineraryFragment } from '../../../../scripts/itinerary/panel/scheduleItemNotOnItineraryFragment.js';
import { WildEncounterUnscheduleFragment } from '../../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';

test('Test_CreateScheduleItemSaveFailedResult_TestDefault_ExpectSaveFailedType', () => {
   assert.deepEqual(
      ScheduleItemConfirmationController.createScheduleItemSaveFailedResult(),
      { errorType: ItineraryErrorType.SAVE_FAILED }
   );
});

test('Test_ScheduleItineraryItemWithConfirmation_TestSuccess_ExpectDispatch', async () => {
   const originalRequest = ItineraryClient.scheduleItineraryItemRequest;
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalDispatch = ItineraryService.dispatchScheduleItineraryItemResult;
   const dispatches = [];

   ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'SUCCESS' });
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryService.dispatchScheduleItineraryItemResult = (result) => dispatches.push(result);

   try {
      const result = await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation(
         { id: 1 },
         { a: 1 }
      );
      assert.deepEqual(result, { errorType: 'SUCCESS' });
      assert.deepEqual(dispatches, [{ errorType: 'SUCCESS' }]);
   } finally {
      ItineraryClient.scheduleItineraryItemRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryService.dispatchScheduleItineraryItemResult = originalDispatch;
   }
});

test('Test_ScheduleItineraryItemWithConfirmation_TestConfirmationBranches_ExpectHelper', async () => {
   const originalRequest = ItineraryClient.scheduleItineraryItemRequest;
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalNotOn = ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation;
   const originalOutside = ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation;
   const originalGuardians = ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation;
   const originalWithout = ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation;
   const originalLongWait = ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation;
   const originalWild = ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation;
   const originalMulti = ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings;
   const originalHelper = ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation;
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const originalMount = ScheduleItemConfirmationFlowHelper.getConfirmationMountEl;
   const originalBuildConfirmed = ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings;
   const helperCalls = [];

   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation = async (options) => {
      helperCalls.push(options);
      return { confirmed: options.showConfirmation.name || 'confirmed' };
   };
   ScheduleItemConfirmationFlowHelper.getConfirmationMountEl = () => ({ mount: true });
   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async () => {};
   ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = () => ({ multi: true });

   const branchOrder = [
      {
         setup() {
            ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation = () => true;
            ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = () => false;
            ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = () => false;
            ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = () => false;
            ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = () => false;
            ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = () => false;
            ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = () => false;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'ITEM_NOT_ON_ITINERARY' });
         },
         expected: ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation,
      },
      {
         setup() {
            ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation = () => false;
            ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'OUTSIDE' });
         },
         expected: AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation,
      },
      {
         setup() {
            ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = () => false;
            ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({
               errorType: 'WARN',
               issues: ['a', 'b'],
            });
         },
         expected: ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation,
      },
      {
         setup() {
            ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = () => false;
            ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'GT', issues: [] });
         },
         expected: GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation,
      },
      {
         setup() {
            ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = () => false;
            ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'GTWA', issues: [] });
         },
         expected: GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation,
      },
      {
         setup() {
            ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = () => false;
            ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'WAIT', issues: [] });
         },
         expected: FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
      },
      {
         setup() {
            ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = () => false;
            ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = () => true;
            ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'WE', issues: [] });
         },
         expected: WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation,
      },
   ];

   try {
      for (const branch of branchOrder) {
         branch.setup();
         await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
         assert.equal(helperCalls.at(-1).showConfirmation, branch.expected);
      }

      const notOnCall = helperCalls[0];
      assert.deepEqual(notOnCall.buildConfirmedOptions(), {
         confirmingScheduleItemNotOnItinerary: true,
      });
      await notOnCall.beforeConfirm({ doNotShowAgain: true });

      assert.deepEqual(helperCalls[1].buildConfirmedOptions(), {
         confirmingAttractionOutsideOperatingHours: true,
      });
      assert.deepEqual(helperCalls[2].buildConfirmedOptions(), { multi: true });
      assert.deepEqual(helperCalls[3].buildConfirmedOptions(), {
         confirmingGuardiansTalkUnschedule: true,
      });
      assert.deepEqual(helperCalls[4].buildConfirmedOptions(), {
         confirmingGuardiansTalkWithoutAnimal: true,
      });
      assert.deepEqual(helperCalls[5].buildConfirmedOptions(), {
         confirmingFixedTimeItemLongWait: true,
      });
      assert.deepEqual(helperCalls[6].buildConfirmedOptions(), {
         confirmingWildEncounterUnschedule: true,
      });

      ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = () => false;
      ItineraryClient.scheduleItineraryItemRequest = async () => ({ errorType: 'OTHER' });
      assert.deepEqual(
         await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 2 }),
         { errorType: 'OTHER' }
      );
   } finally {
      ItineraryClient.scheduleItineraryItemRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation = originalNotOn;
      ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = originalOutside;
      ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = originalGuardians;
      ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = originalWithout;
      ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = originalLongWait;
      ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = originalWild;
      ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = originalMulti;
      ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation = originalHelper;
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
      ScheduleItemConfirmationFlowHelper.getConfirmationMountEl = originalMount;
      ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = originalBuildConfirmed;
   }
});
