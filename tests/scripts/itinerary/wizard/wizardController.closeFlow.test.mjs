import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { State } from '../../../../scripts/itinerary/wizard/state.js';
import { APP_STRINGS } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController, syncedSelection } from '../../helpers/wizardTestFixtures.mjs';

test.describe('WizardController.openItineraryWizard close flow', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });
   test('Test_Syncs_TestSyncsTheActiveSelectionStepDraftBeforePrompting_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      let closeHandler = null;
      const syncedSelection = [{
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }];

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: () => State.createItineraryWizardState({
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

   test('Test_Confirming_TestConfirmingTheSavePromptFinishesTheWizard_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finishCalls = [];
      let closeHandler = null;
      let popupConfig = null;

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

   test('Test_Discarding_TestDiscardingFromTheSavePromptClosesTheWizard_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let closeHandler = null;
      let popupConfig = null;

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

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

      assert.equal(mountEl.children.length, 0);
   });

   test('Test_Selection_TestSelectionFinishHandlersFinalizeTheWizard_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finishCalls = [];
      let finishHandler = null;
      const selectedAnimals = syncedSelection();

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
            finalizeWizard: async (draft) => {
               finishCalls.push(draft);
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

      assert.equal(finishCalls.length, 1);
      assert.deepEqual(finishCalls[0].animals, selectedAnimals);
   });

   test('Test_Cancelling_TestCancellingFinishLeavesAnimalSelectionsWhenIssuesHave_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const popupConfigs = [];
      const stepShows = [];
      let finishHandler = null;
      let closeHandler = null;
      let wizard = null;
      let selectionSnapshot = [{ species: 'African Lion', exhibit: 'Africa Savanna' }];

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => ({
               date: '2026-06-15',
               animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: (existing) => {
               wizard = State.createItineraryWizardState(existing);
               return wizard;
            },
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onFinish, onClose }) => {
                     finishHandler = onFinish;
                     closeHandler = onClose;
                     return {
                        show() {
                           stepShows.push('animals');
                           selectionSnapshot = [...wizard.state.animals];
                        },
                        getSelectionSnapshot: async () => selectionSnapshot,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async () => ({ cancelled: true, issues: [] }),
            showConfirmPopup: (config) => {
               popupConfigs.push(config);
            },
            syncAnimalDraft: () => {},
         },
      });

      selectionSnapshot = [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'Cheetah', exhibit: 'Africa Savanna' },
      ];
      finishHandler?.(selectionSnapshot);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(wizard.state.animals.length, 2);
      assert.ok(stepShows.length >= 2);

      await closeHandler?.();

      assert.equal(popupConfigs.length, 1);
      assert.equal(
         popupConfigs[0].title,
         APP_STRINGS.itinerary.confirmation.saveChangesTitle
      );
   });

   test('Test_Cancelling_TestCancellingALongWaitWarningRemovesOnlyThe_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      let finishHandler = null;
      let wizard = null;
      let applyDate = null;

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'guardiansTalks',
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 6, 28),
            createWizardState: (existing) => {
               wizard = State.createItineraryWizardState(existing ?? {
                  date: '',
                  animals: [],
                  attractions: [],
                  guardiansTalks: [],
                  wildEncounters: [],
               });
               return wizard;
            },
            createDateStepController: ({ onSave }) => {
               applyDate = onSave;
               return { show() {} };
            },
            selectionStepConfigs: [
               {
                  stepKey: 'guardiansTalks',
                  selectionKey: 'guardiansTalks',
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => wizard.state.guardiansTalks,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async (draft) => {
               assert.equal(draft.date, '2026-07-28');
               assert.equal(draft.guardiansTalks.length, 2);
               return {
                  cancelled: true,
                  issues: [{
                     type: 'fixedTimeItemLongWait',
                     items: [{
                        name: 'Western Grey Kangaroo',
                        item_type: 'guardiansTalk',
                        start_time: '11:00 AM',
                        end_time: '11:30 AM',
                     }],
                  }],
               };
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      applyDate?.('2026-07-28');
      wizard.updateSelection('guardiansTalks', [
         { name: 'Western Grey Kangaroo', start_time: '11:00 AM' },
         { name: 'Aldabra Tortoise', start_time: '2:00 PM' },
      ]);

      finishHandler?.(wizard.state.guardiansTalks);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(wizard.state.date, '2026-07-28');
      assert.deepEqual(
         wizard.state.guardiansTalks.map((talk) => talk.name),
         ['Aldabra Tortoise']
      );
   });
});

test.describe('WizardController.openItineraryWizard finish flow', () => {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
      },
      after: () => {
         delete globalThis.localStorage;
      },
   });

   test('Test_Skips_TestSkipsSaveWhenFinishingWithoutSelectionChanges_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finalizeCalls = [];
      let finishHandler = null;
      const existingAnimals = syncedSelection();

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => ({
               date: '2026-06-15',
               animals: existingAnimals,
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
               isActive: true,
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: (existing) => State.createItineraryWizardState(existing),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => existingAnimals,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async (draft) => {
               finalizeCalls.push(draft);
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      finishHandler?.(existingAnimals);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finalizeCalls.length, 0);
      assert.equal(mountEl.children.length, 0);
   });

   test('Test_Saves_TestSavesWhenFinishingAfterSelectionChanges_ExpectOk', async () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const finalizeCalls = [];
      let finishHandler = null;
      const existingAnimals = syncedSelection();
      const nextAnimals = [
         ...existingAnimals,
         { species: 'Cheetah', exhibit: 'Africa Savanna' },
      ];

      await WizardController.openItineraryWizard({
         mountEl,
         startAt: 'animals',
         deps: {
            loadItinerary: async () => ({
               date: '2026-06-15',
               animals: existingAnimals,
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
               isActive: true,
            }),
            resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
            createWizardState: (existing) => State.createItineraryWizardState(existing),
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => nextAnimals,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async (draft) => {
               finalizeCalls.push(draft);
               return draft;
            },
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      finishHandler?.(nextAnimals);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.equal(finalizeCalls.length, 1);
      assert.equal(finalizeCalls[0].animals.length, 2);
   });
});
