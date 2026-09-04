import assert from 'node:assert/strict';
import { test } from 'node:test';

import { openItineraryWizard } from '../../scripts/itinerary/wizard/wizardController.js';
import { createItineraryWizardState } from '../../scripts/itinerary/wizard/state.js';
import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
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
      let closeHandler = null;
      const dateController = {
         show() {},
         getDate: () => null,
      };

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await openItineraryWizard({
         mountEl,
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
         StorageKeys.SELECTED_EXHIBITS_KEY,
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

      assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
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

   test('closes without prompting after revisiting regions on an unchanged itinerary', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let saveHandler = null;
      let closeHandler = null;
      const visitDate = '2026-07-04';
      const existingAnimals = [
         { species: 'Red Panda', exhibit: 'Eurasia Wilds' },
      ];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => ({
               isActive: true,
               date: visitDate,
               animals: existingAnimals,
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 6, 4),
            createWizardState: (existing = {}) => createItineraryWizardState(existing),
            createDateStepController: ({ onSave, onClose }) => {
               saveHandler = onSave;
               closeHandler = onClose;
               return { show() {} };
            },
            selectionStepConfigs: [
               {
                  stepKey: 'regions',
                  selectionKey: 'animals',
                  preserveOnInvalid: true,
                  factory: ({ onClose }) => {
                     closeHandler = onClose;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => existingAnimals,
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

      saveHandler?.(visitDate);
      await closeHandler?.();

      assert.equal(popupConfigs.length, 0);
      assert.equal(mountEl.children.length, 0);
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

   test('regions finish saves when only the visit date changed', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let saveHandler = null;
      let regionsFinishHandler = null;
      const finishCalls = [];
      const existingAnimals = [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => ({
               isActive: true,
               date: '2026-06-01',
               animals: existingAnimals,
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: (existing = {}) => createItineraryWizardState(existing),
            createDateStepController: ({ onSave }) => {
               saveHandler = onSave;
               return { show() {} };
            },
            selectionStepConfigs: [
               {
                  stepKey: 'regions',
                  selectionKey: 'animals',
                  preserveOnInvalid: true,
                  factory: ({ onFinish }) => {
                     regionsFinishHandler = onFinish;
                     return {
                        show() {},
                        shouldSkipClosingSelectionSync: () => true,
                     };
                  },
               },
            ],
            finalizeWizard: async (draft, mountEl, options) => {
               finishCalls.push({ draft, options });
               mountEl.replaceChildren();
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      saveHandler?.('2026-06-15');
      regionsFinishHandler?.(null);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finishCalls.length, 1);
      assert.equal(finishCalls[0].draft.date, '2026-06-15');
      assert.deepEqual(
         finishCalls[0].draft.animals.map((animal) => animal.species),
         ['African Lion']
      );
      assert.equal(mountEl.children.length, 0);
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

   test('finish after selection changes clears the wizard overlay', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      const selectedAnimals = syncedSelection();
      const finalizeCalls = [];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await openItineraryWizard({
         mountEl,
         startAt: 'animals',
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
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return { show() {} };
                  },
               },
            ],
            finalizeWizard: async (draft, mount) => {
               finalizeCalls.push(draft);
               mount.replaceChildren();
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      finishHandler?.(selectedAnimals);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finalizeCalls.length, 1);
      assert.equal(mountEl.children.length, 0);
   });

   test('date finish saves when only the visit date changed', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      const finishCalls = [];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

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
            finalizeWizard: async (draft, mountEl, options) => {
               finishCalls.push({ draft, options });
               mountEl.replaceChildren();
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      await finishHandler?.('2026-06-15');

      assert.equal(finishCalls.length, 1);
      assert.equal(finishCalls[0].draft.date, '2026-06-15');
      assert.equal(mountEl.children.length, 0);
   });
});
