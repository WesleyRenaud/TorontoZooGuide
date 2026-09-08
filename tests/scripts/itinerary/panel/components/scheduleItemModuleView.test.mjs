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

installDomTestHooks();

test('Test_BuildSearchRowRenderer_TestModuleTypes_ExpectConfiguredRenderers', () => {
   const originalCreate = ResultRenderer.createDefaultSelectorRowLeftRenderer;
   const configs = [];

   ResultRenderer.createDefaultSelectorRowLeftRenderer = (config) => {
      configs.push(config);
      return () => config;
   };

   try {
      assert.equal(
         ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ANIMAL.itemType)().getTitle,
         AnimalSelectorModel.getAnimalTitleLine
      );
      assert.equal(
         ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.GUARDIANS_TALK.itemType)().getTitle,
         GuardiansTalkSelectorModel.getGuardiansTalkName
      );
      assert.equal(
         ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.WILD_ENCOUNTER.itemType)().getTitle,
         WildEncounterSelectorModel.getWildEncounterName
      );
      assert.equal(
         ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.TRANSPORTATION.itemType)().getTitle,
         TransportationSelectorModel.getTransportationName
      );
      assert.equal(
         ScheduleItemModuleView.buildSearchRowRenderer(ScheduleItemKind.ATTRACTION.itemType)().getTitle,
         AttractionSelectorModel.getAttractionTitle
      );

      const animalConfig = configs.find(
         (config) => config.getTitle === AnimalSelectorModel.getAnimalTitleLine
      );
      const originalSpecies = AnimalSelectorModel.getAnimalSpecies;
      const originalEnclosure = AnimalSelectorModel.getAnimalEnclosureName;
      AnimalSelectorModel.getAnimalSpecies = () => 'Tiger';
      AnimalSelectorModel.getAnimalEnclosureName = () => 'Indoor';
      assert.deepEqual(animalConfig.getTitleParts({}), {
         species: 'Tiger',
         enclosureName: 'Indoor',
      });
      AnimalSelectorModel.getAnimalSpecies = originalSpecies;
      AnimalSelectorModel.getAnimalEnclosureName = originalEnclosure;

      const transportationConfig = configs.find(
         (config) => config.getTitle === TransportationSelectorModel.getTransportationName
      );
      const opens = [];
      const originalOpen = window.open;
      window.open = (...args) => opens.push(args);
      const originalLink = TransportationSelectorModel.getTransportationInfoLink;

      TransportationSelectorModel.getTransportationInfoLink = () => 'https://example.com/ride';
      assert.equal(transportationConfig.shouldEnableTitleClick({}), true);
      transportationConfig.onTitleClick({});
      TransportationSelectorModel.getTransportationInfoLink = () => null;
      transportationConfig.onTitleClick({});
      assert.deepEqual(opens, [['https://example.com/ride', '_blank']]);

      TransportationSelectorModel.getTransportationInfoLink = originalLink;
      window.open = originalOpen;

      const attractionConfig = configs.find(
         (config) => config.getTitle === AttractionSelectorModel.getAttractionTitle
      );
      const attractionOpens = [];
      window.open = (...args) => attractionOpens.push(args);
      const originalAttractionLink = AttractionSelectorModel.getAttractionInfoLink;

      AttractionSelectorModel.getAttractionInfoLink = () => 'https://example.com/ride-attraction';
      assert.equal(attractionConfig.shouldEnableTitleClick({}), true);
      attractionConfig.onTitleClick({});
      AttractionSelectorModel.getAttractionInfoLink = () => null;
      attractionConfig.onTitleClick({});
      assert.deepEqual(attractionOpens, [['https://example.com/ride-attraction', '_blank']]);

      AttractionSelectorModel.getAttractionInfoLink = originalAttractionLink;
      window.open = originalOpen;
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = originalCreate;
   }
});

test('Test_BuildScheduleItemModuleBody_TestStrings_ExpectFields', () => {
   const originalSelect = ScheduleItemModuleFormBuilder.createSelectField;
   const originalLabel = ScheduleItemModuleFormBuilder.createFieldLabel;
   const originalCheckbox = ScheduleItemModuleFormBuilder.createOnlyItineraryItemsCheckbox;
   const originalTypes = ScheduleItemTypes.buildScheduleItemTypeOptions;
   const originalTimes = ScheduleItemTimeFields.makeScheduleItemTimeFields;

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
         searchPlaceholder: 'Find…',
         onlyItineraryItemsLabel: 'Only itinerary',
      }, ['lunch']);

      assert.ok(bodyParts.body.classList.contains('schedule-item-module-body'));
      assert.equal(bodyParts.typeSelect.tagName.toLowerCase(), 'select');
      assert.equal(bodyParts.searchInput.className, 'schedule-item-search-input');
      assert.equal(bodyParts.searchInput.placeholder, 'Find…');
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
