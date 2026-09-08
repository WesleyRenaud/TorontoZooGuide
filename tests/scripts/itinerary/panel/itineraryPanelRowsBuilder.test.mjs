import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelRowsBuilder } from '../../../../scripts/itinerary/panel/itineraryPanelRowsBuilder.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { RowActionPresenter } from '../../../../scripts/itinerary/panel/rowActionPresenter.js';
import { RowAlertPresenter } from '../../../../scripts/itinerary/panel/rowAlertPresenter.js';
import { RowBuilder } from '../../../../scripts/itinerary/panel/rowBuilder.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { ScheduledOccurrenceSorter } from '../../../../scripts/itinerary/scheduledOccurrenceSorter.js';
import { AnimalSelectorModel } from '../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { SpeciesFragment } from '../../../../scripts/overlays/speciesFragment.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _captureNamedRowConfig(methodName, items, options) {
   const originalBuildRows = RowBuilder.buildRows;
   const originalBuildNamedRows = RowBuilder.buildNamedRows;
   let captured = null;

   RowBuilder.buildRows = (sourceItems, config) => {
      captured = { sourceItems, config, via: 'buildRows' };
      return ['animal-row'];
   };
   RowBuilder.buildNamedRows = (sourceItems, config) => {
      captured = { sourceItems, config, via: 'buildNamedRows' };
      return ['named-row'];
   };

   try {
      const result = ItineraryPanelRowsBuilder[methodName](items, options);
      return { result, captured };
   } finally {
      RowBuilder.buildRows = originalBuildRows;
      RowBuilder.buildNamedRows = originalBuildNamedRows;
   }
}

test('Test_BuildAnimalRows_TestConfig_ExpectRowPropsWired', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeAnimal;
   const originalUnique = RowBuilder.buildUniqueAnimals;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalSpecies = AnimalSelectorModel.getAnimalSpecies;
   const originalEnclosure = AnimalSelectorModel.getAnimalEnclosureName;
   const originalSubtitle = AnimalSelectorModel.getAnimalSubtitle;
   const originalAlert = RowAlertPresenter.buildAnimalAlert;
   const originalImage = RowPresenter.buildImageSrc;
   const originalMeta = RowPresenter.buildMetaLines;
   const originalLink = RowPresenter.buildLinkRowProps;
   const originalActions = RowActionPresenter.buildRowScheduleActionProps;
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   const opens = [];

   ItineraryItemFormatter.normalizeAnimal = (item) => item;
   RowBuilder.buildUniqueAnimals = (items) => items;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   AnimalSelectorModel.getAnimalSpecies = () => 'Lion';
   AnimalSelectorModel.getAnimalEnclosureName = () => 'Savanna';
   AnimalSelectorModel.getAnimalSubtitle = () => 'Subtitle';
   RowAlertPresenter.buildAnimalAlert = () => ({ line: 'alert', tone: 'warn' });
   RowPresenter.buildImageSrc = () => 'img.png';
   RowPresenter.buildMetaLines = (lines) => lines;
   RowPresenter.buildLinkRowProps = () => ({ linkHref: '/x' });
   RowActionPresenter.buildRowScheduleActionProps = (...args) => ({ actionArgs: args });
   SpeciesFragment.openAnimalSpeciesOverlay = (animal) => {
      opens.push(animal);
   };

   try {
      const { result, captured } = _captureNamedRowConfig('buildAnimalRows', [{ species: 'Lion' }], {
         onUnscheduleItem: () => {},
         onScheduleItem: () => {},
         onRemoveItem: () => {},
      });

      assert.deepEqual(result, ['animal-row']);
      assert.equal(captured.via, 'buildRows');
      const props = captured.config.buildRowProps({ species: 'Lion', exhibit: 'Savanna', link: '/a' });
      assert.equal(props.species, 'Lion');
      assert.equal(props.enclosureName, 'Savanna');
      assert.equal(props.imageSrc, 'img.png');
      assert.equal(props.alertLine, 'alert');
      assert.equal(props.linkHref, '/x');
      assert.equal(props.actionArgs[0], ScheduleItemKind.ANIMAL.itemType);
      props.onNameClick();
      assert.equal(opens.length, 1);
      assert.equal(captured.config.normalizeItem, ItineraryItemFormatter.normalizeAnimal);
   } finally {
      ItineraryItemFormatter.normalizeAnimal = originalNormalize;
      RowBuilder.buildUniqueAnimals = originalUnique;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      AnimalSelectorModel.getAnimalSpecies = originalSpecies;
      AnimalSelectorModel.getAnimalEnclosureName = originalEnclosure;
      AnimalSelectorModel.getAnimalSubtitle = originalSubtitle;
      RowAlertPresenter.buildAnimalAlert = originalAlert;
      RowPresenter.buildImageSrc = originalImage;
      RowPresenter.buildMetaLines = originalMeta;
      RowPresenter.buildLinkRowProps = originalLink;
      RowActionPresenter.buildRowScheduleActionProps = originalActions;
      SpeciesFragment.openAnimalSpeciesOverlay = originalOpen;
   }
});

