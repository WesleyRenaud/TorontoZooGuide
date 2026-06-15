import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { openItineraryWizard } from '../../scripts/itinerary/wizard/wizardController.js';
import { buildWizardDraft } from '../../scripts/itinerary/wizard/wizardDraft.js';
import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function createLocalStorageMock() {
   const values = new Map();

   return {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => {
         values.set(key, String(value));
      },
      removeItem: (key) => {
         values.delete(key);
      },
   };
}

function makeNoonDate(year, monthIndex, day) {
   return new Date(year, monthIndex, day, 12, 0, 0, 0);
}

function createStubStepController(stepKey, shownSteps) {
   return {
      show() {
         shownSteps.push(stepKey);
      },
      getSelectionSnapshot: async () => [],
      shouldSkipClosingSelectionSync: () => true,
   };
}

test('buildWizardDraft preserves itinerary times when changing date', () => {
   assert.deepEqual(
      buildWizardDraft(
         {
            date: '2026-06-13',
            arrivalTime: '09:15',
            departureTime: '17:00',
            animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
            attractions: ['Conservation Carousel'],
            guardiansTalks: [],
            wildEncounters: [],
            events: [],
         },
         {
            date: '2026-06-15',
         }
      ),
      {
         date: '2026-06-15',
         arrivalTime: '09:15',
         departureTime: '17:00',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
         attractions: ['Conservation Carousel'],
         guardiansTalks: [],
         wildEncounters: [],
         events: [],
      }
   );
});

test.describe('openItineraryWizard', () => {
   beforeEach(() => {
      globalThis.localStorage = createLocalStorageMock();
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.window;
      delete globalThis.localStorage;
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
});
