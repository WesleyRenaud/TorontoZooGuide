import assert from 'node:assert/strict';
import { test } from 'node:test';

import { finalizeItineraryWizard } from '../../scripts/itinerary/wizard/wizardFinalizer.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

test.describe('finalizeItineraryWizard', () => {
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

   test('shows the empty-selection popup when finish is blocked', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupCalls = [];

      const result = await finalizeItineraryWizard(
         { date: '2026-06-15', animals: [] },
         mountEl,
         {
            deps: {
               normalizeDraft: (draft) => draft,
               shouldBlockEmpty: () => true,
               showWizardPopup: (config) => {
                  popupCalls.push(config);
               },
            },
         }
      );

      assert.equal(result, null);
      assert.equal(popupCalls.length, 1);
      assert.equal(
         popupCalls[0].title,
         APP_STRINGS.itinerary.noItemsSelected.title
      );
   });

   test('saves, syncs draft state, clears the mount, and calls onDone', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      mountEl.replaceChildren(createDomNode('div', 'wizard-step'));
      const synced = [];
      const done = [];
      const savedItinerary = {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      };

      const result = await finalizeItineraryWizard(
         savedItinerary,
         mountEl,
         {
            onDone: (itinerary) => {
               done.push(itinerary);
            },
            deps: {
               normalizeDraft: (draft) => draft,
               shouldBlockEmpty: () => false,
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

   test('shows a wizard error popup when save fails', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupCalls = [];

      const result = await finalizeItineraryWizard(
         { date: '2026-06-15', animals: ['Lion'] },
         mountEl,
         {
            deps: {
               normalizeDraft: (draft) => draft,
               shouldBlockEmpty: () => false,
               saveItineraryFn: async () => {
                  throw new Error('Save failed');
               },
               showWizardPopup: (config) => {
                  popupCalls.push(config);
               },
            },
         }
      );

      assert.equal(result, null);
      assert.equal(popupCalls[0].message, 'Save failed');
   });

   test('opens the save-issues notice when the backend returns issues', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const saveIssuesCalls = [];
      const savedItinerary = {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         saveIssues: [{ type: 'conflict', message: 'Conflict' }],
      };

      await finalizeItineraryWizard(
         savedItinerary,
         mountEl,
         {
            deps: {
               normalizeDraft: (draft) => draft,
               shouldBlockEmpty: () => false,
               shouldShowSaveIssues: () => true,
               saveItineraryFn: async () => savedItinerary,
               syncAnimalDraft: () => {},
               showSaveIssuesPopup: (itinerary, options) => {
                  saveIssuesCalls.push({ itinerary, options });
               },
            },
         }
      );

      assert.equal(saveIssuesCalls.length, 1);
      assert.deepEqual(saveIssuesCalls[0].itinerary, savedItinerary);
      assert.equal(typeof saveIssuesCalls[0].options.saveFinalItinerary, 'function');
   });
});
