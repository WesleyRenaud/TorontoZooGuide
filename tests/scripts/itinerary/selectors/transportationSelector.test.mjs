import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySearchContext } from '../../../../scripts/itinerary/itinerarySearchContext.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { TransportationSelector } from '../../../../scripts/itinerary/selectors/transportationSelector.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationSelectorPrompter } from '../../../../scripts/itinerary/selectors/transportationSelectorPrompter.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateItineraryTransportationSelectorController_TestWiring_ExpectFactoryOptions', () => {
   const original = SelectorControllerFactory.createItinerarySelectorController;
   let captured;
   const controllerResult = { controller: true };
   const mountEl = { id: 'mount' };
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return controllerResult;
   };
   const zoomobile = { name: 'Zoomobile' };

   try {
      const controller = TransportationSelector.createItineraryTransportationSelectorController({
         mountEl,
      });

      assert.deepEqual(controller, controllerResult);
      assert.equal(TransportationSelector.STORAGE_KEY, StorageKeys.TRANSPORTATIONS_KEY);
      assert.equal(captured.storageKey, TransportationSelector.STORAGE_KEY);
      assert.equal(captured.hideNextButton, true);
      assert.equal(captured.migrateSelected, TransportationSelectorModel.migrateStoredTransportations);
      assert.equal(captured.getId, TransportationSelectorModel.getTransportationId);
      assert.equal(captured.h1, Strings.itinerary.selectors.titleTransportations);
      assert.deepEqual(captured.extractRows({ transportations: [zoomobile] }), [zoomobile]);
      assert.deepEqual(captured.extractRows({}), []);
      const query = 'bus';
      assert.deepEqual(captured.buildSearchPayload(query), {
         query,
         includeTransportations: true,
      });
      assert.equal(captured.getInfoLink(), null);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = original;
   }
});


test('Test_ShouldEnableTitleClick_TestLink_ExpectTrue', () => {
   const originalFactory = SelectorControllerFactory.createItinerarySelectorController;
   const originalLink = TransportationSelectorModel.getTransportationInfoLink;
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };
   TransportationSelectorModel.getTransportationInfoLink = (row) => row.link || null;
   const href = '/info';

   try {
      TransportationSelector.createItineraryTransportationSelectorController();

      const enabled = captured.shouldEnableTitleClick({ link: href });

      assert.equal(enabled, true);
      assert.equal(captured.shouldEnableTitleClick({}), false);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalFactory;
      TransportationSelectorModel.getTransportationInfoLink = originalLink;
   }
});


test('Test_OnTitleClick_TestLink_ExpectWindowOpen', () => {
   const originalFactory = SelectorControllerFactory.createItinerarySelectorController;
   const originalLink = TransportationSelectorModel.getTransportationInfoLink;
   const originalOpen = globalThis.window.open;
   const opens = [];
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };
   TransportationSelectorModel.getTransportationInfoLink = (row) => row.link || null;
   globalThis.window.open = (...args) => { opens.push(args); };
   const href = '/info';

   try {
      TransportationSelector.createItineraryTransportationSelectorController();
      captured.onTitleClick({ link: href });
      captured.onTitleClick({});

      assert.deepEqual(opens, [[href, '_blank']]);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalFactory;
      TransportationSelectorModel.getTransportationInfoLink = originalLink;
      globalThis.window.open = originalOpen;
   }
});


test('Test_OnBeforeToggleAdd_TestAlreadySelected_ExpectProceed', () => {
   const originalFactory = SelectorControllerFactory.createItinerarySelectorController;
   const originalShouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation;
   const originalPrompt = TransportationSelectorPrompter.promptForAddAsTransportationSelection;
   const prompts = [];
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };
   TransportationSelectorModel.shouldConfirmAddAsTransportation = ({ isSelected }) => !isSelected;
   TransportationSelectorPrompter.promptForAddAsTransportationSelection = (...args) => {
      prompts.push(args);
   };
   let proceeded = 0;

   try {
      TransportationSelector.createItineraryTransportationSelectorController();
      captured.onBeforeToggleAdd({
         row: { name: 'Zoomobile' },
         isSelected: true,
         proceed: () => { proceeded += 1; },
      });

      assert.equal(proceeded, 1);
      assert.equal(prompts.length, 0);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalFactory;
      TransportationSelectorModel.shouldConfirmAddAsTransportation = originalShouldConfirm;
      TransportationSelectorPrompter.promptForAddAsTransportationSelection = originalPrompt;
   }
});


test('Test_OnBeforeToggleAdd_TestAdding_ExpectPrompt', () => {
   const originalFactory = SelectorControllerFactory.createItinerarySelectorController;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalShouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation;
   const originalPrompt = TransportationSelectorPrompter.promptForAddAsTransportationSelection;
   const prompts = [];
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ date: '2026-06-15' });
   TransportationSelectorModel.shouldConfirmAddAsTransportation = ({ isSelected }) => !isSelected;
   TransportationSelectorPrompter.promptForAddAsTransportationSelection = (...args) => {
      prompts.push(args);
   };

   try {
      TransportationSelector.createItineraryTransportationSelectorController();
      captured.onBeforeToggleAdd({
         row: { name: 'Zoomobile' },
         isSelected: false,
         proceed: () => {},
      });

      assert.equal(prompts.length, 1);
      assert.equal(typeof captured.getContext, 'function');
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalFactory;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      TransportationSelectorModel.shouldConfirmAddAsTransportation = originalShouldConfirm;
      TransportationSelectorPrompter.promptForAddAsTransportationSelection = originalPrompt;
   }
});
