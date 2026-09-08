import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { ItineraryWizardStore } from '../../../../scripts/itinerary/wizard/itineraryWizardStore.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController } from '../../helpers/wizardTestFixtures.mjs';

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
   },
});

test('Test_OpenItineraryWizard_TestMissingMount_ExpectNoOp', async () => {
   await WizardController.openItineraryWizard({ mountEl: null });
});

test('Test_OpenItineraryWizard_TestDepsWiring_ExpectShowsStartStep', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const shownSteps = [];
   const synced = [];

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: 'animals',
      deps: {
         loadItinerary: async () => ({
            isActive: true,
            animals: [{ species: 'Lion', exhibit: 'Africa' }],
         }),
         resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({}),
         createDateStepController: () => createStubStepController('date', shownSteps),
         selectionStepConfigs: [
            {
               stepKey: 'animals',
               selectionKey: 'animals',
               prevStepKey: 'regions',
               nextStepKey: null,
               factory: () => createStubStepController('animals', shownSteps),
            },
         ],
         finalizeWizard: async () => ({}),
         showConfirmPopup: () => {},
         syncAnimalDraft: (itinerary) => {
            synced.push(itinerary);
         },
      },
   });

   assert.deepEqual(shownSteps, ['animals']);
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
         resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
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

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: '',
               animals: [],
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
         finalizeWizard: async () => ({}),
         showConfirmPopup: (config) => {
            popups.push(config);
         },
         syncAnimalDraft: () => {},
      },
   });

   await closeHandler?.();
   assert.equal(popups.length, 1);
   assert.equal(popups[0].title, Strings.itinerary.confirmation.saveChangesTitle);
   assert.equal(typeof popups[0].onConfirm, 'function');
   assert.equal(typeof popups[0].onCancel, 'function');
});

test('Test_OpenItineraryWizard_TestFinishWithChanges_ExpectFinalize', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const finalized = [];

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(2026, 5, 15),
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: '',
               animals: [],
            });
            wizard.updateSelection('animals', [
               { species: 'African Lion', exhibit: 'Africa Savanna' },
            ]);
            return wizard;
         },
         createDateStepController: ({ onFinish }) => {
            finishHandler = onFinish;
            return {
               show() {},
               getDate: () => makeNoonDate(2026, 5, 15),
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

   await finishHandler?.(makeNoonDate(2026, 5, 15));
   assert.equal(finalized.length, 1);
   assert.equal(finalized[0].el, mountEl);
});
