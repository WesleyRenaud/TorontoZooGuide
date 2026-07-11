import {
   resolveGroupedScheduledPillOptions,
   resolveScheduledPillOptions,
} from './dayPlannerScheduledPillOptions.js';
import { appendScheduledDurationPill } from './dayPlannerTimelinePillAppend.js';
import { el } from '../dom.js';
import { openAnimalSpeciesOverlay } from '../../../overlays/speciesOverlay.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
import {
   ScheduleItemKind,
   usesScheduledTimelineEventCard,
} from '../../../shared/enums/scheduleItemKind.js';

export function makeTimelineRow(timeLabel) {
   const timeCell = el('div', 'itinerary-day-time');

   timeCell.appendChild(el('span', 'itinerary-day-time-label', timeLabel));

   const gridLine = el('div', 'itinerary-day-grid-line');

   return [
      timeCell,
      gridLine,
   ];
}

export function appendTimelineBoundaryLabel(timeCell, label) {
   if (!timeCell || !label) {
      return;
   }

   timeCell.appendChild(el('span', 'itinerary-day-time-boundary-label', label));
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
      && usesScheduledTimelineEventCard(scheduledItem.scheduleItemKind)
   );
}

function getRenderGroupPrimaryScheduledItem(renderGroup = {}) {
   return renderGroup.items?.[0] ?? null;
}

function resolveRenderGroupLabel(renderGroup = {}) {
   if (renderGroup.label) {
      return renderGroup.label;
   }

   return getRenderGroupPrimaryScheduledItem(renderGroup)?.label ?? '';
}

function resolveRenderGroupStartTime(renderGroup = {}) {
   return getRenderGroupPrimaryScheduledItem(renderGroup)?.item?.start_time ?? '';
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

function resolveScheduledItemLabelClick(scheduledItem = {}) {
   if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
      return null;
   }

   return () => openAnimalSpeciesOverlay(scheduledItem.item);
}

function resolveRenderGroupLabelClick(renderGroup = {}) {
   if (renderGroup.items?.length !== 1) {
      return null;
   }

   const scheduledItem = getRenderGroupPrimaryScheduledItem(renderGroup);

   if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
      return null;
   }

   return () => openAnimalSpeciesOverlay(scheduledItem.item);
}

function resolveRenderGroupItem(renderGroup = {}) {
   return getRenderGroupPrimaryScheduledItem(renderGroup)?.item ?? null;
}

function resolveRenderGroupPillOptions(
   renderGroup = {},
   scheduleHandlers = {},
   strings = {}
) {
   if ((renderGroup.items ?? []).length === 1) {
      return resolveScheduledPillOptions(
         getRenderGroupPrimaryScheduledItem(renderGroup),
         scheduleHandlers,
         strings
      );
   }

   return resolveGroupedScheduledPillOptions(
      renderGroup.items,
      scheduleHandlers,
      strings,
      resolveScheduledItemLabelClick
   );
}

export function appendScheduledItems(
   gridLine,
   scheduledRenderGroups = [],
   scheduleHandlers = {},
   strings = {}
) {
   (scheduledRenderGroups ?? []).forEach((renderGroup) => {
      const scheduledItem = getRenderGroupPrimaryScheduledItem(renderGroup);

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
         displayDurationMinutes: renderGroup.displayDurationMinutes,
         slotSpanMinutes: renderGroup.slotSpanMinutes,
         startTime: resolveRenderGroupStartTime(renderGroup),
         endTime: resolveRenderGroupEndTime(renderGroup),
         onLabelClick: resolveRenderGroupLabelClick(renderGroup),
         item: resolveRenderGroupItem(renderGroup),
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
} from './dayPlannerTimelinePillPlacement.js';
