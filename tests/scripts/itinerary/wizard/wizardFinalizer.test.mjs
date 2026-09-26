import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardFinalizer } from '../../../../scripts/itinerary/wizard/wizardFinalizer.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { Position } from '../../../../scripts/shared/enums/position.js';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      document.querySelector('.tzg-popup')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-popup')?.remove();
      delete globalThis.localStorage;
   },
});


test('Test_Saves_TestSavesSyncsDraftStateClearsTheMountAnd_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   mountEl.replaceChildren(createDomNode('div', 'wizard-step'));
   const synced = [];
   const done = [];
   const savedItinerary = {
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
   };

   const result = await WizardFinalizer.finalizeItineraryWizard(
      savedItinerary,
      mountEl,
      {
         onDone: (itinerary) => {
            done.push(itinerary);
         },
         deps: {
            normalizeDraft: (draft) => draft,
            shouldShowSaveIssues: () => false,
            saveItineraryFn: async (draft) => draft,
            syncAnimalDraft: (itinerary) => {
               synced.push(itinerary);
            },
         },
      }
   );

   assert.deepEqual(result, savedItinerary);
   assert.deepEqual(synced, [savedItinerary]);
   assert.deepEqual(done, [savedItinerary]);
   assert.equal(mountEl.children.length, 0);
});


test('Test_Shows_TestShowsAWizardErrorPopupWhenSaveFails_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupCalls = [];
   const saveError = 'Save failed';
   const draft = { date: '2026-06-15', animals: ['Lion'] };

   const result = await WizardFinalizer.finalizeItineraryWizard(
      draft,
      mountEl,
      {
         deps: {
            normalizeDraft: (value) => value,
            saveItineraryFn: async () => {
               throw new Error(saveError);
            },
            showWizardPopup: (config) => {
               popupCalls.push(config);
            },
         },
      }
   );

   assert.equal(result, null);
   assert.equal(popupCalls[Position.FIRST].message, saveError);
});


test('Test_Returns_TestReturnsCancelledWhenSaveIsCancelledFromA_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupCalls = [];
   const draft = {
      date: '2026-06-15',
      guardiansTalks: [{ name: 'Arctic Wolf' }],
   };
   const cancelled = { cancelled: true };

   const result = await WizardFinalizer.finalizeItineraryWizard(
      draft,
      mountEl,
      {
         deps: {
            normalizeDraft: (value) => value,
            saveItineraryFn: async () => null,
            showWizardPopup: (config) => {
               popupCalls.push(config);
            },
         },
      }
   );

   assert.deepEqual(result, cancelled);
   assert.equal(popupCalls.length, 0);
});


test('Test_Opens_TestOpensTheSaveIssuesNoticeWhenTheBackend_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const saveIssuesCalls = [];
   const savedItinerary = {
      date: '2026-06-15',
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      saveIssues: [{ type: 'conflict', message: 'Conflict' }],
   };
   const saveCalls = [];
   const overrideDate = '2026-06-16';
   const overrideOptions = { overridingConflictingGuardiansTalks: true };

   await WizardFinalizer.finalizeItineraryWizard(
      savedItinerary,
      mountEl,
      {
         deps: {
            normalizeDraft: (draft) => draft,
            shouldShowSaveIssues: () => true,
            saveItineraryFn: async (draft, options) => {
               saveCalls.push({ draft, options });
               return savedItinerary;
            },
            syncAnimalDraft: () => {},
            showSaveIssuesPopup: (itinerary, options) => {
               saveIssuesCalls.push({ itinerary, options });
            },
         },
      }
   );

   assert.equal(saveIssuesCalls.length, 1);
   assert.deepEqual(saveIssuesCalls[Position.FIRST].itinerary, savedItinerary);
   assert.equal(typeof saveIssuesCalls[Position.FIRST].options.saveFinalItinerary, 'function');

   await saveIssuesCalls[Position.FIRST].options.saveFinalItinerary(
      { date: overrideDate },
      overrideOptions
   );

   assert.equal(saveCalls.length, 2);
   assert.deepEqual(saveCalls[Position.SECOND].options, {
      ...overrideOptions,
      confirmingShortVisit: false,
      confirmingEarlyAdmission: false,
      selectedExhibits: [],
   });
});


test('Test_Returns_TestReturnsCancelledConfirmationResult_ExpectPassthrough', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const cancelled = { cancelled: true, reason: 'user' };
   const draft = { date: '2026-06-15', animals: ['Lion'] };

   const result = await WizardFinalizer.finalizeItineraryWizard(
      draft,
      mountEl,
      {
         deps: {
            normalizeDraft: (value) => value,
            saveItineraryFn: async () => cancelled,
         },
      }
   );

   assert.equal(result, cancelled);
});


test('Test_Saves_TestSavesDateOnlyItineraryWithoutBlocking_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const saved = [];
   const draft = { date: '2026-06-15', animals: [] };

   const result = await WizardFinalizer.finalizeItineraryWizard(
      draft,
      mountEl,
      {
         deps: {
            normalizeDraft: (value) => value,
            shouldShowSaveIssues: () => false,
            saveItineraryFn: async (itinerary) => {
               saved.push(itinerary);
               return itinerary;
            },
            syncAnimalDraft: () => {},
         },
      }
   );

   assert.deepEqual(result, draft);
   assert.deepEqual(saved, [draft]);
   assert.equal(mountEl.children.length, 0);
});
