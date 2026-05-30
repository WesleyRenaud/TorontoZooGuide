import { formatItineraryEventTypeLabel } from './scheduleItemEventLabels.js';
import { APP_STRINGS } from '../../strings.js';

export const SCHEDULE_ITEM_TYPE_PLACEHOLDER = '';

export const SCHEDULE_ITEM_MODULE_TYPES = Object.freeze({
   animals: 'animals',
   attractions: 'attractions',
});

export function isScheduleItemTypeUnset(selection) {
   return selection === SCHEDULE_ITEM_TYPE_PLACEHOLDER;
}

export function isScheduleItemSearchEnabled(selection, eventTypes = []) {
   return !isScheduleItemEventType(selection, eventTypes);
}

export function isScheduleItemEventType(selection, eventTypes = []) {
   return Array.isArray(eventTypes) && eventTypes.includes(selection);
}

export function buildSchedulableEventTypes(itineraryConfig = {}) {
   const excluded = new Set(['arrival', 'departure']);
   const eventTypes = Array.isArray(itineraryConfig?.eventTypes)
      ? itineraryConfig.eventTypes
      : [];

   return eventTypes.filter((eventType) => !excluded.has(eventType));
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
         value: SCHEDULE_ITEM_MODULE_TYPES.animals,
         label: APP_STRINGS.entityLabels.animal,
      },
      {
         value: SCHEDULE_ITEM_MODULE_TYPES.attractions,
         label: APP_STRINGS.entityLabels.attraction,
      },
   ];
}