test('Test_BuildAttractionRows_TestConfig_ExpectNamedRows', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeAttraction;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalField = RowPresenter.buildFieldLine;
   const originalApprox = RowPresenter.buildApproximateStartTimeFieldLine;
   const originalAlert = RowAlertPresenter.buildAttractionRemovalReasonLine;
   const originalTitleLink = RowPresenter.buildTitleLinkRowProps;
   const originalActions = RowActionPresenter.buildRowScheduleActionProps;

   ItineraryItemFormatter.normalizeAttraction = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildApproximateStartTimeFieldLine = () => 'approx';
   RowAlertPresenter.buildAttractionRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRowScheduleActionProps = () => ({ actions: true });

   try {
      const { result, captured } = _captureNamedRowConfig(
         'buildAttractionRows',
         [{ name: 'Carousel', subtitle: 'Fun', region: 'Americas', price: '$5', infoLink: '/i' }],
         { onRemoveItem: () => {} }
      );

      assert.deepEqual(result, ['named-row']);
      assert.equal(captured.via, 'buildNamedRows');
      assert.equal(captured.config.getName({ name: 'Carousel' }), 'Carousel');
      assert.deepEqual(
         captured.config.getMetaLines({
            subtitle: 'Fun',
            region: 'Americas',
            price: '$5',
         }),
         ['Fun', 'Location:Americas', 'Price:$5', 'approx']
      );
      assert.deepEqual(captured.config.extendRowProps({ infoLink: '/i' }), {
         titleLink: true,
         actions: true,
      });
   } finally {
      ItineraryItemFormatter.normalizeAttraction = originalNormalize;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      RowPresenter.buildFieldLine = originalField;
      RowPresenter.buildApproximateStartTimeFieldLine = originalApprox;
      RowAlertPresenter.buildAttractionRemovalReasonLine = originalAlert;
      RowPresenter.buildTitleLinkRowProps = originalTitleLink;
      RowActionPresenter.buildRowScheduleActionProps = originalActions;
   }
});

test('Test_BuildTransportationRows_TestConfig_ExpectNamedRows', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeTransportation;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalName = TransportationSelectorModel.getTransportationName;
   const originalStations = TransportationSelectorModel.buildTransportationStationsLine;
   const originalApprox = RowPresenter.buildApproximateStartTimeFieldLine;
   const originalAlert = RowAlertPresenter.buildAttractionRemovalReasonLine;
   const originalTitleLink = RowPresenter.buildTitleLinkRowProps;
   const originalActions = RowActionPresenter.buildRowScheduleActionProps;

   ItineraryItemFormatter.normalizeTransportation = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   TransportationSelectorModel.getTransportationName = () => 'Zoomobile';
   TransportationSelectorModel.buildTransportationStationsLine = () => 'A → B';
   RowPresenter.buildApproximateStartTimeFieldLine = () => 'approx';
   RowAlertPresenter.buildAttractionRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRowScheduleActionProps = () => ({ actions: true });

   try {
      const { captured } = _captureNamedRowConfig('buildTransportationRows', [{ name: 'Zoomobile' }]);
      assert.equal(captured.config.getName({}), 'Zoomobile');
      assert.deepEqual(captured.config.getMetaLines({}), ['A → B', 'approx']);
   } finally {
      ItineraryItemFormatter.normalizeTransportation = originalNormalize;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      TransportationSelectorModel.getTransportationName = originalName;
      TransportationSelectorModel.buildTransportationStationsLine = originalStations;
      RowPresenter.buildApproximateStartTimeFieldLine = originalApprox;
      RowAlertPresenter.buildAttractionRemovalReasonLine = originalAlert;
      RowPresenter.buildTitleLinkRowProps = originalTitleLink;
      RowActionPresenter.buildRowScheduleActionProps = originalActions;
   }
});

