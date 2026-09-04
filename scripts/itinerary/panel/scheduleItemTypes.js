import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ScheduleItemEventLabels } from './scheduleItemEventLabels.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

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
         label: ScheduleItemEventLabels.formatItineraryEventTypeLabel(eventType),
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
            label: APP_STRINGS.entityLabels.animal,
         },
         {
            value: ScheduleItemKind.ATTRACTION.itemType,
            label: APP_STRINGS.entityLabels.attraction,
         },
         {
            value: ScheduleItemKind.TRANSPORTATION.itemType,
            label: APP_STRINGS.entityLabels.transportation,
         },
         {
            value: ScheduleItemKind.GUARDIANS_TALK.itemType,
            label: APP_STRINGS.entityLabels.guardiansTalk,
         },
         {
            value: ScheduleItemKind.WILD_ENCOUNTER.itemType,
            label: APP_STRINGS.entityLabels.wildEncounter,
         },
      ];
   }
}
