import { sortScheduledItemsForGroupDisplay } from './scheduledPillOverlap.js';
import {
   isScheduleItemModuleItemType,
   ScheduleItemKind,
} from '../../../shared/enums/scheduleItemKind.js';

function flattenScheduledItemsForPillGroup(scheduledItems = []) {
   return scheduledItems.flatMap((scheduledItem) => (
      scheduledItem.clusterItems?.length
         ? scheduledItem.clusterItems
         : [scheduledItem]
   ));
}

function buildScheduledPillMenuItems(
   scheduledItem = {},
   scheduleHandlers = {},
   strings = {}
) {
   const {
      scheduleItemKind,
      scheduleItemKey,
      scheduleItemEventType,
   } = scheduledItem;
   const menuItems = [];

   if (
      typeof scheduleHandlers.onUnscheduleItineraryItem === 'function'
      && scheduleItemKind !== ScheduleItemKind.EVENT.kind
   ) {
      if (
         isScheduleItemModuleItemType(scheduleItemKind)
         && scheduleItemKey
      ) {
         menuItems.push({
            label: strings.unschedule,
            onAction: () => scheduleHandlers.onUnscheduleItineraryItem({
               itemType: scheduleItemKind,
               key: scheduleItemKey,
            }),
         });
      }
   }

   if (typeof scheduleHandlers.onRemoveItineraryItem === 'function') {
      if (
         scheduleItemKind === ScheduleItemKind.EVENT.kind
         && scheduleItemEventType
      ) {
         menuItems.push({
            label: strings.remove,
            onAction: () => scheduleHandlers.onRemoveItineraryItem({
               itemType: scheduleItemEventType,
               key: '',
            }),
         });
      }
      else if (scheduleItemKey) {
         menuItems.push({
            label: strings.remove,
            onAction: () => scheduleHandlers.onRemoveItineraryItem({
               itemType: scheduleItemKind,
               key: scheduleItemKey,
            }),
         });
      }
   }

   return menuItems;
}

function mergeScheduledPillMenuItems(items = [], scheduleHandlers = {}, strings = {}) {
   const menuItems = [];

   flattenScheduledItemsForPillGroup(items).forEach((scheduledItem) => {
      menuItems.push(
         ...buildScheduledPillMenuItems(scheduledItem, scheduleHandlers, strings)
      );
   });

   return menuItems;
}

export function resolveScheduledPillOptions(
   scheduledItem = {},
   scheduleHandlers = {},
   strings = {}
) {
   const menuItems = buildScheduledPillMenuItems(
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

export function buildGroupedScheduledPillItems(
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {},
   resolveItemLabelClick = () => null
) {
   return sortScheduledItemsForGroupDisplay(
      flattenScheduledItemsForPillGroup(scheduledItems)
   ).map((scheduledItem) => ({
      label: scheduledItem.label,
      item: scheduledItem.item,
      startTime: scheduledItem.item?.start_time ?? '',
      endTime: scheduledItem.item?.end_time ?? '',
      onLabelClick: resolveItemLabelClick(scheduledItem),
      menuItems: buildScheduledPillMenuItems(
         scheduledItem,
         scheduleHandlers,
         strings
      ),
   }));
}

export function resolveGroupedScheduledPillOptions(
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {},
   resolveItemLabelClick = () => null
) {
   const groupItems = buildGroupedScheduledPillItems(
      scheduledItems,
      scheduleHandlers,
      strings,
      resolveItemLabelClick
   );
   const menuItems = mergeScheduledPillMenuItems(
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
