import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardSaveIssuesPopup } from '../../../../scripts/itinerary/wizard/wizardSaveIssuesPopup.js';
import { Strings } from '../../../../scripts/strings.js';

const savedItinerary = {
   date: '2026-06-15',
   animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
   saveIssues: [{
      type: 'wildEncounterTimeConflict',
      items: [{
         name: 'From Howls to Honks',
         start_time: '13:00',
         end_time: '13:45',
      }],
   }],
};

const selectedEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
};

test('Test_ShowWizardSaveIssuesPopup_TestShowWizardSaveIssuesPopupNoOpsWhenThereAreNoSave_ExpectOk', () => {
   const noticeCalls = [];

   WizardSaveIssuesPopup.showWizardSaveIssuesPopup(
      { date: '2026-06-15', saveIssues: [] },
      {
         showNoticePopup: (config) => {
            noticeCalls.push(config);
         },
         saveFinalItinerary: async () => {},
      }
   );

   assert.equal(noticeCalls.length, 0);
});

test('Test_ShowWizardSaveIssuesPopup_TestShowWizardSaveIssuesPopupConfirmsCloseThroughProceedConfirmation_ExpectOk', () => {
   let noticeConfig = null;
   let proceedConfig = null;
   const closeCalls = [];

   WizardSaveIssuesPopup.showWizardSaveIssuesPopup(savedItinerary, {
      createSaveIssues: () => ({
         content: {},
         conflictGroups: [],
      }),
      showNoticePopup: (config) => {
         noticeConfig = config;
      },
      showProceedConfirmation: (config) => {
         proceedConfig = config;
      },
      saveFinalItinerary: async () => {},
   });

   noticeConfig?.onClose({
      close: () => {
         closeCalls.push('closed');
      },
   });

   assert.equal(
      proceedConfig?.title,
      Strings.itinerary.confirmation.closeSaveIssuesTitle
   );
   assert.equal(
      proceedConfig?.message,
      Strings.itinerary.confirmation.proceedWithoutConflictSelectionMessage
   );

   proceedConfig?.onConfirm();

   assert.deepEqual(closeCalls, ['closed']);
});

test('Test_ShowWizardSaveIssuesPopup_TestShowWizardSaveIssuesPopupReturnsFalseWhenConflictSelectionIsUnresolved_ExpectOk', async () => {
   let noticeConfig = null;

   WizardSaveIssuesPopup.showWizardSaveIssuesPopup(savedItinerary, {
      createSaveIssues: () => ({
         content: {},
         conflictGroups: [{ items: [selectedEncounter] }],
      }),
      confirmSaveIssues: async () => false,
      showNoticePopup: (config) => {
         noticeConfig = config;
      },
      showProceedConfirmation: () => {},
      saveFinalItinerary: async () => {},
   });

   const result = await noticeConfig?.onConfirm({
      close: () => {},
   });

   assert.equal(result, false);
});

test('Test_ShowWizardSaveIssuesPopup_TestShowWizardSaveIssuesPopupSavesResolvedConflictsAndClosesOnConfirm_ExpectOk', async () => {
   let noticeConfig = null;
   const saveCalls = [];
   const closeCalls = [];
   const resolvedItinerary = {
      ...savedItinerary,
      wildEncounters: [selectedEncounter],
   };

   WizardSaveIssuesPopup.showWizardSaveIssuesPopup(savedItinerary, {
      createSaveIssues: () => ({
         content: {},
         conflictGroups: [{ items: [selectedEncounter] }],
      }),
      confirmSaveIssues: async (_groups, onResolved) => {
         await onResolved([selectedEncounter]);
         return true;
      },
      buildResolvedItinerary: (_itinerary, selectedItems) => ({
         ...savedItinerary,
         wildEncounters: selectedItems,
      }),
      showNoticePopup: (config) => {
         noticeConfig = config;
      },
      showProceedConfirmation: () => {},
      saveFinalItinerary: async (itinerary, options) => {
         saveCalls.push({ itinerary, options });
      },
   });

   const result = await noticeConfig?.onConfirm({
      close: () => {
         closeCalls.push('closed');
      },
   });

   assert.equal(result, true);
   assert.deepEqual(saveCalls, [{
      itinerary: resolvedItinerary,
      options: { overridingConflictingGuardiansTalks: true },
   }]);
   assert.deepEqual(closeCalls, ['closed']);
});
