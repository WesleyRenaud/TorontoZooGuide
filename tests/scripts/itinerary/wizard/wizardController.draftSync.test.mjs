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


test('Test_Does_TestDoesNotPromptWhenClosingAfterADate_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupConfigs = [];
   let closeHandler = null;
   const selectedDate = makeNoonDate(_year, _juneIndex, _day);
   mountEl.appendChild(createDomNode('div', 'keep-until-close'));

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => selectedDate,
         createWizardState: () => ItineraryWizardStore.createItineraryWizardState({
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
         showConfirmPopup: (config) => {
            popupConfigs.push(config);
         },
         syncAnimalDraft: () => {},
      },
   });
   await closeHandler?.();

   assert.equal(popupConfigs.length, 0);
   assert.equal(mountEl.children.length, 0);
});


test('Test_Skips_TestSkipsDateDraftSyncWhenThePickerDate_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupConfigs = [];
   let closeHandler = null;
   const selectedDate = makeNoonDate(_year, _juneIndex, _day);
   const visitDate = '2026-06-15';

   await WizardController.openItineraryWizard({
      mountEl,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => selectedDate,
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: visitDate,
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            });

            wizard.updateSelection(_animalsStep, syncedSelection());
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


test('Test_Skips_TestSkipsSelectionDraftSyncWhenTheStepReports_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const popupConfigs = [];
   let closeHandler = null;

   await WizardController.openItineraryWizard({
      mountEl,
      startAt: _animalsStep,
      deps: {
         loadItinerary: async () => null,
         resolveEarliestVisitDate: async () => makeNoonDate(_year, _juneIndex, _day),
         createWizardState: () => {
            const wizard = ItineraryWizardStore.createItineraryWizardState({
               date: '',
               animals: [],
               attractions: [],
               guardiansTalks: [],
               wildEncounters: [],
            });

            wizard.updateSelection(_animalsStep, syncedSelection());
            return wizard;
         },
         createDateStepController: () => ({ show() {} }),
         selectionStepConfigs: [
            {
               stepKey: _animalsStep,
               selectionKey: _animalsStep,
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


test('Test_Finalize_TestFinalizeOnDoneConsumesPendingValidationAndClearsThe_ExpectOk', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   let finishHandler = null;
   const selectedAnimals = syncedSelection();
   const visitDate = '2026-06-15';
   const savedItinerary = {
      date: visitDate,
      animals: selectedAnimals,
      isActive: true,
   };
   let finishOnDoneCalls = 0;
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
               selectionKey: _animalsStep,
               factory: ({ onFinish }) => {
                  finishHandler = onFinish;
                  return { show() {} };
               },
            },
         ],
         finalizeWizard: async (_draft, mount, options) => {
            mount.replaceChildren();
            options.onDone?.(savedItinerary);
            finishOnDoneCalls += 1;
            return savedItinerary;
         },
         showConfirmPopup: () => {},
         syncAnimalDraft: () => {},
      },
   });
   finishHandler?.(selectedAnimals);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(finishOnDoneCalls, 1);
   assert.equal(mountEl.children.length, 0);
});
