import assert from 'node:assert/strict';
import test from 'node:test';

import { CreateScheduledOccurrenceSelector } from '../../../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import { StoredSelectionNormalizer } from '../../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { ScheduledOccurrencePresenter } from '../../../../scripts/itinerary/scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceSelectorFactory } from '../../../../scripts/itinerary/selectors/scheduledOccurrenceSelectorFactory.js';
import { ScheduledOccurrenceSorter } from '../../../../scripts/itinerary/scheduledOccurrenceSorter.js';
import { ScheduledOccurrenceTimeModel } from '../../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';
import { SelectorControllerFactory } from '../../../../scripts/itinerary/selectors/selectorControllerFactory.js';
import { ItinerarySearchContext } from '../../../../scripts/itinerary/itinerarySearchContext.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateScheduledOccurrenceMigration_TestItems_ExpectNormalizerWired', () => {
   const originalMigrate = StoredSelectionNormalizer.migrateStoredSelectionItems;
   const originalFromString = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString;
   const originalFromObject = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject;
   const name = 'Talk';
   const emptyStoredFields = { region: '' };
   const includeLink = true;
   StoredSelectionNormalizer.migrateStoredSelectionItems = (items, options) => ({
      items,
      fromString: options.fromString(name),
      fromObject: options.fromObject({ name }),
   });
   ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString = (item, options) => ({
      kind: 'string',
      item,
      emptyStoredFields: options.emptyStoredFields,
      image: options.buildImageSrc(item),
   });
   ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject = (item, options) => ({
      kind: 'object',
      item,
      includeLink: options.includeLink,
      id: options.getId(item),
   });

   try {
      const migrate = CreateScheduledOccurrenceSelector.createScheduledOccurrenceMigration({
         emptyStoredFields,
         buildImageSrc: (value) => `img:${value}`,
         includeLink,
         getId: (row) => row.name,
      });
      const migrated = migrate([name]);

      assert.deepEqual(migrated.items, [name]);
      assert.equal(migrated.fromString.item, name);
      assert.deepEqual(migrated.fromString.emptyStoredFields, emptyStoredFields);
      assert.equal(migrated.fromString.image, `img:${name}`);
      assert.equal(migrated.fromObject.item.name, name);
      assert.equal(migrated.fromObject.includeLink, includeLink);
      assert.equal(migrated.fromObject.id, name);
   } finally {
      StoredSelectionNormalizer.migrateStoredSelectionItems = originalMigrate;
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString = originalFromString;
      ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject = originalFromObject;
   }
});


test('Test_CreateScheduledOccurrenceSelectorController_TestConfig_ExpectFactoryArgs', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   const originalBuildImage = ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc;
   const originalMakeSelection = ScheduledOccurrenceSelectorFactory.createOccurrenceSelection;
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalSubtitle = ScheduledOccurrencePresenter.buildOccurrenceSubtitle;
   const originalTimeRange = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange;
   const originalGetContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const opens = [];
   const originalOpen = window.open;
   let captured;
   const controllerResult = { controller: true };
   const storageKey = 'talks';
   const searchFlag = 'includeGuardiansTalks';
   const imageDirectory = 'guardians-talks';
   const defaultTitle = 'Talk';
   const heading = 'Choose a talk';
   const query = 'tiger';
   const talkName = 'Amur Tiger';
   const region = 'Asia';
   const startTime = '11:00 AM';
   const href = 'https://zoo.example/talk';
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return controllerResult;
   };
   ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc = (dir, name) => `${dir}/${name}.jpg`;
   ScheduledOccurrenceSelectorFactory.createOccurrenceSelection = (row) => ({ selected: row.name });
   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (rows) => rows;
   ScheduledOccurrencePresenter.buildOccurrenceSubtitle = ({ primaryValue, timeRange }) => (
      `${primaryValue}|${timeRange}`
   );
   ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = (row) => row.start_time;
   ItinerarySearchContext.getItineraryDateSearchContext = () => ({ date: '2026-01-01' });
   window.open = (...args) => opens.push(args);

   try {
      const controller = CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController({
         mountEl: document.createElement('div'),
         storageKey,
         responseKey: 'guardiansTalks',
         searchFlag,
         imageDirectory,
         defaultTitle,
         heading,
         subtitle: 'Pick one',
         emptyText: 'None',
         getPrimaryValue: (row) => row.region,
         getLink: (row) => row.link,
         buildSelectionFields: () => ({}),
      });

      assert.deepEqual(controller, controllerResult);
      assert.equal(captured.storageKey, storageKey);
      assert.deepEqual(captured.buildSearchPayload(query), {
         query,
         [searchFlag]: true,
      });
      const rows = [{ name: 'A', start_time: '10:00 AM' }];
      assert.deepEqual(captured.extractRows({ guardiansTalks: rows }), rows);
      assert.equal(captured.getTitle({ name: talkName }), talkName);
      assert.equal(captured.getTitle({}), defaultTitle);
      assert.equal(
         captured.getSubtitle({ region, start_time: startTime }),
         `${region}|${startTime}`
      );
      assert.equal(captured.getImageSrc({ name: talkName }), `${imageDirectory}/${talkName}.jpg`);
      assert.equal(captured.getInfoLink(), null);
      assert.deepEqual(captured.makeSelection({ name: talkName }), { selected: talkName });
      captured.onTitleClick({ link: href });
      captured.onTitleClick({});
      assert.deepEqual(opens.at(Position.FIRST), [href, '_blank']);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
      ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc = originalBuildImage;
      ScheduledOccurrenceSelectorFactory.createOccurrenceSelection = originalMakeSelection;
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      ScheduledOccurrencePresenter.buildOccurrenceSubtitle = originalSubtitle;
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange = originalTimeRange;
      ItinerarySearchContext.getItineraryDateSearchContext = originalGetContext;
      window.open = originalOpen;
   }
});


test('Test_CreateScheduledOccurrenceSelectorController_TestNoLink_ExpectNullTitleClick', () => {
   const originalCreate = SelectorControllerFactory.createItinerarySelectorController;
   let captured;
   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return {};
   };

   try {
      CreateScheduledOccurrenceSelector.createScheduledOccurrenceSelectorController({
         storageKey: 'talks',
         responseKey: 'guardiansTalks',
         searchFlag: 'includeGuardiansTalks',
         imageDirectory: 'guardians-talks',
         defaultTitle: 'Talk',
         heading: 'Choose',
         subtitle: 'Sub',
         emptyText: 'Empty',
         getPrimaryValue: () => null,
      });

      assert.equal(captured.onTitleClick, null);
   } finally {
      SelectorControllerFactory.createItinerarySelectorController = originalCreate;
   }
});
