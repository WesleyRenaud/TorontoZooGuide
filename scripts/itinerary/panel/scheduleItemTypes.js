import {
   buildSchedulableEventTypes,
   isScheduleItemEventType,
} from '../itineraryEventTypes.js';
import { formatItineraryEventTypeLabel } from './scheduleItemEventLabels.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../strings.js';

export { buildSchedulableEventTypes, isScheduleItemEventType };

export const SCHEDULE_ITEM_TYPE_PLACEHOLDER = '';

export function isScheduleItemTypeUnset(selection) {
   return selection === SCHEDULE_ITEM_TYPE_PLACEHOLDER;
}

export function isScheduleItemSearchEnabled(selection, eventTypes = []) {
   return !isScheduleItemEventType(selection, eventTypes);
}

export function buildScheduleItemTypeOptions(eventTypes = [], strings = {}) {
   const eventOptions = eventTypes.map((eventType) => ({
      value: eventType,
      label: formatItineraryEventTypeLabel(eventType),
   }));

   return [
      {
         value: SCHEDULE_ITEM_TYPE_PLACEHOLDER,
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
