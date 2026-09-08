import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduledPillOptionsBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptionsBuilder.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_FlattenScheduledItemsForPillGroup_TestClusters_ExpectFlat', () => {
   assert.deepEqual(
      DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup([
         { id: 1, clusterItems: [{ id: 'a' }, { id: 'b' }] },
         { id: 2 },
      ]),
      [{ id: 'a' }, { id: 'b' }, { id: 2 }]
   );
});

test('Test_BuildScheduledPillMenuItems_TestUnscheduleAndRemove_ExpectActions', () => {
   const unschedules = [];
   const removes = [];
   const menuItems = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
      {
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
         scheduleItemKey: 'lion||savanna',
         item: { species: 'African Lion' },
      },
      {
         onUnscheduleItineraryItem: (args) => { unschedules.push(args); },
         onRemoveItineraryItem: (args) => { removes.push(args); },
      },
      { unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(menuItems.length, 2);
   assert.equal(menuItems[0].label, 'Unschedule');
   assert.equal(menuItems[1].label, 'Remove');
   menuItems[0].onAction();
   menuItems[1].onAction();
   assert.deepEqual(unschedules, [{ itemType: ScheduleItemKind.ANIMAL.itemType, key: 'lion||savanna' }]);
   assert.deepEqual(removes, [{ itemType: ScheduleItemKind.ANIMAL.itemType, key: 'lion||savanna' }]);
});

test('Test_BuildScheduledPillMenuItems_TestEvent_ExpectEventRemove', () => {
   const removes = [];
   const menuItems = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
      {
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: 'arrival',
         scheduleItemKey: '',
         item: {},
      },
      {
         onRemoveItineraryItem: (args) => { removes.push(args); },
      },
      { remove: 'Remove' }
   );

   assert.equal(menuItems.length, 1);
   menuItems[0].onAction();
   assert.deepEqual(removes, [{ itemType: 'arrival', key: '' }]);
});

test('Test_MergeScheduledPillMenuItems_TestGroup_ExpectCombined', () => {
   const menuItems = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems(
      [{
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
         scheduleItemKey: 'carousel',
         item: { name: 'Carousel' },
      }],
      {
         onRemoveItineraryItem: () => {},
      },
      { remove: 'Remove', unschedule: 'Unschedule' }
   );

   assert.ok(menuItems.some((item) => item.label === 'Remove'));
});
