import { RowActionPresenter } from '../rowActionPresenter.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

export class DayPlannerScheduledPillOptionsBuilder {
   static flattenScheduledItemsForPillGroup(scheduledItems = []) {
      return scheduledItems.flatMap((scheduledItem) => (
         scheduledItem.clusterItems?.length
            ? scheduledItem.clusterItems
            : [scheduledItem]
      ));
   }

   static buildScheduledPillMenuItems(
      scheduledItem = {},
      scheduleHandlers = {},
      strings = {}
   ) {
      const {
         scheduleItemKind,
         scheduleItemKey,
         scheduleItemEventType,
         item,
      } = scheduledItem;
      const menuItems = [];

      if (
         typeof scheduleHandlers.onUnscheduleItineraryItem === 'function'
         && scheduleItemKind !== ScheduleItemKind.EVENT.kind
         && !ScheduleItemKind.isFixedTimeScheduleItemKind(scheduleItemKind)
         && RowActionPresenter.canShowItineraryItemScheduleControls(scheduleItemKind, item)
      ) {
         if (
            ScheduleItemKind.isScheduleItemModuleItemType(scheduleItemKind)
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

   static mergeScheduledPillMenuItems(items = [], scheduleHandlers = {}, strings = {}) {
      const menuItems = [];

      DayPlannerScheduledPillOptionsBuilder.flattenScheduledItemsForPillGroup(items).forEach((scheduledItem) => {
         menuItems.push(
            ...DayPlannerScheduledPillOptionsBuilder.buildScheduledPillMenuItems(scheduledItem, scheduleHandlers, strings)
         );
      });

      return menuItems;
   }
}
