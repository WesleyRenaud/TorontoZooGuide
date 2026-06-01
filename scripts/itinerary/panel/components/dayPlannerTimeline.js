import {
   appendScheduledDurationPill,
   resolveScheduledPillOptions,
} from './dayPlannerTimelinePills.js';
import { el } from '../dom.js';
import { openAnimalSpeciesOverlay } from '../../../overlays/speciesOverlay.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import {
   isScheduleItemModuleItemType,
   ScheduleItemKind,
} from '../../../shared/enums/scheduleItemKind.js';

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

function makeScheduledItemBlock(itemRow, maximumDuration, offsetFraction = 0) {
   const block = el('div', 'itinerary-day-event');
   const slotSpan = maximumDuration / TIMELINE_SLOT_MINUTES;

   block.style.setProperty('--itinerary-event-slot-span', String(slotSpan));

   if (offsetFraction > 0) {
      block.setAttribute('data-offset-fraction', String(offsetFraction));
      block.style.setProperty(
         '--itinerary-event-offset-fraction',
         String(offsetFraction)
      );
   }

   itemRow.classList.add('itinerary-day-event-card');
   block.appendChild(itemRow);

   return block;
}

function usesScheduledTimelineEventBlock(scheduledItem) {
   return Boolean(
      scheduledItem.row
      && !isScheduleItemModuleItemType(scheduledItem.scheduleItemKind)
   );
}

export function appendScheduledItems(
   gridLine,
   scheduledItems = [],
   scheduleHandlers = {},
   strings = {}
) {
   scheduledItems.forEach((scheduledItem) => {
      if (usesScheduledTimelineEventBlock(scheduledItem)) {
         gridLine.appendChild(
            makeScheduledItemBlock(
               scheduledItem.row,
               scheduledItem.maximumDuration,
               scheduledItem.offsetFraction
            )
         );
         return;
      }

      appendScheduledDurationPill(gridLine, {
         label: scheduledItem.label,
         offsetFraction: scheduledItem.offsetFraction,
         durationMinutes: scheduledItem.maximumDuration,
         startTime: scheduledItem.item.start_time,
         endTime: scheduledItem.item.end_time,
         onLabelClick: scheduledItem.scheduleItemKind === ScheduleItemKind.ANIMAL.itemType
            ? () => openAnimalSpeciesOverlay(scheduledItem.item)
            : null,
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
