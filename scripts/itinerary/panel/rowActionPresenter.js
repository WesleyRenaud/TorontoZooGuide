import { ScheduleItemSearcher } from './scheduleItemSearcher.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class RowActionPresenter {
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

      if (RowActionPresenter.hasItineraryScheduleTimes(item)) {
         return {};
      }

      if (!RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item)) {
         return {};
      }

      const row = ScheduleItemSearcher.tagScheduleItemRow(itemType, item);

      if (!row) {
         return {};
      }

      return {
         actionLabel: Strings.itinerary.scheduleItem.scheduleButton,
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

      if (!RowActionPresenter.hasItineraryScheduleTimes(item)) {
         return {};
      }

      if (!RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item)) {
         return {};
      }

      const key = ScheduleItemSearcher.getItineraryItemKey(itemType, item);

      if (!key) {
         return {};
      }

      return {
         actionLabel: Strings.itinerary.dayPlanner.unschedule,
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

      const key = ScheduleItemSearcher.getItineraryItemKey(itemType, item);

      if (!key) {
         return {};
      }

      const onRemove = () => onRemoveItem({
         itemType,
         key,
      });

      if (useSecondaryAction) {
         return {
            secondaryActionLabel: Strings.itinerary.dayPlanner.remove,
            onSecondaryAction: onRemove,
         };
      }

      return {
         actionLabel: Strings.itinerary.dayPlanner.remove,
         onAction: onRemove,
      };
   }

   static buildRowScheduleActionProps(itemType, item, handlers = {}) {
      const { onUnscheduleItem = null, onScheduleItem = null, onRemoveItem = null } = handlers;
      const scheduleActionProps = {
         ...RowActionPresenter.buildUnscheduleRowProps(itemType, item, onUnscheduleItem),
         ...RowActionPresenter.buildScheduleRowProps(itemType, item, onScheduleItem),
      };

      return {
         ...scheduleActionProps,
         ...RowActionPresenter.buildRemoveRowProps(itemType, item, onRemoveItem, {
            useSecondaryAction: Boolean(scheduleActionProps.actionLabel),
         }),
      };
   }
}
