import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduledPillOptions } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { DayPlannerScheduledPillOptionsBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptionsBuilder.js';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_ResolveScheduledPillOptions_TestEmptyMenu_ExpectEmptyObject', () => {
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;
   const strings = { scheduledItemMenuAria: 'Menu' };

   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => [];

   try {
      const options = DayPlannerScheduledPillOptions.resolveScheduledPillOptions({}, {}, strings);

      assert.deepEqual(options, {});
   } finally {
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});


test('Test_ResolveScheduledPillOptions_TestMenuItems_ExpectAriaAndItems', () => {
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;
   const menuItems = [{ label: 'Remove' }];
   const menuAriaLabel = 'Menu';
   const strings = { scheduledItemMenuAria: menuAriaLabel };

   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => menuItems;

   try {
      const options = DayPlannerScheduledPillOptions.resolveScheduledPillOptions({}, {}, strings);

      assert.deepEqual(options, {
         menuAriaLabel,
         menuItems,
      });
   } finally {
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});


test('Test_BuildGroupedScheduledPillItems_TestItems_ExpectMappedGroup', () => {
   const originalFlatten = DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup;
   const originalSort = ScheduledPillChecker.sortScheduledItemsForGroupDisplay;
   const originalBuild = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems;
   const species = 'African Lion';
   const startTime = '10:00';
   const endTime = '11:00';
   const menuItems = [{ label: 'Unschedule' }];
   const clickResult = 'clicked';
   const items = [{
      label: species,
      item: { start_time: startTime, end_time: endTime },
   }];

   DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup = (grouped) => grouped;
   ScheduledPillChecker.sortScheduledItemsForGroupDisplay = (grouped) => grouped;
   DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = () => menuItems;

   try {
      const groupItems = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems(
         items,
         {},
         {},
         () => () => clickResult
      );
      const firstItem = groupItems.at(Position.FIRST);

      assert.equal(groupItems.length, items.length);
      assert.equal(firstItem.label, species);
      assert.equal(firstItem.startTime, startTime);
      assert.equal(firstItem.endTime, endTime);
      assert.equal(firstItem.onLabelClick(), clickResult);
      assert.deepEqual(firstItem.menuItems, menuItems);
   } finally {
      DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup = originalFlatten;
      ScheduledPillChecker.sortScheduledItemsForGroupDisplay = originalSort;
      DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems = originalBuild;
   }
});


test('Test_ResolveGroupedScheduledPillOptions_TestSparseGroup_ExpectEmpty', () => {
   const originalBuildGrouped = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems;
   const originalMerge = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems;

   DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = () => [{ label: 'African Lion' }];
   DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = () => [];

   try {
      const options = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions([], {}, {});

      assert.deepEqual(options, {});
   } finally {
      DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = originalBuildGrouped;
      DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = originalMerge;
   }
});


test('Test_ResolveGroupedScheduledPillOptions_TestMenusOrMany_ExpectOptions', () => {
   const originalBuildGrouped = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems;
   const originalMerge = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems;
   const groupItems = [
      { label: 'African Lion' },
      { label: 'Amur Tiger' },
   ];
   const menuItems = [{ label: 'Remove' }];
   const menuAriaLabel = 'Group menu';

   DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = () => groupItems;
   DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = () => menuItems;

   try {
      const options = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
         [],
         {},
         { scheduledItemMenuAria: menuAriaLabel }
      );

      assert.deepEqual(options, {
         menuAriaLabel,
         menuItems,
         groupItems,
      });
   } finally {
      DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems = originalBuildGrouped;
      DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems = originalMerge;
   }
});
