import { DayPlannerScheduledPillOptionsBuilder } from './dayPlannerScheduledPillOptionsBuilder.js';
import { ScheduledPillOverlap } from './scheduledPillOverlap.js';

export class DayPlannerScheduledPillOptions {
   static resolveScheduledPillOptions(
      scheduledItem = {},
      scheduleHandlers = {},
      strings = {}
   ) {
      const menuItems = DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
         scheduledItem,
         scheduleHandlers,
         strings
      );

      if (!menuItems.length) {
         return {};
      }

      return {
         menuAriaLabel: strings.scheduledItemMenuAria,
         menuItems,
      };
   }

   static buildGroupedScheduledPillItems(
      scheduledItems = [],
      scheduleHandlers = {},
      strings = {},
      resolveItemLabelClick = () => null
   ) {
      return ScheduledPillOverlap.sortScheduledItemsForGroupDisplay(
         DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup(scheduledItems)
      ).map((scheduledItem) => ({
         label: scheduledItem.label,
         item: scheduledItem.item,
         startTime: scheduledItem.item?.start_time ?? '',
         endTime: scheduledItem.item?.end_time ?? '',
         onLabelClick: resolveItemLabelClick(scheduledItem),
         menuItems: DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(
            scheduledItem,
            scheduleHandlers,
            strings
         ),
      }));
   }

   static resolveGroupedScheduledPillOptions(
      scheduledItems = [],
      scheduleHandlers = {},
      strings = {},
      resolveItemLabelClick = () => null
   ) {
      const groupItems = DayPlannerScheduledPillOptions.buildGroupedScheduledPillItems(
         scheduledItems,
         scheduleHandlers,
         strings,
         resolveItemLabelClick
      );
      const menuItems = DayPlannerScheduledPillOptionsBuilder.mergeScheduledPillMenuItems(
         scheduledItems,
         scheduleHandlers,
         strings
      );

      if (!menuItems.length && groupItems.length <= 1) {
         return {};
      }

      return {
         menuAriaLabel: strings.scheduledItemMenuAria,
         menuItems,
         groupItems,
      };
   }
}
