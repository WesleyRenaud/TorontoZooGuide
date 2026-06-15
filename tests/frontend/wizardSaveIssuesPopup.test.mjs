import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showWizardSaveIssuesPopup } from '../../scripts/itinerary/wizard/wizardSaveIssuesPopup.js';
import { APP_STRINGS } from '../../scripts/strings.js';

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

test('showWizardSaveIssuesPopup no-ops when there are no save issues', () => {
   const noticeCalls = [];

   showWizardSaveIssuesPopup(
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

test('showWizardSaveIssuesPopup confirms close through proceed confirmation', () => {
   let noticeConfig = null;
   let proceedConfig = null;
   const closeCalls = [];

   showWizardSaveIssuesPopup(savedItinerary, {
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
      APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle
   );
   assert.equal(
      proceedConfig?.message,
      APP_STRINGS.itinerary.confirmation.proceedWithoutConflictSelectionMessage
   );

   proceedConfig?.onConfirm();

   assert.deepEqual(closeCalls, ['closed']);
});

test('showWizardSaveIssuesPopup returns false when conflict selection is unresolved', async () => {
   let noticeConfig = null;

   showWizardSaveIssuesPopup(savedItinerary, {
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

test('showWizardSaveIssuesPopup saves resolved conflicts and closes on confirm', async () => {
   let noticeConfig = null;
   const saveCalls = [];
   const closeCalls = [];
   const resolvedItinerary = {
      ...savedItinerary,
      wildEncounters: [selectedEncounter],
   };

   showWizardSaveIssuesPopup(savedItinerary, {
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
