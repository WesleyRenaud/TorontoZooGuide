import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ScheduleItemEventFormatter } from './scheduleItemEventFormatter.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class ScheduleItemTypes {
   static SCHEDULE_ITEM_TYPE_PLACEHOLDER = '';

   static isScheduleItemTypeUnset(selection) {
      return selection === ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER;
   }

   static isScheduleItemSearchEnabled(selection, eventTypes = []) {
      return !ItineraryEventTypes.isScheduleItemEventType(selection, eventTypes);
   }

   static buildScheduleItemTypeOptions(eventTypes = [], strings = {}) {
      const eventOptions = eventTypes.map((eventType) => ({
         value: eventType,
         label: ScheduleItemEventFormatter.formatItineraryEventTypeLabel(eventType),
      }));

      return [
         {
            value: ScheduleItemTypes.SCHEDULE_ITEM_TYPE_PLACEHOLDER,
            label: strings.typePlaceholder ?? '',
            selected: true,
         },
         ...eventOptions,
         {
            value: ScheduleItemKind.ANIMAL.itemType,
            label: Strings.entityLabels.animal,
         },
         {
            value: ScheduleItemKind.ATTRACTION.itemType,
            label: Strings.entityLabels.attraction,
         },
         {
            value: ScheduleItemKind.GUARDIANS_TALK.itemType,
            label: Strings.entityLabels.guardiansTalk,
         },
         {
            value: ScheduleItemKind.WILD_ENCOUNTER.itemType,
            label: Strings.entityLabels.wildEncounter,
         },
         {
            value: ScheduleItemKind.TRANSPORTATION.itemType,
            label: Strings.entityLabels.transportation,
         },
      ];
   }
}
