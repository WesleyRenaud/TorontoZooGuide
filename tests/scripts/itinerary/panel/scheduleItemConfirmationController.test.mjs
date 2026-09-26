import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../../scripts/api/itineraryClient.js';
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
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

function _installConfirmationMocks({ errorType, issues, helperResult } = {}) {
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
   ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation = () => false;
   ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = () => false;
   ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = () => false;
   ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = () => false;
   ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = () => false;
   ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = () => false;
   ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = () => false;
   ItineraryClient.scheduleItineraryItemRequest = async () => (
      issues === undefined ? { errorType } : { errorType, issues }
   );
   ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation = async (options) => {
      helperCalls.push(options);
      return helperResult ?? { confirmed: options.showConfirmation.name || 'confirmed' };
   };
   ScheduleItemConfirmationFlowHelper.getConfirmationMountEl = () => ({ mount: true });
   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async () => {};
   ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings = () => ({ multi: true });

   return {
      helperCalls,
      restore() {
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
      },
   };
}


test('Test_CreateScheduleItemSaveFailedResult_TestDefault_ExpectSaveFailedType', () => {
   const result = ScheduleItemConfirmationController.createScheduleItemSaveFailedResult();

   assert.deepEqual(result, { errorType: ItineraryErrorType.SAVE_FAILED });
});


test('Test_ScheduleItineraryItemWithConfirmation_TestSuccess_ExpectDispatch', async () => {
   const originalRequest = ItineraryClient.scheduleItineraryItemRequest;
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalDispatch = ItineraryService.dispatchScheduleItineraryItemResult;
   const dispatches = [];
   const successResult = { errorType: ItineraryErrorType.SUCCESS };
   ItineraryClient.scheduleItineraryItemRequest = async () => successResult;
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryService.dispatchScheduleItineraryItemResult = (result) => {
      dispatches.push(result);
   };

   try {
      const result = await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation(
         { id: 1 },
         { a: 1 }
      );

      assert.deepEqual(result, successResult);
      assert.deepEqual(dispatches, [successResult]);
   } finally {
      ItineraryClient.scheduleItineraryItemRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryService.dispatchScheduleItineraryItemResult = originalDispatch;
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestItemNotOnItinerary_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
   });
   ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingScheduleItemNotOnItinerary: true,
      });

      await helperCall.beforeConfirm({ doNotShowAgain: true });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestAttractionOutsideHours_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS,
   });
   ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingAttractionOutsideOperatingHours: true,
      });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestMultipleBuildWarnings_ExpectConfirmation', async () => {
   const issues = ['a', 'b'];
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      issues,
   });
   ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation
      );
      assert.deepEqual(confirmedOptions, { multi: true });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestGuardiansTalkUnschedule_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      issues: [],
   });
   ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingGuardiansTalkUnschedule: true,
      });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestGuardiansTalkWithoutAnimal_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      issues: [],
   });
   ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingGuardiansTalkWithoutAnimal: true,
      });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestFixedTimeItemLongWait_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      issues: [],
   });
   ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingFixedTimeItemLongWait: true,
      });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestWildEncounterUnschedule_ExpectConfirmation', async () => {
   const mocks = _installConfirmationMocks({
      errorType: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      issues: [],
   });
   ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation = () => true;

   try {
      await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 1 });
      const helperCall = mocks.helperCalls.at(Position.FIRST);
      const confirmedOptions = helperCall.buildConfirmedOptions();

      assert.equal(
         helperCall.showConfirmation,
         WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation
      );
      assert.deepEqual(confirmedOptions, {
         confirmingWildEncounterUnschedule: true,
      });
   } finally {
      mocks.restore();
   }
});


test('Test_ScheduleItineraryItemWithConfirmation_TestUnhandledError_ExpectReturned', async () => {
   const errorResult = { errorType: ItineraryErrorType.SAVE_FAILED };
   const mocks = _installConfirmationMocks(errorResult);

   try {
      const result = await ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation({ id: 2 });

      assert.deepEqual(result, errorResult);
   } finally {
      mocks.restore();
   }
});
