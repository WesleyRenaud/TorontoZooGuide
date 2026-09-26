import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduledPillOptionsBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptionsBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_FlattenScheduledItemsForPillGroup_TestClusters_ExpectFlat', () => {
   const lion = { id: 'african-lion' };
   const tiger = { id: 'amur-tiger' };
   const carousel = { id: 'conservation-carousel' };
   const items = [
      { id: 1, clusterItems: [lion, tiger] },
      carousel,
   ];

   const flattened = DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup(items);

   assert.deepEqual(flattened, [lion, tiger, carousel]);
});


test('Test_BuildScheduledPillMenuItems_TestUnscheduleAndRemove_ExpectActions', () => {
   const unscheduleLabel = 'Unschedule';
   const removeLabel = 'Remove';
   const scheduleItemKind = ScheduleItemKind.ANIMAL.itemType;
   const scheduleItemKey = 'lion||savanna';
   const unschedules = [];
   const removes = [];

   const menuItems = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
      {
         scheduleItemKind,
         scheduleItemKey,
         item: { species: 'African Lion' },
      },
      {
         onUnscheduleItineraryItem: (args) => { unschedules.push(args); },
         onRemoveItineraryItem: (args) => { removes.push(args); },
      },
      { unschedule: unscheduleLabel, remove: removeLabel }
   );
   menuItems.at(Position.FIRST).onAction();
   menuItems.at(Position.SECOND).onAction();

   assert.equal(menuItems.length, 2);
   assert.equal(menuItems.at(Position.FIRST).label, unscheduleLabel);
   assert.equal(menuItems.at(Position.SECOND).label, removeLabel);
   assert.deepEqual(unschedules, [{ itemType: scheduleItemKind, key: scheduleItemKey }]);
   assert.deepEqual(removes, [{ itemType: scheduleItemKind, key: scheduleItemKey }]);
});


test('Test_BuildScheduledPillMenuItems_TestEvent_ExpectEventRemove', () => {
   const removeLabel = 'Remove';
   const eventType = 'arrival';
   const scheduleItemKey = '';
   const removes = [];

   const menuItems = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
      {
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: eventType,
         scheduleItemKey,
         item: {},
      },
      {
         onRemoveItineraryItem: (args) => { removes.push(args); },
      },
      { remove: removeLabel }
   );
   menuItems.at(Position.FIRST).onAction();

   assert.equal(menuItems.length, 1);
   assert.deepEqual(removes, [{ itemType: eventType, key: scheduleItemKey }]);
});


test('Test_MergeScheduledPillMenuItems_TestGroup_ExpectCombined', () => {
   const removeLabel = 'Remove';

   const menuItems = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems(
      [{
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
         scheduleItemKey: 'carousel',
         item: { name: 'Conservation Carousel' },
      }],
      {
         onRemoveItineraryItem: () => {},
      },
      { remove: removeLabel, unschedule: 'Unschedule' }
   );

   assert.ok(menuItems.some((item) => item.label === removeLabel));
});
