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

   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { controller: true };
   };

   try {
      assert.deepEqual(
         TransportationSelector.createItineraryTransportationSelectorController({
            mountEl: { id: 'mount' },
         }),
         { controller: true }
      );
      assert.equal(TransportationSelector.STORAGE_KEY, StorageKeys.TRANSPORTATIONS_KEY);
      assert.equal(captured.storageKey, TransportationSelector.STORAGE_KEY);
      assert.equal(captured.hideNextButton, true);
      assert.equal(captured.migrateSelected, TransportationSelectorModel.migrateStoredTransportations);
      assert.equal(captured.getId, TransportationSelectorModel.getTransportationId);
      assert.equal(captured.h1, Strings.itinerary.selectors.titleTransportations);
      assert.deepEqual(captured.extractRows({ transportations: [{ name: 'Zoomobile' }] }), [
         { name: 'Zoomobile' },
      ]);
      assert.deepEqual(captured.extractRows({}), []);
      assert.deepEqual(captured.buildSearchPayload('bus'), {
         query: 'bus',
         includeTransportations: true,
      });
      assert.equal(captured.getInfoLink(), null);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = original;
   }
});

test('Test_CreateItineraryTransportationSelectorController_TestTitleClickAndToggle_ExpectSideEffects', () => {
   const originalFactory = SelectorControllerFactory.createItinerarySelectorController;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalLink = TransportationSelectorModel.getTransportationInfoLink;
   const originalShouldConfirm = TransportationSelectorModel.shouldConfirmAddAsTransportation;
   const originalPrompt = TransportationSelectorPrompter.promptForAddAsTransportationSelection;
   const opens = [];
   const prompts = [];
   let captured;

   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ date: '2026-06-15' });
   TransportationSelectorModel.getTransportationInfoLink = (row) => row.link || null;
   TransportationSelectorModel.shouldConfirmAddAsTransportation = ({ isSelected }) => !isSelected;
   TransportationSelectorPrompter.promptForAddAsTransportationSelection = (...args) => {
      prompts.push(args);
   };
   const originalOpen = globalThis.window.open;
   globalThis.window.open = (...args) => { opens.push(args); };

   try {
      TransportationSelector.createItineraryTransportationSelectorController();

      assert.equal(captured.shouldEnableTitleClick({ link: '/info' }), true);
      assert.equal(captured.shouldEnableTitleClick({}), false);

      captured.onTitleClick({ link: '/info' });
      captured.onTitleClick({});
      assert.deepEqual(opens, [['/info', '_blank']]);

      let proceeded = 0;
      captured.onBeforeToggleAdd({
         row: { name: 'Zoomobile' },
         isSelected: true,
         proceed: () => { proceeded += 1; },
      });
      assert.equal(proceeded, 1);
      assert.equal(prompts.length, 0);

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
      TransportationSelectorModel.getTransportationInfoLink = originalLink;
      TransportationSelectorModel.shouldConfirmAddAsTransportation = originalShouldConfirm;
      TransportationSelectorPrompter.promptForAddAsTransportationSelection = originalPrompt;
      globalThis.window.open = originalOpen;
   }
});
