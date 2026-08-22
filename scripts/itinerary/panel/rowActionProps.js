import {
   getItineraryItemKey,
   tagScheduleItemRow,
} from './scheduleItemSearch.js';
import { isTransportationAddedAsAttraction } from '../selectors/transportationSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

export function hasItineraryScheduleTimes(item) {
   return Boolean(item.start_time && item.end_time);
}

export function canShowItineraryItemScheduleAction(itemType, item) {
   if (itemType !== ScheduleItemKind.TRANSPORTATION.itemType) {
      return true;
   }

   return isTransportationAddedAsAttraction(item);
}

export function buildScheduleRowProps(itemType, item, onScheduleItem) {
   if (typeof onScheduleItem !== 'function') {
      return {};
   }

   if (hasItineraryScheduleTimes(item)) {
      return {};
   }

   if (!canShowItineraryItemScheduleAction(itemType, item)) {
      return {};
   }

   const row = tagScheduleItemRow(itemType, item);

   if (!row) {
      return {};
   }

   const actionLabel = APP_STRINGS.itinerary.scheduleItem.scheduleButton;

   return {
      actionLabel,
      onAction: () => onScheduleItem({
         itemType,
         row,
      }),
   };
}

export function buildUnscheduleRowProps(itemType, item, onUnscheduleItem) {
   if (typeof onUnscheduleItem !== 'function') {
      return {};
   }

   if (!hasItineraryScheduleTimes(item)) {
      return {};
   }

   const key = getItineraryItemKey(itemType, item);

   if (!key) {
      return {};
   }

   const actionLabel = APP_STRINGS.itinerary.dayPlanner.unschedule;

   return {
      actionLabel,
      onAction: () => onUnscheduleItem({
         itemType,
         key,
      }),
   };
}

export function buildRemoveRowProps(
   itemType,
   item,
   onRemoveItem,
   { useSecondaryAction = true } = {}
) {
   if (typeof onRemoveItem !== 'function') {
      return {};
   }

   const key = getItineraryItemKey(itemType, item);

   if (!key) {
      return {};
   }

   const removeLabel = APP_STRINGS.itinerary.dayPlanner.remove;
   const onRemove = () => onRemoveItem({
      itemType,
      key,
   });

   if (useSecondaryAction) {
      return {
         secondaryActionLabel: removeLabel,
         onSecondaryAction: onRemove,
      };
   }

   return {
      actionLabel: removeLabel,
      onAction: onRemove,
   };
}

export function buildRowScheduleActionProps(itemType, item, handlers = {}) {
   const { onUnscheduleItem = null, onScheduleItem = null, onRemoveItem = null } = handlers;
   const scheduleActionProps = {
      ...buildUnscheduleRowProps(itemType, item, onUnscheduleItem),
      ...buildScheduleRowProps(itemType, item, onScheduleItem),
   };

   return {
      ...scheduleActionProps,
      ...buildRemoveRowProps(itemType, item, onRemoveItem, {
         useSecondaryAction: Boolean(scheduleActionProps.actionLabel),
      }),
   };
}
