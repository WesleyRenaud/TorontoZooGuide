import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLinkedAnimalOpener } from '../../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryPanelRowsBuilder } from '../../../../scripts/itinerary/panel/itineraryPanelRowsBuilder.js';
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
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

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

installDomTestHooks();


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
   const species = 'African Lion';
   const enclosureName = 'Africa Savanna';
   const imageSrc = 'img.png';
   const alertLine = 'alert';
   const linkHref = '/x';
   const animalRow = 'animal-row';
   ItineraryItemFormatter.normalizeAnimal = (item) => item;
   RowBuilder.buildUniqueAnimals = (items) => items;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   AnimalSelectorModel.getAnimalSpecies = () => species;
   AnimalSelectorModel.getAnimalEnclosureName = () => enclosureName;
   AnimalSelectorModel.getAnimalSubtitle = () => 'Subtitle';
   RowAlertPresenter.buildAnimalAlert = () => ({ line: alertLine, tone: 'warn' });
   RowPresenter.buildImageSrc = () => imageSrc;
   RowPresenter.buildMetaLines = (lines) => lines;
   RowPresenter.buildLinkRowProps = () => ({ linkHref });
   RowActionPresenter.buildRowScheduleActionProps = (...args) => ({ actionArgs: args });
   SpeciesFragment.openAnimalSpeciesOverlay = (animal) => {
      opens.push(animal);
   };

   try {
      const { result, captured } = _captureNamedRowConfig('buildAnimalRows', [{ species }], {
         onUnscheduleItem: () => {},
         onScheduleItem: () => {},
         onRemoveItem: () => {},
      });
      const props = captured.config.buildRowProps({ species, exhibit: enclosureName, link: '/a' });

      assert.deepEqual(result, [animalRow]);
      assert.equal(captured.via, 'buildRows');
      assert.equal(props.species, species);
      assert.equal(props.enclosureName, enclosureName);
      assert.equal(props.imageSrc, imageSrc);
      assert.equal(props.alertLine, alertLine);
      assert.equal(props.linkHref, linkHref);
      assert.equal(props.actionArgs.at(Position.FIRST), ScheduleItemKind.ANIMAL.itemType);
      props.onNameClick();
      assert.equal(opens.length, Position.SECOND);
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


test('Test_BuildAnimalRows_TestTransportationOnlyAnimals_ExpectOmitted', () => {
   const lion = { species: 'African Lion' };
   const giraffe = { species: 'Masai Giraffe', added_by_transportation: true };

   const { captured } = _captureNamedRowConfig('buildAnimalRows', [lion, giraffe]);

   assert.deepEqual(captured.sourceItems, [lion]);
});


test('Test_BuildAttractionRows_TestConfig_ExpectNamedRows', () => {
   const originalNormalize = ItineraryItemFormatter.normalizeAttraction;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalField = RowPresenter.buildFieldLine;
   const originalApprox = RowPresenter.buildApproximateStartTimeFieldLine;
   const originalAlert = RowAlertPresenter.buildAttractionRemovalReasonLine;
   const originalTitleLink = RowPresenter.buildTitleLinkRowProps;
   const originalActions = RowActionPresenter.buildRowScheduleActionProps;
   const name = 'Conservation Carousel';
   const subtitle = 'Fun';
   const region = 'Americas';
   const price = '$5';
   const infoLink = '/i';
   const approx = 'approx';
   ItineraryItemFormatter.normalizeAttraction = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildApproximateStartTimeFieldLine = () => approx;
   RowAlertPresenter.buildAttractionRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRowScheduleActionProps = () => ({ actions: true });

   try {
      const { result, captured } = _captureNamedRowConfig(
         'buildAttractionRows',
         [{ name, subtitle, region, price, infoLink }],
         { onRemoveItem: () => {} }
      );
      const metaLines = captured.config.getMetaLines({ subtitle, region, price });
      const extended = captured.config.extendRowProps({ infoLink });

      assert.deepEqual(result, ['named-row']);
      assert.equal(captured.via, 'buildNamedRows');
      assert.equal(captured.config.getName({ name }), name);
      assert.deepEqual(metaLines, [
         subtitle,
         RowPresenter.buildFieldLine('Location', region),
         RowPresenter.buildFieldLine('Price', price),
         approx,
      ]);
      assert.deepEqual(extended, {
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
   const name = 'Zoomobile';
   const stationsLine = 'A → B';
   const approx = 'approx';
   ItineraryItemFormatter.normalizeTransportation = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   TransportationSelectorModel.getTransportationName = () => name;
   TransportationSelectorModel.buildTransportationStationsLine = () => stationsLine;
   RowPresenter.buildApproximateStartTimeFieldLine = () => approx;
   RowAlertPresenter.buildAttractionRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRowScheduleActionProps = () => ({ actions: true });

   try {
      const { captured } = _captureNamedRowConfig('buildTransportationRows', [{ name }]);
      const metaLines = captured.config.getMetaLines({});

      assert.equal(captured.config.getName({}), name);
      assert.deepEqual(metaLines, [stationsLine, approx]);
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
   const talkName = 'Amur Tiger';
   ItineraryItemFormatter.normalizeTalk = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   GuardiansTalkSelectorModel.getGuardiansTalkName = () => talkName;
   GuardiansTalkSelectorModel.getGuardiansTalkTitleSuffix = () => 'Talk';
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildScheduledTimeFieldLine = () => 'time';
   RowAlertPresenter.buildGuardiansRemovalReasonLine = () => 'alert';
   RowActionPresenter.buildRemoveRowProps = () => ({ remove: true });
   GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal = () => ({ species: talkName });
   GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal = async (talk) => {
      opens.push(talk);
   };

   try {
      const { captured } = _captureNamedRowConfig(
         'buildGuardiansRows',
         [{ name: talkName, location: 'Eurasia Wilds', link: '/t' }],
         { onRemoveItem: () => {} }
      );
      const props = captured.config.extendRowProps({ name: talkName });

      assert.equal(typeof props.onNameClick, 'function');
      props.onNameClick();
      assert.equal(opens.length, Position.SECOND);
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
   const encounterName = 'Capybara';
   const meetingSpot = 'Spot';
   const link = '/w';
   ItineraryItemFormatter.normalizeWild = (item) => item;
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   WildEncounterSelectorModel.getWildEncounterName = () => encounterName;
   WildEncounterSelectorModel.getWildEncounterTitleSuffix = () => 'Encounter';
   RowPresenter.buildFieldLine = (label, value) => `${label}:${value}`;
   RowPresenter.buildScheduledTimeFieldLine = () => 'time';
   RowAlertPresenter.buildWildRemovalReasonLine = () => 'alert';
   RowPresenter.buildTitleLinkRowProps = () => ({ titleLink: true });
   RowActionPresenter.buildRemoveRowProps = () => ({ remove: true });

   try {
      const { captured } = _captureNamedRowConfig(
         'buildWildRows',
         [{ name: encounterName, meeting_spot: meetingSpot, link }],
         { onRemoveItem: () => {} }
      );
      const metaLines = captured.config.getMetaLines({ meeting_spot: meetingSpot });
      const extended = captured.config.extendRowProps({ link });

      assert.equal(captured.config.getName({}), encounterName);
      assert.equal(metaLines.at(Position.FIRST).includes(meetingSpot), true);
      assert.deepEqual(extended, {
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
