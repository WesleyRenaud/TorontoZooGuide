import { ScheduleItemSearch } from './scheduleItemSearch.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class RowActionProps {
   static hasItineraryScheduleTimes(item) {
      return Boolean(item.start_time && item.end_time);
   }

   static canShowItineraryItemScheduleControls(itemType, item) {
      if (itemType !== ScheduleItemKind.TRANSPORTATION.itemType) {
         return true;
      }

      return TransportationSelectorModel.isTransportationAddedAsAttraction(item);
   }

   static buildScheduleRowProps(itemType, item, onScheduleItem) {
      if (typeof onScheduleItem !== 'function') {
         return {};
      }

      if (RowActionProps.hasItineraryScheduleTimes(item)) {
         return {};
      }

      if (!RowActionProps.canShowItineraryItemScheduleControls(itemType, item)) {
         return {};
      }

      const row = ScheduleItemSearch.tagScheduleItemRow(itemType, item);

      if (!row) {
         return {};
      }

      const actionLabel = Strings.itinerary.scheduleItem.scheduleButton;

      return {
         actionLabel,
         onAction: () => onScheduleItem({
            itemType,
            row,
         }),
      };
   }

   static buildUnscheduleRowProps(itemType, item, onUnscheduleItem) {
      if (typeof onUnscheduleItem !== 'function') {
         return {};
      }

      if (!RowActionProps.hasItineraryScheduleTimes(item)) {
         return {};
      }

      if (!RowActionProps.canShowItineraryItemScheduleControls(itemType, item)) {
         return {};
      }

      const key = ScheduleItemSearch.getItineraryItemKey(itemType, item);

      if (!key) {
         return {};
      }

      const actionLabel = Strings.itinerary.dayPlanner.unschedule;

      return {
         actionLabel,
         onAction: () => onUnscheduleItem({
            itemType,
            key,
         }),
      };
   }

   static buildRemoveRowProps(
      itemType,
      item,
      onRemoveItem,
      { useSecondaryAction = true } = {}
   ) {
      if (typeof onRemoveItem !== 'function') {
         return {};
      }

      const key = ScheduleItemSearch.getItineraryItemKey(itemType, item);

      if (!key) {
         return {};
      }

      const removeLabel = Strings.itinerary.dayPlanner.remove;
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

   static buildRowScheduleActionProps(itemType, item, handlers = {}) {
      const { onUnscheduleItem = null, onScheduleItem = null, onRemoveItem = null } = handlers;
      const scheduleActionProps = {
         ...RowActionProps.buildUnscheduleRowProps(itemType, item, onUnscheduleItem),
         ...RowActionProps.buildScheduleRowProps(itemType, item, onScheduleItem),
      };

      return {
         ...scheduleActionProps,
         ...RowActionProps.buildRemoveRowProps(itemType, item, onRemoveItem, {
            useSecondaryAction: Boolean(scheduleActionProps.actionLabel),
         }),
      };
   }
}
