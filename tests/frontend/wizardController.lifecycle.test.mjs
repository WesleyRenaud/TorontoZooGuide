import assert from 'node:assert/strict';
import { test } from 'node:test';

import { openItineraryWizard } from '../../scripts/itinerary/wizard/wizardController.js';
import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';
import { SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';
import { makeNoonDate } from './helpers/visitDateMock.mjs';
import {
   createStubStepController,
   syncedSelection,
} from './helpers/wizardTestFixtures.mjs';

test.describe('openItineraryWizard lifecycle', () => {
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

   test('clears stale region selection storage when opening without an active itinerary', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      localStorage.setItem(
         SELECTED_EXHIBITS_KEY,
         JSON.stringify(['Africa Savanna'])
      );

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => ({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
               isActive: false,
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            syncAnimalDraft: () => {},
         },
      });

      assert.equal(localStorage.getItem(SELECTED_EXHIBITS_KEY), null);
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

   test('finish does not call onDone after save because itineraryUpdated handles refresh', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const doneCalls = [];
      let finishHandler = null;

      await openItineraryWizard({
         mountEl,
         onDone: () => {
            doneCalls.push('done');
         },
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => createItineraryWizardState({}),
            createDateStepController: ({ onFinish }) => {
               finishHandler = onFinish;
               return { show() {} };
            },
            selectionStepConfigs: [],
            finalizeWizard: async (_draft, _mountEl, { onDone }) => {
               onDone?.({ date: '2026-06-15' });
               return { date: '2026-06-15' };
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      await finishHandler?.('2026-06-15');

      assert.deepEqual(doneCalls, []);
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
});