test('Test_BuildGuardiansRows_TestLinkedAnimal_ExpectOnNameClick', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeTalk;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalName = GuardiansTalkSelectorModel.getGuardiansTalkName;
   const originalSuffix = GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix;
   const originalField = RowPresenter.buildFieldLine;
   const originalScheduled = RowPresenter.buildScheduledTimeFieldLine;
   const originalAlert = RowAlertPresenter.buildGuardiansRemovalReasonLine;
   const originalRemove = RowActionPresenter.buildRemoveRowProps;
   const originalLinked = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal;
   const originalOpen = GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal;
   const opens = [];

   ItineraryItemFormatter.normalizeTalk = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   GuardiansTalkSelectorModel.getGuardiansTalkName = () => 'Tiger Talk';
   GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix = () => 'Talk';
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildScheduledTimeFieldLine = () => 'time';
   RowAlertPresenter.buildGuardiansRemovalReasonLine = () => 'alert';
   RowActionPresenter.buildRemoveRowProps = () => ({ remove: true });
   GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = () => ({ species: 'Tiger' });
   GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = async (talk) => {
      opens.push(talk);
   };

   try {
      const { captured } = _captureNamedRowConfig(
         'buildGuardiansRows',
         [{ name: 'Tiger Talk', location: 'Eurasia', link: '/t' }],
         { onRemoveItem: () => {} }
      );
      const props = captured.config.extendRowProps({ name: 'Tiger Talk' });
      assert.equal(typeof props.onNameClick, 'function');
      props.onNameClick();
      assert.equal(opens.length, 1);
      assert.equal(props.remove, true);
   } finally {
      ItineraryItemFormatter.normalizeTalk = originalNormalize;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      GuardiansTalkSelectorModel.getGuardiansTalkName = originalName;
      GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix = originalSuffix;
      RowPresenter.buildFieldLine = originalField;
      RowPresenter.buildScheduledTimeFieldLine = originalScheduled;
      RowAlertPresenter.buildGuardiansRemovalReasonLine = originalAlert;
      RowActionPresenter.buildRemoveRowProps = originalRemove;
      GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = originalLinked;
      GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = originalOpen;
   }
});

test('Test_BuildWildRows_TestConfig_ExpectNamedRows', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeWild;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalName = WildEncounterSelectorModel.getWildEncounterName;
   const originalSuffix = WildEncounterSelectorModel.getWildEncounterTitleSuffix;
   const originalField = RowPresenter.buildFieldLine;
   const originalScheduled = RowPresenter.buildScheduledTimeFieldLine;
   const originalAlert = RowAlertPresenter.buildWildRemovalReasonLine;
   const originalTitleLink = RowPresenter.buildTitleLinkRowProps;
   const originalRemove = RowActionPresenter.buildRemoveRowProps;

   ItineraryItemFormatter.normalizeWild = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   WildEncounterSelectorModel.getWildEncounterName = () => 'Capybara';
   WildEncounterSelectorModel.getWildEncounterTitleSuffix = () => 'Encounter';
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildScheduledTimeFieldLine = () => 'time';
   RowAlertPresenter.buildWildRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRemoveRowProps = () => ({ remove: true });

   try {
      const { captured } = _captureNamedRowConfig(
         'buildWildRows',
         [{ name: 'Capybara', meeting_spot: 'Spot', link: '/w' }],
         { onRemoveItem: () => {} }
      );
      assert.equal(captured.config.getName({}), 'Capybara');
      assert.deepEqual(
         captured.config.getMetaLines({ meeting_spot: 'Spot' })[0].includes('Spot'),
         true
      );
      assert.deepEqual(captured.config.extendRowProps({ link: '/w' }), {
         titleLink: true,
         remove: true,
      });
   } finally {
      ItineraryItemFormatter.normalizeWild = originalNormalize;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      WildEncounterSelectorModel.getWildEncounterName = originalName;
      WildEncounterSelectorModel.getWildEncounterTitleSuffix = originalSuffix;
      RowPresenter.buildFieldLine = originalField;
      RowPresenter.buildScheduledTimeFieldLine = originalScheduled;
      RowAlertPresenter.buildWildRemovalReasonLine = originalAlert;
      RowPresenter.buildTitleLinkRowProps = originalTitleLink;
      RowActionPresenter.buildRemoveRowProps = originalRemove;
   }
});
