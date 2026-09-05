import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerScheduledItems } from '../../../../scripts/itinerary/panel/dayPlannerScheduledItems.js';
import { DayPlannerScheduledPillOptions } from '../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { allTextFor } from '../../helpers/panelRowsTestSetup.mjs';
import { makeScheduledItem } from '../../helpers/scheduledPillTestSetup.mjs';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_ResolveScheduledPillOptions_TestPureTransportations_ExpectHideUnschedule', () => {
   const options = DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
      {
         scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
         scheduleItemKey: 'Zoomobile||0',
         item: {
            name: 'Zoomobile',
            added_as_attraction: false,
            start_time: '2:30 PM',
            end_time: '3:00 PM',
         },
      },
      {
         onUnscheduleItineraryItem: () => {
            throw new Error('pure transportations should not expose unschedule');
         },
         onRemoveItineraryItem: () => {},
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.deepEqual(
      options.menuItems?.map((item) => item.label),
      ['Remove']
   );
});

test('Test_ResolveScheduledPillOptions_TestAddedAsAttraction_ExpectKeepUnschedule', () => {
   const options = DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
      {
         scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
         scheduleItemKey: 'Zoomobile||1',
         item: {
            name: 'Zoomobile',
            added_as_attraction: true,
            start_time: '2:30 PM',
            end_time: '3:00 PM',
         },
      },
      {
         onUnscheduleItineraryItem: () => {},
         onRemoveItineraryItem: () => {},
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.deepEqual(
      options.menuItems?.map((item) => item.label),
      ['Unschedule', 'Remove']
   );
});

test('Test_ResolveGroupedScheduledPillOptions_TestGroupedPills_ExpectMergedMenus', () => {
   const options = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
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

test('Test_BuildScheduledItemRowsContext_TestGenericEvents_ExpectOnTimeline', () => {
   const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
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

test('Test_ResolveScheduledPillOptions_TestGenericEvents_ExpectOnlyRemove', () => {
   const removeRequests = [];

   const options = DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
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

test('Test_ResolveScheduledPillOptions_TestAnimalsAndTalks_ExpectRemove', () => {
   const removeRequests = [];

   const animalOptions = DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
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

   const talkOptions = DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
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

test.describe('Test_BuildScheduledItemRowsContext_TestScheduledAnimals', () => {
   installDomTestHooks();

   test('Test_BuildScheduledItemRowsContext_TestSeparateViewingSpots_ExpectDistinct', () => {
      const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
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

   test('Test_BuildScheduledItemRowsContext_TestCoveredByTalk_ExpectOmitPillKeepScheduled', () => {
      const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
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

test('Test_BuildScheduledItinerary_TestMissingCollections_ExpectEmpty', () => {
   assert.deepEqual(DayPlannerScheduledItems.buildScheduledItinerary({}), {
      animals: [],
      attractions: [],
      transportations: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
});

test.describe('Test_BuildScheduledItemRowsContext_TestTransportation', () => {
   installDomTestHooks();

   test('Test_BuildScheduledItemRowsContext_TestStationRange_ExpectRendered', () => {
      const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
         {
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            transportations: [
               {
                  name: 'Zoomobile',
                  added_as_attraction: false,
                  bulk_transit_evaluated: true,
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
         /Main Station → Wildlife Health/
      );
   });

   test('Test_BuildScheduledItemRowsContext_TestDiscontinuousRides_ExpectSplitPills', () => {
      const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
         {
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            transportations: [
               {
                  name: 'Zoomobile',
                  added_as_attraction: false,
                  bulk_transit_evaluated: true,
                  start_time: '9:00 AM',
                  end_time: '11:19 AM',
                  legs: [
                     {
                        from_station: 'Main Zoomobile Station',
                        to_station: 'Canadian Domain Zoomobile Station',
                        start_time: '9:00 AM',
                        end_time: '9:20 AM',
                     },
                     {
                        from_station: 'Canadian Domain Zoomobile Station',
                        to_station: 'Africa Zoomobile Station',
                        start_time: '9:20 AM',
                        end_time: '9:30 AM',
                     },
                     {
                        from_station: 'Canadian Domain Zoomobile Station',
                        to_station: 'Africa Zoomobile Station',
                        start_time: '10:24 AM',
                        end_time: '10:34 AM',
                     },
                     {
                        from_station: 'Africa Zoomobile Station',
                        to_station: 'Tundra Zoomobile Station',
                        start_time: '10:34 AM',
                        end_time: '10:49 AM',
                     },
                     {
                        from_station: 'Tundra Zoomobile Station',
                        to_station: 'Eurasia Zoomobile Station',
                        start_time: '10:49 AM',
                        end_time: '11:04 AM',
                     },
                     {
                        from_station: 'Eurasia Zoomobile Station',
                        to_station: 'Main Zoomobile Station',
                        start_time: '11:04 AM',
                        end_time: '11:19 AM',
                     },
                  ],
               },
            ],
            events: [],
         },
         [540, 570, 600, 630, 660, 690],
         1140
      );
      const transportationItems = [...context.itemsByStart.values()].flat()
         .filter((item) => (
            item.scheduleItemKind === ScheduleItemKind.TRANSPORTATION.itemType
         ))
         .sort((left, right) => left.startMinutes - right.startMinutes);

      assert.equal(transportationItems.length, 2);
      assert.equal(transportationItems[0].startMinutes, 540);
      assert.equal(transportationItems[0].maximumDuration, 30);
      assert.equal(transportationItems[1].startMinutes, 624);
      assert.equal(transportationItems[1].maximumDuration, 55);
      assert.match(
         allTextFor(transportationItems[0].row),
         /Main Zoomobile Station → Africa Zoomobile Station/
      );
      assert.match(
         allTextFor(transportationItems[1].row),
         /Canadian Domain Zoomobile Station → Main Zoomobile Station/
      );
   });
});

test('Test_BuildScheduledItemRowsContext_TestDeletedWildEncounters_ExpectOmitted', () => {
   const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
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

test('Test_BuildScheduledItemRowsContext_TestDeletedGuardiansTalks_ExpectOmitted', () => {
   const context = DayPlannerScheduledItems.buildScheduledItemRowsContext(
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
