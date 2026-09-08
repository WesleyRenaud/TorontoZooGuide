import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduledPillOptions } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { DayPlannerScheduledPillOptionsBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptionsBuilder.js';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';

test('Test_ResolveScheduledPillOptions_TestEmptyMenu_ExpectEmptyObject', () => {
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;
   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => [];
   try {
      assert.deepEqual(
         DayPlannerScheduledPillOptions.resolveScheduledPillOptions({}, {}, { scheduledItemMenuAria: 'Menu' }),
         {}
      );
   } finally {
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});

test('Test_ResolveScheduledPillOptions_TestMenuItems_ExpectAriaAndItems', () => {
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;
   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => [{ label: 'Remove' }];
   try {
      assert.deepEqual(
         DayPlannerScheduledPillOptions.resolveScheduledPillOptions({}, {}, { scheduledItemMenuAria: 'Menu' }),
         {
            menuAriaLabel: 'Menu',
            menuItems: [{ label: 'Remove' }],
         }
      );
   } finally {
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});

test('Test_BuildGroupedScheduledPillItems_TestItems_ExpectMappedGroup', () => {
   const originalFlatten = DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup;
   const originalSort = ScheduledPillChecker.sortScheduledItemsForGroupDisplay;
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;

   DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup = (items) => items;
   ScheduledPillChecker.sortScheduledItemsForGroupDisplay = (items) => items;
   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => [{ label: 'Unschedule' }];

   try {
      const groupItems = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems(
         [{
            label: 'Lion',
            item: { start_time: '10:00', end_time: '11:00' },
         }],
         {},
         {},
         () => () => 'clicked'
      );

      assert.equal(groupItems.length, 1);
      assert.equal(groupItems[0].label, 'Lion');
      assert.equal(groupItems[0].startTime, '10:00');
      assert.equal(groupItems[0].endTime, '11:00');
      assert.equal(groupItems[0].onLabelClick(), 'clicked');
      assert.deepEqual(groupItems[0].menuItems, [{ label: 'Unschedule' }]);
   } finally {
      DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup = originalFlatten;
      ScheduledPillChecker.sortScheduledItemsForGroupDisplay = originalSort;
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});

test('Test_ResolveGroupedScheduledPillOptions_TestSparseGroup_ExpectEmpty', () => {
   const originalBuildGrouped = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems;
   const originalMerge = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems;

   DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = () => [{ label: 'Only' }];
   DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = () => [];

   try {
      assert.deepEqual(
         DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions([], {}, {}),
         {}
      );
   } finally {
      DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = originalBuildGrouped;
      DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = originalMerge;
   }
});

test('Test_ResolveGroupedScheduledPillOptions_TestMenusOrMany_ExpectOptions', () => {
   const originalBuildGrouped = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems;
   const originalMerge = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems;

   DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = () => [
      { label: 'A' },
      { label: 'B' },
   ];
   DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = () => [{ label: 'Remove' }];

   try {
      assert.deepEqual(
         DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
            [],
            {},
            { scheduledItemMenuAria: 'Group menu' }
         ),
         {
            menuAriaLabel: 'Group menu',
            menuItems: [{ label: 'Remove' }],
            groupItems: [{ label: 'A' }, { label: 'B' }],
         }
      );
   } finally {
      DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = originalBuildGrouped;
      DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = originalMerge;
   }
});
