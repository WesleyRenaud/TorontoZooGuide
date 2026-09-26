import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { ItineraryWizardStore } from '../../../../scripts/itinerary/wizard/itineraryWizardStore.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController, syncedSelection } from '../../helpers/wizardTestFixtures.mjs';
import { Position } from '../../../../scripts/shared/enums/position.js';

const _year = 2026;
const _juneIndex = 5;
const _day = 15;
const _animalsStep = 'animals';
const _animalsKey = 'animals';
const _regionsStep = 'regions';
const _dateStep = 'date';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
   },
});


test('Test_No_TestNoOpsWhenMountElIsMissing_ExpectOk', async () => {
   const mountEl = null;

   await assert.doesNotReject(async () => {
      await WizardController.openItineraryWizard({ mountEl });
   });
});


test('Test_Shows_TestShowsTheResolvedStartStepWithInjectedControllers_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const shownSteps = [];
   const dateController = createStubStepController(_dateStep, shownSteps);

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: () => dateController,
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
               prevStepKey: _regionsStep,
               nextStepKey: 'attractions',
               factory: () => createStubStepController(_animalsStep, shownSteps),
            },
         ],
         finalizeWizard: async () => {},
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });

   assert.deepEqual(shownSteps, [_animalsStep]);
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
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
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
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => ({
            isActive: true,
            date: visitDate,
            animals: [animal],
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
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
   const exhibit = 'Africa Savanna';
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([exhibit])
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
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
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
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
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

            wizard.updateSelection(_animalsKey, [animal]);

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
   assert.equal(
      popupConfigs[Position.FIRST].title,
      Strings.itinerary.confirmation.saveChangesTitle
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
         resolveEarliestVisitDate: async () => makeNoonDate(_year, 6, 4),
         createWizardState: (existing = {}) => ItineraryWizardStore.createItineraryWizardState(existing),
         createDateStepController: ({ onSave, onClose }) => {
            saveHandler = onSave;
            closeHandler = onClose;
            return { show() {} };
         },
         selectionStepConfigs: [
            {
               stepKey: _regionsStep,
               selectionKey: _animalsKey,
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
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: ({ onSave }) => {
            saveHandler = onSave;
            return {
               show() {
                  shownSteps.push(_dateStep);
               },
            };
         },
         selectionStepConfigs: [
            {
               stepKey: _regionsStep,
               selectionKey: _animalsKey,
               factory: () => ({
                  show() {
                     shownSteps.push(_regionsStep);
                  },
               }),
            },
         ],
         finalizeWizard: async () => {},
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   saveHandler?.(visitDate);

   assert.deepEqual(shownSteps, [_dateStep, _regionsStep]);
});


test('Test_Regions_TestRegionsFinishSavesWhenOnlyTheVisitDate_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let saveHandler = null;
   let regionsFinishHandler = null;
   const finishCalls = [];
   const existingAnimals = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
   ];
   const nextDate = '2026-06-15';
   const existingDate = '2026-06-01';
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => ({
            isActive: true,
            date: existingDate,
            animals: existingAnimals,
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: (existing = {}) => ItineraryWizardStore.createItineraryWizardState(existing),
         createDateStepController: ({ onSave }) => {
            saveHandler = onSave;
            return { show() {} };
         },
         selectionStepConfigs: [
            {
               stepKey: _regionsStep,
               selectionKey: _animalsKey,
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
         finalizeWizard: async (draft, mount, options) => {
            finishCalls.push({ draft, options });
            mount.replaceChildren();
            return draft;
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   saveHandler?.(nextDate);
   regionsFinishHandler?.(null);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(finishCalls.length, 1);
   assert.equal(finishCalls[Position.FIRST].draft.date, nextDate);
   assert.deepEqual(
      finishCalls[Position.FIRST].draft.animals.map((animal) => animal.species),
      existingAnimals.map((animal) => animal.species)
   );
   assert.equal(mountEl.children.length, 0);
});


test('Test_Selection_TestSelectionPrevHandlersReturnToThePreviousStep_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const shownSteps = [];
   let animalsPrevHandler = null;

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: () => ({
            show() {
               shownSteps.push(_dateStep);
            },
         }),
         selectionStepConfigs: [
            {
               stepKey: _regionsStep,
               selectionKey: _animalsKey,
               prevStepKey: _dateStep,
               nextStepKey: _animalsStep,
               factory: () => ({
                  show() {
                     shownSteps.push(_regionsStep);
                  },
               }),
            },
            {
               stepKey: _animalsStep,
               selectionKey: _animalsKey,
               prevStepKey: _regionsStep,
               factory: ({ onPrev }) => {
                  animalsPrevHandler = onPrev;
                  return {
                     show() {
                        shownSteps.push(_animalsStep);
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

   assert.deepEqual(shownSteps, [_animalsStep, _regionsStep]);
});


test('Test_Loads_TestLoadsDefaultSelectionStepConfigsWhenNoneAre_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const shownSteps = [];

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: () => ({
            show() {
               shownSteps.push(_dateStep);
            },
         }),
         loadSelectionStepConfigs: async () => ([
            {
               stepKey: _regionsStep,
               selectionKey: _animalsKey,
               factory: () => ({
                  show() {
                     shownSteps.push(_regionsStep);
                  },
               }),
            },
         ]),
         finalizeWizard: async () => {},
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });

   assert.deepEqual(shownSteps, [_dateStep]);
});


test('Test_Finish_TestFinishAfterSelectionChangesClearsTheWizardOverlay_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const selectedAnimals = syncedSelection();
   const finalizeCalls = [];
   const visitDate = '2026-06-15';
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

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
   assert.deepEqual(finalizeCalls[Position.FIRST].animals, selectedAnimals);
   assert.equal(mountEl.children.length, 0);
});


test('Test_Date_TestDateFinishSavesWhenOnlyTheVisitDate_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const finishCalls = [];
   const visitDate = '2026-06-15';
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: ({ onFinish }) => {
            finishHandler = onFinish;
            return { show() {} };
         },
         selectionStepConfigs: [],
         finalizeWizard: async (draft, mount, options) => {
            finishCalls.push({ draft, options });
            mount.replaceChildren();
            return draft;
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   await finishHandler?.(visitDate);

   assert.equal(finishCalls.length, 1);
   assert.equal(finishCalls[Position.FIRST].draft.date, visitDate);
   assert.equal(mountEl.children.length, 0);
});


test('Test_Date_TestDateFinishSavesChangedVisitTimes_ExpectDraftTimes', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const finishCalls = [];
   const visitDate = '2026-06-15';
   const arrivalTime = '10:00 AM';
   const departureTime = '4:00 PM';
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: ({ onFinish }) => {
            finishHandler = onFinish;
            return {
               show() {},
               getArrivalTime: () => arrivalTime,
               getDepartureTime: () => departureTime,
            };
         },
         selectionStepConfigs: [],
         finalizeWizard: async (draft, mount, options) => {
            finishCalls.push({ draft, options });
            mount.replaceChildren();
            return draft;
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   await finishHandler?.(visitDate);

   assert.equal(finishCalls.length, 1);
   assert.equal(finishCalls[Position.FIRST].draft.arrivalTime, arrivalTime);
   assert.equal(finishCalls[Position.FIRST].draft.departureTime, departureTime);
});
