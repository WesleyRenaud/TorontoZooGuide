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
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateScheduledOccurrenceMigration_TestItems_ExpectNormalizerWired', () => {
   const originalMigrate = StoredSelectionNormalizer.migrateStoredSelectionItems;
   const originalFromString = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromString;
   const originalFromObject = ScheduledOccurrenceSelectorFactory.createStoredOccurrenceFromObject;

   StoredSelectionNormalizer.migrateStoredSelectionItems = (items, options) => ({
      items,
      fromString: options.fromString('Talk'),
      fromObject: options.fromObject({ name: 'Talk' }),
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
         emptyStoredFields: { region: '' },
         buildImageSrc: (name) => `img:${name}`,
         includeLink: true,
         getId: (row) => row.name,
      });

      assert.deepEqual(migrate(['Talk']), {
         items: ['Talk'],
         fromString: {
            kind: 'string',
            item: 'Talk',
            emptyStoredFields: { region: '' },
            image: 'img:Talk',
         },
         fromObject: {
            kind: 'object',
            item: { name: 'Talk' },
            includeLink: true,
            id: 'Talk',
         },
      });
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

   SelectorControllerFactory.createItinerarySelectorController = (options) => {
      captured = options;
      return { controller: true };
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
         storageKey: 'talks',
         responseKey: 'guardiansTalks',
         searchFlag: 'includeGuardiansTalks',
         imageDirectory: 'guardians-talks',
         defaultTitle: 'Talk',
         heading: 'Choose a talk',
         subtitle: 'Pick one',
         emptyText: 'None',
         getPrimaryValue: (row) => row.region,
         getLink: (row) => row.link,
         buildSelectionFields: () => ({}),
      });

      assert.deepEqual(controller, { controller: true });
      assert.equal(captured.storageKey, 'talks');
      assert.deepEqual(captured.buildSearchPayload('tiger'), {
         query: 'tiger',
         includeGuardiansTalks: true,
      });
      assert.deepEqual(
         captured.extractRows({ guardiansTalks: [{ name: 'A', start_time: '10:00 AM' }] }),
         [{ name: 'A', start_time: '10:00 AM' }]
      );
      assert.equal(captured.getTitle({ name: 'Amur Tiger' }), 'Amur Tiger');
      assert.equal(captured.getTitle({}), 'Talk');
      assert.equal(
         captured.getSubtitle({ region: 'Asia', start_time: '11:00 AM' }),
         'Asia|11:00 AM'
      );
      assert.equal(captured.getImageSrc({ name: 'Amur Tiger' }), 'guardians-talks/Amur Tiger.jpg');
      assert.equal(captured.getInfoLink(), null);
      assert.deepEqual(captured.makeSelection({ name: 'Amur Tiger' }), { selected: 'Amur Tiger' });

      captured.onTitleClick({ link: 'https://zoo.example/talk' });
      captured.onTitleClick({});
      assert.deepEqual(opens, [['https://zoo.example/talk', '_blank']]);
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
