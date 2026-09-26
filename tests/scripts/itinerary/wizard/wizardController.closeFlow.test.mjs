import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { ItineraryWizardStore } from '../../../../scripts/itinerary/wizard/itineraryWizardStore.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController, syncedSelection } from '../../helpers/wizardTestFixtures.mjs';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

const _year = 2026;
const _juneIndex = 5;
const _day = 15;
const _animalsStep = 'animals';
const _animalsKey = 'animals';

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
   const selectedAnimals = [{
      species: 'African Lion',
      exhibit: 'Africa Savanna',
   }];

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({
            date: '',
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
         }),
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
               factory: ({ onClose }) => {
                  closeHandler = onClose;
                  return {
                     show() {},
                     getSelectionSnapshot: async () => selectedAnimals,
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
   const selectedDate = makeNoonDate(_year, _juneIndex, _day);

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => selectedDate,
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            });

            wizard.updateSelection(_animalsKey, syncedSelection());
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
   assert.equal(finishCalls[Position.FIRST].animals.length, 1);
});


test('Test_Discarding_TestDiscardingFromTheSavePromptClosesTheWizard_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let closeHandler = null;
   let popupConfig = null;
   const selectedDate = makeNoonDate(_year, _juneIndex, _day);
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => selectedDate,
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            });

            wizard.updateSelection(_animalsKey, syncedSelection());
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
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({
            date: visitDate,
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
         }),
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
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
   assert.deepEqual(finishCalls[Position.FIRST].animals, selectedAnimals);
});


test('Test_Cancelling_TestCancellingFinishLeavesAnimalSelectionsWhenIssuesHave_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupConfigs = [];
   const stepShows = [];
   let finishHandler = null;
   let closeHandler = null;
   let wizard = null;
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const cheetah = { species: 'Cheetah', exhibit: 'Africa Savanna' };
   let selectionSnapshot = [lion];
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => ({
            date: visitDate,
            animals: [lion],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: (existing) => {
            wizard = ItineraryWizardStore.createItineraryWizardState(existing);
            return wizard;
         },
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
               factory: ({ onFinish, onClose }) => {
                  finishHandler = onFinish;
                  closeHandler = onClose;
                  return {
                     show() {
                        stepShows.push(_animalsStep);
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
   selectionSnapshot = [lion, cheetah];
   finishHandler?.(selectionSnapshot);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(wizard.state.animals.length, 2);
   assert.ok(stepShows.length >= 2);

   await closeHandler?.();

   assert.equal(popupConfigs.length, 1);
   assert.equal(
      popupConfigs[Position.FIRST].title,
      Strings.itinerary.confirmation.saveChangesTitle
   );
});


test('Test_Cancelling_TestCancellingALongWaitWarningRemovesOnlyThe_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   let wizard = null;
   let applyDate = null;
   const visitDate = '2026-07-28';
   const kangarooName = 'Western Grey Kangaroo';
   const tortoiseName = 'Aldabra Tortoise';
   const kangarooStart = '11:00 AM';
   const talksStep = 'guardiansTalks';

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: talksStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, 6, 28),
         createWizardState: (existing) => {
            wizard = ItineraryWizardStore.createItineraryWizardState(existing ?? {
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
               stepKey: talksStep,
               selectionKey: talksStep,
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
            assert.equal(draft.date, visitDate);
            assert.equal(draft.guardiansTalks.length, 2);
            return {
               cancelled: true,
               issues: [{
                  type: 'fixedTimeItemLongWait',
                  items: [{
                     name: kangarooName,
                     item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                     start_time: kangarooStart,
                     end_time: '11:30 AM',
                  }],
               }],
            };
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   applyDate?.(visitDate);
   wizard.updateSelection(talksStep, [
      { name: kangarooName, start_time: kangarooStart },
      { name: tortoiseName, start_time: '2:00 PM' },
   ]);
   finishHandler?.(wizard.state.guardiansTalks);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(wizard.state.date, visitDate);
   assert.deepEqual(
      wizard.state.guardiansTalks.map((talk) => talk.name),
      [tortoiseName]
   );
});


test('Test_Skips_TestSkipsSaveWhenFinishingWithoutSelectionChanges_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const finalizeCalls = [];
   let finishHandler = null;
   const existingAnimals = syncedSelection();
   const visitDate = '2026-06-15';
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => ({
            date: visitDate,
            animals: existingAnimals,
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            isActive: true,
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: (existing) => ItineraryWizardStore.createItineraryWizardState(existing),
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
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
   const cheetah = { species: 'Cheetah', exhibit: 'Africa Savanna' };
   const nextAnimals = [
      ...existingAnimals,
      cheetah,
   ];
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => ({
            date: visitDate,
            animals: existingAnimals,
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            isActive: true,
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: (existing) => ItineraryWizardStore.createItineraryWizardState(existing),
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
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
   assert.deepEqual(finalizeCalls[Position.FIRST].animals, nextAnimals);
});
