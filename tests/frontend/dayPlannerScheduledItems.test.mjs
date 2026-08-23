import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildScheduledItemRowsContext, buildScheduledItinerary } from '../../scripts/itinerary/panel/dayPlannerScheduledItems.js';
import {
   resolveGroupedScheduledPillOptions,
   resolveScheduledPillOptions,
} from '../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { allTextFor } from './helpers/panelRowsTestSetup.mjs';
import { makeScheduledItem } from './helpers/scheduledPillTestSetup.mjs';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

test('resolveGroupedScheduledPillOptions merges menu actions for grouped pills', () => {
   const options = resolveGroupedScheduledPillOptions(
      [
         makeScheduledItem('African Lion', 570),
         makeScheduledItem('Cheetah', 570),
      ],
      {
         onUnscheduleItineraryItem: () => {},
         onRemoveItineraryItem: () => {},
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(options.menuItems?.length, 4);
});

test('buildScheduledItemRowsContext places generic events on the timeline', () => {
   const context = buildScheduledItemRowsContext(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         events: [
            {
               event_type: 'lunch',
               start_time: '12:00 PM',
               end_time: '12:40 PM',
            },
         ],
      },
      [720, 750],
      1140
   );
   const lunchItems = [...context.itemsByStart.values()].flat();

   assert.equal(lunchItems.length, 1);
   assert.equal(lunchItems[0].label, 'Lunch');
   assert.equal(lunchItems[0].scheduleItemKind, ScheduleItemKind.EVENT.kind);
   assert.equal(lunchItems[0].scheduleItemEventType, 'lunch');
   assert.equal(lunchItems[0].maximumDuration, 40);
   assert.equal(lunchItems[0].anchorSlotMinutes, 720);
});

test('resolveScheduledPillOptions offers only remove for generic events', () => {
   const removeRequests = [];

   const options = resolveScheduledPillOptions(
      {
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: 'lunch',
         scheduleItemKey: '',
      },
      {
         onUnscheduleItineraryItem: () => {
            throw new Error('generic events should not expose unschedule');
         },
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(options.menuItems?.length, 1);
   assert.equal(options.menuItems?.[0]?.label, 'Remove');

   options.menuItems?.[0]?.onAction?.();

   assert.deepEqual(removeRequests, [{
      itemType: 'lunch',
      key: '',
   }]);
});

test('resolveScheduledPillOptions adds remove for animals and guardians talks', () => {
   const removeRequests = [];

   const animalOptions = resolveScheduledPillOptions(
      {
         scheduleItemKind: 'animals',
         scheduleItemKey: 'African Lion||Africa Savanna',
      },
      {
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   animalOptions.menuItems?.find((item) => item.label === 'Remove')?.onAction?.();

   assert.deepEqual(removeRequests, [{
      itemType: 'animals',
      key: 'African Lion||Africa Savanna',
   }]);

   const talkOptions = resolveScheduledPillOptions(
      {
         scheduleItemKind: 'guardians_talks',
         scheduleItemKey: 'Amur Tiger||1:30 PM||2:00 PM',
      },
      {
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(talkOptions.menuItems?.length, 1);
   assert.equal(talkOptions.menuItems?.[0]?.label, 'Remove');

   talkOptions.menuItems?.[0]?.onAction?.();

   assert.deepEqual(removeRequests[1], {
      itemType: 'guardians_talks',
      key: 'Amur Tiger||1:30 PM||2:00 PM',
   });
});

test.describe('buildScheduledItemRowsContext scheduled animals', () => {
   installDomTestHooks();

   test('keeps separate scheduled animals per viewing spot', () => {
      const context = buildScheduledItemRowsContext(
         {
            animals: [
               {
                  species: 'Western Lowland Gorilla',
                  exhibit: 'African Rainforest Pavilion',
                  enclosure_name: 'Indoor',
                  start_time: '9:30 AM',
                  end_time: '9:35 AM',
               },
               {
                  species: 'Western Lowland Gorilla',
                  exhibit: 'African Rainforest Pavilion',
                  enclosure_name: 'Outdoor',
                  start_time: '9:40 AM',
                  end_time: '9:45 AM',
               },
            ],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            events: [],
         },
         [570, 600],
         1140
      );
      const animalItems = [...context.itemsByStart.values()].flat()
         .filter((item) => item.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType);

      assert.equal(animalItems.length, 2);
      assert.deepEqual(
         animalItems.map((item) => item.scheduleItemKey).sort(),
         [
            'Western Lowland Gorilla||African Rainforest Pavilion||Indoor',
            'Western Lowland Gorilla||African Rainforest Pavilion||Outdoor',
         ]
      );
      assert.equal(context.scheduledAnimalIndexes.size, 2);
   });

   test('omits covered-by-talk animals from timeline pills but keeps them scheduled', () => {
      const context = buildScheduledItemRowsContext(
         {
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  enclosure_name: null,
                  start_time: '11:00 AM',
                  end_time: '11:30 AM',
                  covered_by_talk: true,
               },
               {
                  species: 'Cheetah',
                  exhibit: 'Africa Savanna',
                  enclosure_name: null,
                  start_time: '11:40 AM',
                  end_time: '11:45 AM',
                  covered_by_talk: false,
               },
            ],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            events: [],
         },
         [660, 690, 720],
         1140
      );
      const animalItems = [...context.itemsByStart.values()].flat()
         .filter((item) => item.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType);

      assert.equal(animalItems.length, 1);
      assert.equal(animalItems[0].item.species, 'Cheetah');
      assert.equal(context.scheduledAnimalIndexes.size, 2);
   });
});

test('buildScheduledItinerary tolerates missing itinerary collections', () => {
   assert.deepEqual(buildScheduledItinerary({}), {
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
});

test.describe('buildScheduledItemRowsContext transportation', () => {
   installDomTestHooks();

   test('renders transportation with station range', () => {
      const context = buildScheduledItemRowsContext(
         {
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            transportations: [
               {
                  name: 'Zoomobile',
                  added_as_attraction: false,
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
                  legs: [
                     {
                        from_station: 'Main Station',
                        to_station: 'Canadian Domain',
                        start_time: '2:30 PM',
                        end_time: '2:40 PM',
                     },
                     {
                        from_station: 'Canadian Domain',
                        to_station: 'Wildlife Health',
                        start_time: '2:40 PM',
                        end_time: '3:00 PM',
                     },
                  ],
               },
            ],
            events: [],
         },
         [870, 900],
         1140
      );
      const transportationItems = [...context.itemsByStart.values()].flat()
         .filter((item) => (
            item.scheduleItemKind === ScheduleItemKind.TRANSPORTATION.itemType
         ));

      assert.equal(transportationItems.length, 1);
      assert.equal(transportationItems[0].label, 'Zoomobile');
      assert.equal(transportationItems[0].scheduleItemKey, 'Zoomobile||0');
      assert.equal(context.scheduledTransportationIndexes.size, 1);
      assert.match(
         allTextFor(transportationItems[0].row),
         /Main Station - Wildlife Health/
      );
   });
});

test('buildScheduledItemRowsContext omits deleted wild encounters from the timeline', () => {
   const context = buildScheduledItemRowsContext(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [
            {
               name: 'Kangaroo',
               meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
               start_time: '3:30 PM',
               end_time: '4:15 PM',
               maximum_duration: 45,
               is_deleted: true,
            },
         ],
         events: [],
      },
      [870, 900],
      1140
   );

   assert.equal([...context.itemsByStart.values()].flat().length, 0);
   assert.equal(context.scheduledWildEncounterIndexes.size, 0);
});

test('buildScheduledItemRowsContext omits deleted guardians talks from the timeline', () => {
   const context = buildScheduledItemRowsContext(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [
            {
               name: 'North American River Otter',
               location: 'Americas Pavilion',
               start_time: '2:00 PM',
               end_time: '2:15 PM',
               maximum_duration: 15,
               is_deleted: true,
            },
         ],
         wildEncounters: [],
         events: [],
      },
      [840, 870],
      1140
   );

   assert.equal([...context.itemsByStart.values()].flat().length, 0);
   assert.equal(context.scheduledGuardiansTalkIndexes.size, 0);
});
