import assert from 'node:assert/strict';
import { test } from 'node:test';

import { openItineraryWizard } from '../../scripts/itinerary/wizard/wizardController.js';
import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';
import { makeNoonDate } from './helpers/visitDateMock.mjs';
import {
   createStubStepController,
   syncedSelection,
} from './helpers/wizardTestFixtures.mjs';

test.describe('openItineraryWizard draft sync', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });
   test('syncs the date step draft before closing without unsaved changes', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const doneCalls = [];
      let closeHandler = null;
      const selectedDate = makeNoonDate(2026, 5, 15);

      await openItineraryWizard({
         mountEl,
         onDone: () => {
            doneCalls.push('done');
         },
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => selectedDate,
            createWizardState: () => createItineraryWizardState({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            createDateStepController: ({ onClose }) => {
               closeHandler = onClose;
               return {
                  show() {},
                  getDate: () => selectedDate,
               };
            },
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {
               assert.fail('Expected close without a save prompt');
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();

      assert.deepEqual(doneCalls, ['done']);
      assert.equal(mountEl.children.length, 0);
   });

   test('skips date draft sync when the picker date already matches the wizard', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;
      const selectedDate = makeNoonDate(2026, 5, 15);

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => selectedDate,
            createWizardState: () => {
               const wizard = createItineraryWizardState({
                  date: '2026-06-15',
                  animals: [],
                  attractions: [],
                  guardiansTalks: [],
                  wildEncounters: [],
               });

               wizard.updateSelection('animals', syncedSelection());
               return wizard;
            },
            createDateStepController: ({ onClose }) => {
               closeHandler = onClose;
               return {
                  show() {},
                  getDate: () => selectedDate,
               };
            },
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            showConfirmPopup: (config) => {
               popupConfigs.push(config);
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();

      assert.equal(popupConfigs.length, 1);
   });

   test('skips selection draft sync when the step reports no pending changes', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;

      await openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => {
               const wizard = createItineraryWizardState({
                  date: '',
                  animals: [],
                  attractions: [],
                  guardiansTalks: [],
                  wildEncounters: [],
               });

               wizard.updateSelection('animals', syncedSelection());
               return wizard;
            },
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onClose }) => {
                     closeHandler = onClose;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => syncedSelection(),
                        shouldSkipClosingSelectionSync: () => true,
                     };
                  },
               },
            ],
            finalizeWizard: async () => {},
            showConfirmPopup: (config) => {
               popupConfigs.push(config);
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();

      assert.equal(popupConfigs.length, 1);
   });

   test('does not notify onDone when finalize completes successfully', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const doneCalls = [];
      let finishHandler = null;
      const savedItinerary = {
         date: '2026-06-15',
         animals: [],
         isActive: true,
      };

      await openItineraryWizard({
         mountEl,
         onDone: (itinerary) => {
            doneCalls.push(itinerary);
         },
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'wildEncounters',
                  selectionKey: 'wildEncounters',
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return { show() {} };
                  },
               },
            ],
            finalizeWizard: async (_draft, _mountEl, options) => {
               options.onDone?.(savedItinerary);
               return savedItinerary;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      finishHandler?.([]);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.deepEqual(doneCalls, []);
   });
});
