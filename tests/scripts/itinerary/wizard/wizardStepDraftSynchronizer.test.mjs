import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardStepDraftSynchronizer } from '../../../../scripts/itinerary/wizard/wizardStepDraftSynchronizer.js';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';


test('Test_ResolveDateStepDraftUpdate_TestInvalidDate_ExpectNull', () => {
   const wizardDate = '2026-06-15';

   const update = WizardStepDraftSynchronizer.resolveDateStepDraftUpdate({
      currentDate: null,
      wizardDate,
   });

   assert.equal(update, null);
});


test('Test_ResolveDateStepDraftUpdate_TestUnchanged_ExpectNull', () => {
   const year = 2026;
   const monthIndex = 5;
   const day = 15;
   const wizardDate = '2026-06-15';

   const update = WizardStepDraftSynchronizer.resolveDateStepDraftUpdate({
      currentDate: makeNoonDate(year, monthIndex, day),
      wizardDate,
   });

   assert.equal(update, null);
});


test('Test_ResolveDateStepDraftUpdate_TestChanged_ExpectDate', () => {
   const year = 2026;
   const monthIndex = 5;
   const day = 16;
   const wizardDate = '2026-06-15';

   const update = WizardStepDraftSynchronizer.resolveDateStepDraftUpdate({
      currentDate: makeNoonDate(year, monthIndex, day),
      wizardDate,
   });

   assert.equal(update, `${year}-06-${day}`);
});


test('Test_ResolveDateStepTimesUpdate_TestUnchanged_ExpectNull', () => {
   const arrivalTime = '10:00 AM';
   const departureTime = '4:00 PM';

   const update = WizardStepDraftSynchronizer.resolveDateStepTimesUpdate({
      currentArrivalTime: arrivalTime,
      currentDepartureTime: departureTime,
      wizardArrivalTime: arrivalTime,
      wizardDepartureTime: departureTime,
   });

   assert.equal(update, null);
});


test('Test_ResolveDateStepTimesUpdate_TestChanged_ExpectTimes', () => {
   const arrivalTime = '10:00 AM';
   const departureTime = '4:00 PM';
   const wizardArrivalTime = '9:30 AM';

   const update = WizardStepDraftSynchronizer.resolveDateStepTimesUpdate({
      currentArrivalTime: arrivalTime,
      currentDepartureTime: departureTime,
      wizardArrivalTime,
      wizardDepartureTime: '',
   });

   assert.deepEqual(update, {
      arrivalTime,
      departureTime,
   });
});


test('Test_ShouldSyncSelectionStepDraft_TestMissingConfig_ExpectFalse', () => {
   const stepController = { getSelectionSnapshot: async () => [] };

   const shouldSync = WizardStepDraftSynchronizer.shouldSyncSelectionStepDraft({
      stepConfig: null,
      stepController,
   });

   assert.equal(shouldSync, false);
});


test('Test_ShouldSyncSelectionStepDraft_TestSkipClosing_ExpectFalse', () => {
   const stepConfig = { selectionKey: 'animals' };
   const stepController = {
      getSelectionSnapshot: async () => [],
      shouldSkipClosingSelectionSync: () => true,
   };

   const shouldSync = WizardStepDraftSynchronizer.shouldSyncSelectionStepDraft({
      stepConfig,
      stepController,
   });

   assert.equal(shouldSync, false);
});


test('Test_ShouldSyncSelectionStepDraft_TestReady_ExpectTrue', () => {
   const stepConfig = { selectionKey: 'animals' };
   const stepController = {
      getSelectionSnapshot: async () => [],
      shouldSkipClosingSelectionSync: () => false,
   };

   const shouldSync = WizardStepDraftSynchronizer.shouldSyncSelectionStepDraft({
      stepConfig,
      stepController,
   });

   assert.equal(shouldSync, true);
});


test('Test_IsWizardDateStep_TestDate_ExpectTrue', () => {
   const stepKey = 'date';

   const isDateStep = WizardStepDraftSynchronizer.isWizardDateStep(stepKey);

   assert.equal(isDateStep, true);
});


test('Test_IsWizardDateStep_TestAnimals_ExpectFalse', () => {
   const stepKey = 'animals';

   const isDateStep = WizardStepDraftSynchronizer.isWizardDateStep(stepKey);

   assert.equal(isDateStep, false);
});
