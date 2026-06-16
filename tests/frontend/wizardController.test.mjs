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

test.describe('openItineraryWizard', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });

   test('no-ops when mountEl is missing', async () => {
      await openItineraryWizard({ mountEl: null });
   });

   test('shows the resolved start step with injected controllers', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      const dateController = createStubStepController('date', shownSteps);

      await openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: () => dateController,
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  prevStepKey: 'regions',
                  nextStepKey: 'attractions',
                  factory: () => createStubStepController('animals', shownSteps),
               },
            ],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      assert.deepEqual(shownSteps, ['animals']);
   });

   test('closes immediately when there are no unsaved changes', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const doneCalls = [];
      let closeHandler = null;
      const dateController = {
         show() {},
         getDate: () => makeNoonDate(2026, 5, 15),
      };

      await openItineraryWizard({
         mountEl,
         onDone: () => {
            doneCalls.push('done');
         },
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: ({ onClose }) => {
               closeHandler = onClose;
               return dateController;
            },
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();

      assert.deepEqual(doneCalls, ['done']);
      assert.equal(mountEl.children.length, 0);
   });

   test('syncs animal draft state for an active itinerary', async () => {
      const syncedItineraries = [];
      const mountEl = createDomNode('div', 'wizard-mount');

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => ({
               isActive: true,
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: (itinerary) => {
               syncedItineraries.push(itinerary);
            },
         },
      });

      assert.equal(syncedItineraries.length, 1);
   });

   test('prompts to save when closing with unsaved changes', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;

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

               wizard.updateSelection('animals', [
                  { species: 'African Lion', exhibit: 'Africa Savanna' },
               ]);

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
               popupConfigs.push(config);
            },
            syncAnimalDraft: () => {},
         },
      });

      await closeHandler?.();

      assert.equal(popupConfigs.length, 1);
      assert.equal(
         popupConfigs[0].title,
         APP_STRINGS.itinerary.confirmation.saveChangesTitle
      );
   });

   test('date save advances to the regions step', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      let saveHandler = null;

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: ({ onSave }) => {
               saveHandler = onSave;
               return {
                  show() {
                     shownSteps.push('date');
                  },
               };
            },
            selectionStepConfigs: [
               {
                  stepKey: 'regions',
                  selectionKey: 'animals',
                  factory: () => ({
                     show() {
                        shownSteps.push('regions');
                     },
                  }),
               },
            ],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      saveHandler?.('2026-06-15');

      assert.deepEqual(shownSteps, ['date', 'regions']);
   });

   test('selection prev handlers return to the previous step', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      let animalsPrevHandler = null;

      await openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: () => ({
               show() {
                  shownSteps.push('date');
               },
            }),
            selectionStepConfigs: [
               {
                  stepKey: 'regions',
                  selectionKey: 'animals',
                  prevStepKey: 'date',
                  nextStepKey: 'animals',
                  factory: () => ({
                     show() {
                        shownSteps.push('regions');
                     },
                  }),
               },
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  prevStepKey: 'regions',
                  factory: ({ onPrev }) => {
                     animalsPrevHandler = onPrev;
                     return {
                        show() {
                           shownSteps.push('animals');
                        },
                     };
                  },
               },
            ],
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      animalsPrevHandler?.([]);

      assert.deepEqual(shownSteps, ['animals', 'regions']);
   });

   test('loads default selection step configs when none are injected', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: () => ({
               show() {
                  shownSteps.push('date');
               },
            }),
            loadSelectionStepConfigs: async () => ([
               {
                  stepKey: 'regions',
                  selectionKey: 'animals',
                  factory: () => ({
                     show() {
                        shownSteps.push('regions');
                     },
                  }),
               },
            ]),
            finalizeWizard: async () => {},
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      assert.deepEqual(shownSteps, ['date']);
   });

   test('date finish saves an empty itinerary with allowEmpty', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      const finishCalls = [];

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: ({ onFinish }) => {
               finishHandler = onFinish;
               return { show() {} };
            },
            selectionStepConfigs: [],
            finalizeWizard: async (draft, _mountEl, options) => {
               finishCalls.push({ draft, options });
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      await finishHandler?.('2026-06-15');

      assert.equal(finishCalls.length, 1);
      assert.equal(finishCalls[0].draft.date, '2026-06-15');
      assert.equal(finishCalls[0].options.allowEmpty, true);
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

   test('notifies onDone when finalize completes successfully', async () => {
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

      assert.deepEqual(doneCalls, [savedItinerary]);
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
});

