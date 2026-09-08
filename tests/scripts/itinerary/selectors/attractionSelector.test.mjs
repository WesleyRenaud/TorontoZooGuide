import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelector } from '../../../../scripts/itinerary/selectors/attractionSelector.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { AttractionSelectorRenderer } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorRenderer.js';
import { AttractionSelectorPrompter } from '../../../../scripts/itinerary/selectors/attractionSelectorPrompter.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateItineraryAttractionSelectorController_TestWiring_ExpectFactoryConfig', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalClosed = AttractionSelectorModel.shouldConfirmClosedAttraction;
   const originalAlso = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction;
   const originalPromptClosed = AttractionSelectorPrompter.promptForClosedAttractionSelection;
   const originalPromptAlso = AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection;
   const originalToggle = AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle;
   const originalLink = AttractionSelectorModel.getAttractionInfoLink;
   const opens = [];
   const originalOpen = window.open;
   let captured;
   const proceeds = [];

   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   window.open = (...args) => opens.push(args);

   try {
      const controller = AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });

      assert.deepEqual(controller, { ok: true });
      assert.equal(captured.storageKey, AttractionSelector.STORAGE_KEY);
      assert.deepEqual(captured.buildSearchPayload('ride'), {
         query: 'ride',
         includeAttractions: true,
         includeClosedAttractions: false,
      });
      assert.equal(captured.extractRows({ attractions: ['a'] })[0], 'a');

      AttractionSelectorModel.getAttractionInfoLink = () => 'https://example.com';
      assert.equal(captured.shouldEnableTitleClick({}), true);
      captured.onTitleClick({});
      AttractionSelectorModel.getAttractionInfoLink = () => null;
      captured.onTitleClick({});
      assert.deepEqual(opens, [['https://example.com', '_blank']]);

      AttractionSelectorModel.shouldConfirmClosedAttraction = () => false;
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = () => false;
      captured.onBeforeToggleAdd({
         row: { name: 'Carousel' },
         isSelected: false,
         proceed: () => proceeds.push('direct'),
      });
      assert.deepEqual(proceeds, ['direct']);

      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = () => true;
      AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection = (_row, proceed) => {
         proceed();
      };
      captured.onBeforeToggleAdd({
         row: { name: 'Zoomobile' },
         isSelected: false,
         proceed: () => proceeds.push('also'),
      });
      assert.ok(proceeds.includes('also'));

      AttractionSelectorModel.shouldConfirmClosedAttraction = () => true;
      AttractionSelectorPrompter.promptForClosedAttractionSelection = (_row, continueAdd) => {
         continueAdd();
      };
      captured.onBeforeToggleAdd({
         row: { name: 'Closed' },
         isSelected: false,
         proceed: () => proceeds.push('closed'),
      });
      assert.ok(proceeds.includes('closed'));

      AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle = ({ onChange }) => {
         onChange(true);
      };
      captured.renderExtraControls({
         bodyEl: document.createElement('div'),
         rerunSearch: () => {},
      });
      assert.deepEqual(captured.buildSearchPayload('ride'), {
         query: 'ride',
         includeAttractions: true,
         includeClosedAttractions: true,
      });
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.shouldConfirmClosedAttraction = originalClosed;
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = originalAlso;
      AttractionSelectorPrompter.promptForClosedAttractionSelection = originalPromptClosed;
      AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection = originalPromptAlso;
      AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle = originalToggle;
      AttractionSelectorModel.getAttractionInfoLink = originalLink;
      window.open = originalOpen;
   }
});
