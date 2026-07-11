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

test.describe('openItineraryWizard close flow', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });
   test('syncs the active selection step draft before prompting to save', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;
      const syncedSelection = [{
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }];

      await openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onClose }) => {
                     closeHandler = onClose;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => syncedSelection,
                        shouldSkipClosingSelectionSync: () => false,
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

   test('confirming the save prompt finishes the wizard', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finishCalls = [];
      let closeHandler = null;
      let popupConfig = null;

      await openItineraryWizard({
         mountEl,
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
            createDateStepController: ({ onClose }) => {
               closeHandler = onClose;
               return {
                  show() {},
                  getDate: () => makeNoonDate(2026, 5, 15),
               };
            },
            selectionStepConfigs: [],
            finalizeWizard: async (draft) => {
               finishCalls.push(draft);
               return draft;
            },
            showConfirmPopup: (config) => {
               popupConfig = config;
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();
      popupConfig?.onConfirm?.();

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finishCalls.length, 1);
      assert.equal(finishCalls[0].animals.length, 1);
   });

   test('discarding from the save prompt closes the wizard', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const doneCalls = [];
      let closeHandler = null;
      let popupConfig = null;

      await openItineraryWizard({
         mountEl,
         onDone: () => {
            doneCalls.push('done');
         },
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
            createDateStepController: ({ onClose }) => {
               closeHandler = onClose;
               return {
                  show() {},
                  getDate: () => makeNoonDate(2026, 5, 15),
               };
            },
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            showConfirmPopup: (config) => {
               popupConfig = config;
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();
      popupConfig?.onCancel?.();

      assert.deepEqual(doneCalls, ['done']);
      assert.equal(mountEl.children.length, 0);
   });

   test('selection finish handlers finalize the wizard', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finishCalls = [];
      let finishHandler = null;

      await openItineraryWizard({
         mountEl,
         startAt: 'wildEncounters',
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
            finalizeWizard: async (draft) => {
               finishCalls.push(draft);
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      finishHandler?.(['Great Barrier Reef']);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finishCalls.length, 1);
      assert.deepEqual(finishCalls[0].wildEncounters, ['Great Barrier Reef']);
   });

   test('cancelling finish restores selection storage so close does not prompt to save', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      const stepShows = [];
      let finishHandler = null;
      let closeHandler = null;
      let wizard = null;
      let selectionSnapshot = [{ name: "Grevy's Zebra" }];

      await openItineraryWizard({
         mountEl,
         startAt: 'guardiansTalks',
         deps: {
            loadItinerary: async () => ({
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardiansTalks: [{ name: "Grevy's Zebra" }],
               wildEncounters: [],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: (existing) => {
               wizard = createItineraryWizardState(existing);
               return wizard;
            },
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'guardiansTalks',
                  selectionKey: 'guardiansTalks',
                  factory: ({ onFinish, onClose }) => {
                     finishHandler = onFinish;
                     closeHandler = onClose;
                     return {
                        show() {
                           stepShows.push('guardiansTalks');
                           selectionSnapshot = [...wizard.state.guardiansTalks];
                        },
                        getSelectionSnapshot: async () => selectionSnapshot,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async () => ({ cancelled: true }),
            showConfirmPopup: (config) => {
               popupConfigs.push(config);
            },
            syncAnimalDraft: () => {},
         },
      });

      selectionSnapshot = [
         { name: "Grevy's Zebra" },
         { name: 'Slender-Tailed Meerkat' },
      ];
      finishHandler?.(selectionSnapshot);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(wizard.hasUnsavedChanges(), false);
      assert.ok(stepShows.length >= 2);

      await closeHandler?.();

      assert.equal(popupConfigs.length, 0);
      assert.equal(mountEl.children.length, 0);
   });
});
