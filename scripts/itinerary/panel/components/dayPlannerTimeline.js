import {
   appendScheduledDurationPill,
   resolveGroupedScheduledPillOptions,
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

function resolveRenderGroupLabel(renderGroup = {}) {
   if (renderGroup.label) {
      return renderGroup.label;
   }

   return renderGroup.items?.[0]?.label ?? '';
}

function resolveRenderGroupStartTime(renderGroup = {}) {
   return renderGroup.items?.[0]?.item?.start_time ?? '';
}

function resolveRenderGroupEndTime(renderGroup = {}) {
   if (renderGroup.items?.length === 1) {
      return renderGroup.items[0]?.item?.end_time ?? '';
   }

   const endTimes = (renderGroup.items ?? [])
      .map((scheduledItem) => scheduledItem.item?.end_time)
      .filter(Boolean);

   return endTimes[endTimes.length - 1] ?? '';
}

function resolveRenderGroupLabelClick(renderGroup = {}) {
   if (renderGroup.items?.length !== 1) {
      return null;
   }

   const scheduledItem = renderGroup.items[0];

   if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
      return null;
   }

   return () => openAnimalSpeciesOverlay(scheduledItem.item);
}

function resolveRenderGroupPillOptions(
   renderGroup = {},
   scheduleHandlers = {},
   strings = {}
) {
   if ((renderGroup.items ?? []).length === 1) {
      return resolveScheduledPillOptions(
         renderGroup.items[0],
         scheduleHandlers,
         strings
      );
   }

   return resolveGroupedScheduledPillOptions(
      renderGroup.items,
      scheduleHandlers,
      strings
   );
}

export function appendScheduledItems(
   gridLine,
   scheduledRenderGroups = [],
   scheduleHandlers = {},
   strings = {}
) {
   (scheduledRenderGroups ?? []).forEach((renderGroup) => {
      const scheduledItem = renderGroup.items?.[0];

      if (scheduledItem && usesScheduledTimelineEventBlock(scheduledItem)) {
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
         label: resolveRenderGroupLabel(renderGroup),
         offsetFraction: renderGroup.offsetFraction,
         durationMinutes: renderGroup.durationMinutes,
         startTime: resolveRenderGroupStartTime(renderGroup),
         endTime: resolveRenderGroupEndTime(renderGroup),
         horizontalOffsetIndex: renderGroup.horizontalOffsetIndex,
         visualStartMinutes: renderGroup.visualStartMinutes,
         visualEndMinutes: renderGroup.visualEndMinutes,
         onLabelClick: resolveRenderGroupLabelClick(renderGroup),
         ...resolveRenderGroupPillOptions(
            renderGroup,
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
