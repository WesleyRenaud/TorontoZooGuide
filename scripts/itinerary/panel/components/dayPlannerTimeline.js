import { DayPlannerScheduledPillOptions } from './dayPlannerScheduledPillOptions.js';
import { DayPlannerTimelinePillAppend } from './dayPlannerTimelinePillAppend.js';
import { el } from '../dom.js';
import { ItineraryPillMenu } from './itineraryPillMenu.js';
import { openAnimalSpeciesOverlay } from '../../../overlays/speciesOverlay.js';
import { Constants } from '../../../shared/constants.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { RegionColors } from '../../../shared/regionColors.js';

export function timelineSlotRowHeightFraction(slotSpanMinutes) {
   const span = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
      ? slotSpanMinutes
      : Constants.TIMELINE_SLOT_MINUTES;

   return span / Constants.TIMELINE_SLOT_MINUTES;
}

export function makeTimelineRow(
   timeLabel,
   slotSpanMinutes = Constants.TIMELINE_SLOT_MINUTES
) {
   const timeCell = el('div', 'itinerary-day-time');

   timeCell.appendChild(el('span', 'itinerary-day-time-label', timeLabel));

   const gridLine = el('div', 'itinerary-day-grid-line');
   const heightFraction = timelineSlotRowHeightFraction(slotSpanMinutes);

   timeCell.style.setProperty(
      '--itinerary-slot-row-height-fraction',
      String(heightFraction)
   );
   gridLine.style.setProperty(
      '--itinerary-slot-row-height-fraction',
      String(heightFraction)
   );

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

function attachScheduledEventCardMenu(itemRow, {
   menuAriaLabel = '',
   menuItems = [],
} = {}) {
   if (!itemRow || !menuItems.length) {
      return;
   }

   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes(
      menuAriaLabel,
      menuItems
   );

   itemRow.classList.add('itinerary-day-event-card--with-menu');
   itemRow.appendChild(menu);
   ItineraryPillMenu.bindPillMenu(itemRow, {
      menuButton,
      menuPanel,
      menuItems,
      menuOpenClass: 'itinerary-day-event-card--menu-open',
   });
}

function makeScheduledItemBlock(
   itemRow,
   maximumDuration,
   offsetFraction = 0,
   menuOptions = {},
   item = null
) {
   const block = el('div', 'itinerary-day-event');
   const slotSpan = maximumDuration / Constants.TIMELINE_SLOT_MINUTES;

   block.style.setProperty('--itinerary-event-slot-span', String(slotSpan));

   if (offsetFraction > 0) {
      block.setAttribute('data-offset-fraction', String(offsetFraction));
      block.style.setProperty(
         '--itinerary-event-offset-fraction',
         String(offsetFraction)
      );
   }

   itemRow.classList.add('itinerary-day-event-card');
   RegionColors.applyRegionColorsToElement(
      itemRow,
      RegionColors.resolveRegionColorSlugForScheduledItem(item)
   );
   attachScheduledEventCardMenu(itemRow, menuOptions);
   block.appendChild(itemRow);

   return block;
}

function usesScheduledTimelineEventBlock(scheduledItem) {
   return Boolean(
      scheduledItem.row
      && ScheduleItemKind.usesScheduledTimelineEventCard(scheduledItem.scheduleItemKind)
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
      return DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
         getRenderGroupPrimaryScheduledItem(renderGroup),
         scheduleHandlers,
         strings
      );
   }

   return DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
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
               scheduledItem.offsetFraction,
               DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
                  scheduledItem,
                  scheduleHandlers,
                  strings
               ),
               scheduledItem.item
            )
         );
         return;
      }

      DayPlannerTimelinePillAppend.appendScheduledDurationPill(gridLine, {
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
   DayPlannerTimelinePillPlacement,
} from './dayPlannerTimelinePillPlacement.js';
