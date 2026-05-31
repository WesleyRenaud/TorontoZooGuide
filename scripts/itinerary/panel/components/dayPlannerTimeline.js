import {
   appendScheduledDurationPill,
   resolveScheduledPillOptions,
} from './dayPlannerTimelinePills.js';
import { el } from '../dom.js';

export function makeTimelineRow(timeLabel) {
   const gridLine = el('div', 'itinerary-day-grid-line');

   return [
      el('div', 'itinerary-day-time', timeLabel),
      gridLine,
   ];
}

export function makeUnavailableMessage(message) {
   return el('div', 'itinerary-day-unavailable', message);
}

export function appendScheduledItems(
   gridLine,
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {}
) {
   scheduledItems.forEach((scheduledItem) => {
      appendScheduledDurationPill(gridLine, {
         label: scheduledItem.label,
         offsetFraction: scheduledItem.offsetFraction,
         durationMinutes: scheduledItem.maximumDuration,
         ...resolveScheduledPillOptions(
            scheduledItem,
            scheduleHandlers,
            strings
         ),
      });
   });
}

export {
   computeSpanHorizontalOffsetIndex,
   computeTimelineHorizontalOffsetIndex,
} from './dayPlannerTimelinePills.js';
