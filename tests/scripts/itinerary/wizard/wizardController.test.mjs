import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { ItineraryWizardStore } from '../../../../scripts/itinerary/wizard/itineraryWizardStore.js';
import { WizardStepConfigs } from '../../../../scripts/itinerary/wizard/wizardStepConfigs.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController } from '../../helpers/wizardTestFixtures.mjs';
import { Position } from '../../../../scripts/shared/enums/position.js';

const _year = 2026;
const _juneIndex = 5;
const _day = 15;
const _animalsStep = 'animals';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
   },
});


test('Test_OpenItineraryWizard_TestMissingMount_ExpectNoOp', async () => {
   const mountEl = null;

   await assert.doesNotReject(async () => {
      await WizardController.openItineraryWizard({ mountEl });
   });
});


test('Test_OpenItineraryWizard_TestDepsWiring_ExpectShowsStartStep', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const shownSteps = [];
   const synced = [];
   const animal = { species: 'Lion', exhibit: 'Africa' };

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => ({
            isActive: true,
            animals: [animal],
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: () => createStubStepController('date', shownSteps),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsStep,
               prevStepKey: 'regions',
               nextStepKey: null,
               factory: () => createStubStepController(_animalsStep, shownSteps),
            },
         ],
         finalizeWizard: async () => ({}),
         showConfirmPopup: () => {},
         syncAnimalDraft: (itinerary) => {
            synced.push(itinerary);
         },
      },
   });

   assert.deepEqual(shownSteps, [_animalsStep]);
   assert.equal(synced.length, 1);
});


test('Test_OpenItineraryWizard_TestCloseWithoutChanges_ExpectClearsMount', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   mountEl.appendChild(createDomNode('div', 'keep'));
   let closeHandler = null;

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: ({ onClose }) => {
            closeHandler = onClose;
            return {
               show() {},
               getDate: () => null,
            };
         },
         selectionStepConfigs: [],
         finalizeWizard: async () => ({}),
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   await closeHandler?.();

   assert.equal(mountEl.children.length, 0);
});


test('Test_OpenItineraryWizard_TestCloseWithUnsavedChanges_ExpectSavePrompt', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popups = [];
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
            });
            wizard.updateSelection(_animalsStep, [animal]);
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
         finalizeWizard: async () => ({}),
         showConfirmPopup: (config) => {
            popups.push(config);
         },
         syncAnimalDraft: () => {},
      },
   });
   await closeHandler?.();

   assert.equal(popups.length, 1);
   assert.equal(popups[Position.FIRST].title, Strings.itinerary.confirmation.saveChangesTitle);
   assert.equal(typeof popups[Position.FIRST].onConfirm, 'function');
   assert.equal(typeof popups[Position.FIRST].onCancel, 'function');
});


test('Test_OpenItineraryWizard_TestFinishWithChanges_ExpectFinalize', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const finalized = [];
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
            });
            wizard.updateSelection(_animalsStep, [animal]);
            return wizard;
         },
         createDateStepController: ({ onFinish }) => {
            finishHandler = onFinish;
            return {
               show() {},
               getDate: () => selectedDate,
            };
         },
         selectionStepConfigs: [],
         finalizeWizard: async (draft, el) => {
            finalized.push({ draft, el });
            return {};
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   await finishHandler?.(selectedDate);

   assert.equal(finalized.length, 1);
   assert.equal(finalized[Position.FIRST].el, mountEl);
});


test('Test_OpenItineraryWizard_TestFinishOverrideNullSelection_ExpectSkipsUpdate', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   let wizard = null;
   const originalBuild = WizardStepConfigs.buildSelectionStepHandlers;
   let capturedFinish = null;
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const visitDate = '2026-06-15';
   WizardStepConfigs.buildSelectionStepHandlers = (options) => {
      capturedFinish = options.finish;
      return originalBuild(options);
   };

   try {
      await WizardController.openItineraryWizard({
         mountEl,
         startAt: _animalsStep,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
            createWizardState: () => {
               wizard = ItineraryWizardStore.createItineraryWizardState({
                  date: visitDate,
                  animals: [animal],
               });
               return wizard;
            },
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: _animalsStep,
                  selectionKey: _animalsStep,
                  factory: ({ onFinish }) => {
                     finishHandler = onFinish;
                     return {
                        show() {},
                        getSelectionSnapshot: async () => wizard.state.animals,
                        shouldSkipClosingSelectionSync: () => false,
                     };
                  },
               },
            ],
            finalizeWizard: async () => ({}),
            showConfirmPopup: () => {},
            syncAnimalDraft: () => {},
         },
      });

      await capturedFinish({ animals: null });

      assert.equal(typeof capturedFinish, 'function');
      assert.deepEqual(wizard.state.animals, [animal]);
      assert.equal(typeof finishHandler, 'function');
   } finally {
      WizardStepConfigs.buildSelectionStepHandlers = originalBuild;
   }
});
