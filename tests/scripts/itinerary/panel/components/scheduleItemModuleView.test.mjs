import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemModuleView } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleView.js';
import { ScheduleItemModuleFormBuilder } from '../../../../../scripts/itinerary/panel/components/scheduleItemModuleFormBuilder.js';
import { ScheduleItemTimeFields } from '../../../../../scripts/itinerary/panel/components/scheduleItemTimeFields.js';
import { ScheduleItemTypes } from '../../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { ResultRenderer } from '../../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _stubRowRenderer() {
   const configs = [];
   const originalCreate = ResultRenderer.createDefaultSelectorRowLeftRenderer;

   ResultRenderer.createDefaultSelectorRowLeftRenderer = (config) => {
      configs.push(config);
      return () => config;
   };

   return { configs, originalCreate };
}

installDomTestHooks();


test('Test_BuildSearchRowRenderer_TestAnimal_ExpectAnimalTitle', () => {
   const { originalCreate } = _stubRowRenderer();

   try {
      const renderer = ScheduleItemModuleView.buildSearchRowRenderer(
         ScheduleItemKind.ANIMAL.itemType
      );

      assert.equal(renderer().getTitle, AnimalSelectorModel.getAnimalTitleLine);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestGuardiansTalk_ExpectTalkTitle', () => {
   const { originalCreate } = _stubRowRenderer();

   try {
      const renderer = ScheduleItemModuleView.buildSearchRowRenderer(
         ScheduleItemKind.GUARDIANS_TALK.itemType
      );

      assert.equal(renderer().getTitle, GuardiansTalkSelectorModel.getGuardiansTalkName);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestWildEncounter_ExpectEncounterTitle', () => {
   const { originalCreate } = _stubRowRenderer();

   try {
      const renderer = ScheduleItemModuleView.buildSearchRowRenderer(
         ScheduleItemKind.WILD_ENCOUNTER.itemType
      );

      assert.equal(renderer().getTitle, WildEncounterSelectorModel.getWildEncounterName);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestTransportation_ExpectRideTitle', () => {
   const { originalCreate } = _stubRowRenderer();

   try {
      const renderer = ScheduleItemModuleView.buildSearchRowRenderer(
         ScheduleItemKind.TRANSPORTATION.itemType
      );

      assert.equal(renderer().getTitle, TransportationSelectorModel.getTransportationName);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestAttraction_ExpectAttractionTitle', () => {
   const { originalCreate } = _stubRowRenderer();

   try {
      const renderer = ScheduleItemModuleView.buildSearchRowRenderer(
         ScheduleItemKind.ATTRACTION.itemType
      );

      assert.equal(renderer().getTitle, AttractionSelectorModel.getAttractionTitle);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestAnimalParts_ExpectSpeciesAndEnclosure', () => {
   const { configs, originalCreate } = _stubRowRenderer();
   const species = 'Amur Tiger';
   const enclosureName = 'Indoor';
   const originalSpecies = AnimalSelectorModel.getAnimalSpecies;
   const originalEnclosure = AnimalSelectorModel.getAnimalEnclosureName;

   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalEnclosureName = () => enclosureName;

   try {
      ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ANIMAL.itemType);
      const animalConfig = configs.find(
         (config) => config.getTitle === AnimalSelectorModel.getAnimalTitleLine
      );
      const titleParts = animalConfig.getTitleParts({});

      assert.deepEqual(titleParts, { species, enclosureName });
   } finally {
      AnimalSelectorModel.getAnimalSpecies = originalSpecies;
      AnimalSelectorModel.getAnimalEnclosureName = originalEnclosure;
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestTransportationClick_ExpectOpensLink', () => {
   const { configs, originalCreate } = _stubRowRenderer();
   const infoLink = 'https://example.com/ride';
   const opens = [];
   const originalOpen = window.open;
   const originalLink = TransportationSelectorModel.getTransportationInfoLink;

   window.open = (...args) => opens.push(args);
   TransportationSelectorModel.getTransportationInfoLink = () => infoLink;

   try {
      ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.TRANSPORTATION.itemType);
      const transportationConfig = configs.find(
         (config) => config.getTitle === TransportationSelectorModel.getTransportationName
      );
      transportationConfig.onTitleClick({});

      assert.equal(transportationConfig.shouldEnableTitleClick({}), true);
      assert.deepEqual(opens, [[infoLink, '_blank']]);
   } finally {
      TransportationSelectorModel.getTransportationInfoLink = originalLink;
      window.open = originalOpen;
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestTransportationMissingLink_ExpectNoOpen', () => {
   const { configs, originalCreate } = _stubRowRenderer();
   const opens = [];
   const originalOpen = window.open;
   const originalLink = TransportationSelectorModel.getTransportationInfoLink;

   window.open = (...args) => opens.push(args);
   TransportationSelectorModel.getTransportationInfoLink = () => null;

   try {
      ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.TRANSPORTATION.itemType);
      const transportationConfig = configs.find(
         (config) => config.getTitle === TransportationSelectorModel.getTransportationName
      );
      transportationConfig.onTitleClick({});

      assert.deepEqual(opens, []);
   } finally {
      TransportationSelectorModel.getTransportationInfoLink = originalLink;
      window.open = originalOpen;
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestAttractionClick_ExpectOpensLink', () => {
   const { configs, originalCreate } = _stubRowRenderer();
   const infoLink = 'https://example.com/ride-attraction';
   const opens = [];
   const originalOpen = window.open;
   const originalLink = AttractionSelectorModel.getAttractionInfoLink;

   window.open = (...args) => opens.push(args);
   AttractionSelectorModel.getAttractionInfoLink = () => infoLink;

   try {
      ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ATTRACTION.itemType);
      const attractionConfig = configs.find(
         (config) => config.getTitle === AttractionSelectorModel.getAttractionTitle
      );
      attractionConfig.onTitleClick({});

      assert.equal(attractionConfig.shouldEnableTitleClick({}), true);
      assert.deepEqual(opens, [[infoLink, '_blank']]);
   } finally {
      AttractionSelectorModel.getAttractionInfoLink = originalLink;
      window.open = originalOpen;
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildSearchRowRenderer_TestAttractionMissingLink_ExpectNoOpen', () => {
   const { configs, originalCreate } = _stubRowRenderer();
   const opens = [];
   const originalOpen = window.open;
   const originalLink = AttractionSelectorModel.getAttractionInfoLink;

   window.open = (...args) => opens.push(args);
   AttractionSelectorModel.getAttractionInfoLink = () => null;

   try {
      ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ATTRACTION.itemType);
      const attractionConfig = configs.find(
         (config) => config.getTitle === AttractionSelectorModel.getAttractionTitle
      );
      attractionConfig.onTitleClick({});

      assert.deepEqual(opens, []);
   } finally {
      AttractionSelectorModel.getAttractionInfoLink = originalLink;
      window.open = originalOpen;
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});


test('Test_BuildScheduleItemModuleBody_TestStrings_ExpectFields', () => {
   const originalSelect = ScheduleItemModuleFormBuilder.createSelectField;
   const originalLabel = ScheduleItemModuleFormBuilder.createFieldLabel;
   const originalCheckbox = ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox;
   const originalTypes = ScheduleItemTypes.buildScheduleItemTypeOptions;
   const originalTimes = ScheduleItemTimeFields.makeScheduleItemTimeFields;
   const searchPlaceholder = 'Find…';

   ScheduleItemModuleFormBuilder.createSelectField = () => ({
      field: document.createElement('div'),
      select: document.createElement('select'),
   });
   ScheduleItemModuleFormBuilder.createFieldLabel = () => document.createElement('label');
   ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox = () => ({
      wrap: document.createElement('div'),
      checkbox: document.createElement('input'),
   });
   ScheduleItemTypes.buildScheduleItemTypeOptions = () => [{ value: 'animals', label: 'Animals' }];
   ScheduleItemTimeFields.makeScheduleItemTimeFields = () => ({
      fields: [document.createElement('div')],
   });

   try {
      const bodyParts = ScheduleItemModuleView.buildScheduleItemModuleBody({
         typeLabel: 'Type',
         searchLabel: 'Search',
         searchPlaceholder,
         onlyItineraryItemsLabel: 'Only itinerary',
      }, ['lunch']);

      assert.ok(bodyParts.body.classList.contains('schedule-item-module-body'));
      assert.equal(bodyParts.typeSelect.tagName.toLowerCase(), 'select');
      assert.equal(bodyParts.searchInput.className, 'schedule-item-search-input');
      assert.equal(bodyParts.searchInput.placeholder, searchPlaceholder);
      assert.ok(bodyParts.resultsEl.classList.contains('schedule-item-results'));
      assert.equal(bodyParts.resultsEl.getAttribute('aria-live'), 'polite');
      assert.ok(bodyParts.scheduleTimeFields);
   } finally {
      ScheduleItemModuleFormBuilder.createSelectField = originalSelect;
      ScheduleItemModuleFormBuilder.createFieldLabel = originalLabel;
      ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox = originalCheckbox;
      ScheduleItemTypes.buildScheduleItemTypeOptions = originalTypes;
      ScheduleItemTimeFields.makeScheduleItemTimeFields = originalTimes;
   }
});
