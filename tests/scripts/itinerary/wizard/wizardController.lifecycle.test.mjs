import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { State } from '../../../../scripts/itinerary/wizard/state.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { APP_STRINGS } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController, syncedSelection } from '../../helpers/wizardTestFixtures.mjs';

test.describe('WizardController.openItineraryWizard lifecycle', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });
   test('Test_No_TestNoOpsWhenMountElIsMissing_ExpectOk', async () => {
      await WizardController.openItineraryWizard({ mountEl: null });
   });

   test('Test_Shows_TestShowsTheResolvedStartStepWithInjectedControllers_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      const dateController = createStubStepController('date', shownSteps);

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Closes_TestClosesImmediatelyWhenThereAreNoUnsavedChanges_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let closeHandler = null;
      const dateController = {
         show() {},
         getDate: () => null,
      };

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Syncs_TestSyncsAnimalDraftStateForAnActiveItinerary_ExpectOk', async () => {
      const syncedItineraries = [];
      const mountEl = createDomNode('div', 'wizard-mount');

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => ({
               isActive: true,
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Clears_TestClearsStaleRegionSelectionStorageWhenOpeningWithout_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      localStorage.setItem(
         StorageKeys.SELECTED_EXHIBITS_KEY,
         JSON.stringify(['Africa Savanna'])
      );

      await WizardController.openItineraryWizard({
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
            createWizardState: () => State.createItineraryWizardState({}),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [],
            finalizeWizard: async () => {},
            syncAnimalDraft: () => {},
         },
      });

      assert.equal(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY), null);
   });

   test('Test_Prompts_TestPromptsToSaveWhenClosingWithUnsavedChanges_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => {
               const wizard = State.createItineraryWizardState({
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

   test('Test_Closes_TestClosesWithoutPromptingAfterRevisitingRegionsOnAn_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let saveHandler = null;
      let closeHandler = null;
      const visitDate = '2026-07-04';
      const existingAnimals = [
         { species: 'Red Panda', exhibit: 'Eurasia Wilds' },
      ];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
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
            createWizardState: (existing = {}) => State.createItineraryWizardState(existing),
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

   test('Test_Date_TestDateSaveAdvancesToTheRegionsStep_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      let saveHandler = null;

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Regions_TestRegionsFinishSavesWhenOnlyTheVisitDate_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let saveHandler = null;
      let regionsFinishHandler = null;
      const finishCalls = [];
      const existingAnimals = [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
      ];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
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
            createWizardState: (existing = {}) => State.createItineraryWizardState(existing),
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

   test('Test_Selection_TestSelectionPrevHandlersReturnToThePreviousStep_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];
      let animalsPrevHandler = null;

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Loads_TestLoadsDefaultSelectionStepConfigsWhenNoneAre_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const shownSteps = [];

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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

   test('Test_Finish_TestFinishAfterSelectionChangesClearsTheWizardOverlay_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      const selectedAnimals = syncedSelection();
      const finalizeCalls = [];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({
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

   test('Test_Date_TestDateFinishSavesWhenOnlyTheVisitDate_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      const finishCalls = [];

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({}),
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
