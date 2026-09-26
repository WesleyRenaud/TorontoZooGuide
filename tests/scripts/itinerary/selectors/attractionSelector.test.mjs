import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelector } from '../../../../scripts/itinerary/selectors/attractionSelector.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { AttractionSelectorRenderer } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorRenderer.js';
import { AttractionSelectorPrompter } from '../../../../scripts/itinerary/selectors/attractionSelectorPrompter.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateItineraryAttractionSelectorController_TestWiring_ExpectFactoryConfig', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalLink = AttractionSelectorModel.getAttractionInfoLink;
   const originalOpen = window.open;
   let captured;
   const controllerResult = { ok: true };
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return controllerResult;
   };
   window.open = () => {};

   try {
      const controller = AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });

      assert.deepEqual(controller, controllerResult);
      assert.equal(captured.storageKey, AttractionSelector.STORAGE_KEY);
      const query = 'ride';
      assert.deepEqual(captured.buildSearchPayload(query), {
         query,
         includeAttractions: true,
         includeClosedAttractions: false,
      });
      const attractions = ['a'];
      assert.equal(
         captured.extractRows({ attractions }).at(Position.FIRST),
         attractions.at(Position.FIRST)
      );
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.getAttractionInfoLink = originalLink;
      window.open = originalOpen;
   }
});


test('Test_OnTitleClick_TestInfoLink_ExpectWindowOpen', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalLink = AttractionSelectorModel.getAttractionInfoLink;
   const originalOpen = window.open;
   const opens = [];
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   window.open = (...args) => opens.push(args);
   const href = 'https://example.com';

   try {
      AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });
      AttractionSelectorModel.getAttractionInfoLink = () => href;

      const enabled = captured.shouldEnableTitleClick({});
      captured.onTitleClick({});
      AttractionSelectorModel.getAttractionInfoLink = () => null;
      captured.onTitleClick({});

      assert.equal(enabled, true);
      assert.deepEqual(opens, [[href, '_blank']]);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.getAttractionInfoLink = originalLink;
      window.open = originalOpen;
   }
});


test('Test_OnBeforeToggleAdd_TestNoConfirm_ExpectProceed', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalClosed = AttractionSelectorModel.shouldConfirmClosedAttraction;
   const originalAlso = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction;
   let captured;
   const proceeds = [];
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AttractionSelectorModel.shouldConfirmClosedAttraction = () => false;
   AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = () => false;

   try {
      AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.onBeforeToggleAdd({
         row: { name: 'Carousel' },
         isSelected: false,
         proceed: () => proceeds.push('direct'),
      });

      assert.deepEqual(proceeds, ['direct']);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.shouldConfirmClosedAttraction = originalClosed;
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = originalAlso;
   }
});


test('Test_OnBeforeToggleAdd_TestAlsoTransportation_ExpectPrompt', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalClosed = AttractionSelectorModel.shouldConfirmClosedAttraction;
   const originalAlso = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction;
   const originalPromptAlso = AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection;
   let captured;
   const proceeds = [];
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AttractionSelectorModel.shouldConfirmClosedAttraction = () => false;
   AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = () => true;
   AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection = (_row, proceed) => {
      proceed();
   };

   try {
      AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.onBeforeToggleAdd({
         row: { name: 'Zoomobile' },
         isSelected: false,
         proceed: () => proceeds.push('also'),
      });

      assert.ok(proceeds.includes('also'));
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.shouldConfirmClosedAttraction = originalClosed;
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = originalAlso;
      AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection = originalPromptAlso;
   }
});


test('Test_OnBeforeToggleAdd_TestClosed_ExpectPrompt', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalClosed = AttractionSelectorModel.shouldConfirmClosedAttraction;
   const originalAlso = AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction;
   const originalPromptClosed = AttractionSelectorPrompter.promptForClosedAttractionSelection;
   let captured;
   const proceeds = [];
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AttractionSelectorModel.shouldConfirmClosedAttraction = () => true;
   AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = () => false;
   AttractionSelectorPrompter.promptForClosedAttractionSelection = (_row, continueAdd) => {
      continueAdd();
   };

   try {
      AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.onBeforeToggleAdd({
         row: { name: 'Closed' },
         isSelected: false,
         proceed: () => proceeds.push('closed'),
      });

      assert.ok(proceeds.includes('closed'));
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorModel.shouldConfirmClosedAttraction = originalClosed;
      AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction = originalAlso;
      AttractionSelectorPrompter.promptForClosedAttractionSelection = originalPromptClosed;
   }
});


test('Test_RenderExtraControls_TestIncludeClosed_ExpectSearchPayload', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalToggle = AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle;
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { ok: true };
   };
   AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle = ({ onChange }) => {
      onChange(true);
   };
   const query = 'ride';

   try {
      AttractionSelector.createItineraryAttractionSelectorController({
         mountEl: document.createElement('div'),
      });
      captured.renderExtraControls({
         bodyEl: document.createElement('div'),
         rerunSearch: () => {},
      });

      assert.deepEqual(captured.buildSearchPayload(query), {
         query,
         includeAttractions: true,
         includeClosedAttractions: true,
      });
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle = originalToggle;
   }
});
