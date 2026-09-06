import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardController } from '../../../../scripts/itinerary/wizard/wizardController.js';
import { State } from '../../../../scripts/itinerary/wizard/state.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';
import { createStubStepController, syncedSelection } from '../../helpers/wizardTestFixtures.mjs';

test.describe('WizardController.openItineraryWizard draft sync', () => {
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
      const selectedDate = makeNoonDate(2026, 5, 15);

      mountEl.appendChild(createDomNode('div', 'keep-until-close'));

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => selectedDate,
            createWizardState: () => State.createItineraryWizardState({
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
      const selectedDate = makeNoonDate(2026, 5, 15);

      await WizardController.openItineraryWizard({
         mountEl,
         deps: {
            loadItinerary: async () => null,
            resolveEarliestVisitDate: async () => selectedDate,
            createWizardState: () => {
               const wizard = State.createItineraryWizardState({
                  date: '2026-06-15',
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
         startAt: 'animals',
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
            createDateStepController: () => ({ show() {} }),
            selectionStepConfigs: [
               {
                  stepKey: 'animals',
                  selectionKey: 'animals',
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
      const savedItinerary = {
         date: '2026-06-15',
         animals: selectedAnimals,
         isActive: true,
      };
      let finishOnDoneCalls = 0;

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
});
