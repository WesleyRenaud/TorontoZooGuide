import { DayPlannerScheduledPillOptions } from './dayPlannerScheduledPillOptions.js';
import { DayPlannerTimelinePillAppend } from './dayPlannerTimelinePillAppend.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ItineraryPillMenu } from './itineraryPillMenu.js';
import { SpeciesOverlay } from '../../../overlays/speciesOverlay.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { RegionColors } from '../../../shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimeline {
   static attachScheduledEventCardMenu(itemRow, {
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

   static makeScheduledItemBlock(
      itemRow,
      maximumDuration,
      offsetFraction = 0,
      menuOptions = {},
      item = null
   ) {
      const block = ItineraryPanelDom.el('div', 'itinerary-day-event');
      const slotSpan = maximumDuration / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

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
      DayPlannerTimeline.attachScheduledEventCardMenu(itemRow, menuOptions);
      block.appendChild(itemRow);

      return block;
   }

   static usesScheduledTimelineEventBlock(scheduledItem) {
      return Boolean(
         scheduledItem.row
         && ScheduleItemKind.usesScheduledTimelineEventCard(scheduledItem.scheduleItemKind)
      );
   }

   static getRenderGroupPrimaryScheduledItem(renderGroup = {}) {
      return renderGroup.items?.[0] ?? null;
   }

   static resolveRenderGroupLabel(renderGroup = {}) {
      if (renderGroup.label) {
         return renderGroup.label;
      }

      return DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup)?.label ?? '';
   }

   static resolveRenderGroupStartTime(renderGroup = {}) {
      return DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup)?.item?.start_time ?? '';
   }

   static resolveRenderGroupEndTime(renderGroup = {}) {
      if (renderGroup.items?.length === 1) {
         return renderGroup.items[0]?.item?.end_time ?? '';
      }

      const endTimes = (renderGroup.items ?? [])
         .map((scheduledItem) => scheduledItem.item?.end_time)
         .filter(Boolean);

      return endTimes[endTimes.length - 1] ?? '';
   }

   static resolveScheduledItemLabelClick(scheduledItem = {}) {
      if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
         return null;
      }

      return () => SpeciesOverlay.openAnimalSpeciesOverlay(scheduledItem.item);
   }

   static resolveRenderGroupLabelClick(renderGroup = {}) {
      if (renderGroup.items?.length !== 1) {
         return null;
      }

      const scheduledItem = DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup);

      if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
         return null;
      }

      return () => SpeciesOverlay.openAnimalSpeciesOverlay(scheduledItem.item);
   }

   static resolveRenderGroupItem(renderGroup = {}) {
      return DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup)?.item ?? null;
   }

   static resolveRenderGroupPillOptions(
      renderGroup = {},
      scheduleHandlers = {},
      strings = {}
   ) {
      if ((renderGroup.items ?? []).length === 1) {
         return DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
            DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup),
            scheduleHandlers,
            strings
         );
      }

      return DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
         renderGroup.items,
         scheduleHandlers,
         strings,
         DayPlannerTimeline.resolveScheduledItemLabelClick
      );
   }

   static timelineSlotRowHeightFraction(slotSpanMinutes) {
      const span = Number.isFinite(slotSpanMinutes) && slotSpanMinutes > 0
         ? slotSpanMinutes
         : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

      return span / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   }

   static makeTimelineRow(
      timeLabel,
      slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   ) {
      const timeCell = ItineraryPanelDom.el('div', 'itinerary-day-time');

      timeCell.appendChild(ItineraryPanelDom.el('span', 'itinerary-day-time-label', timeLabel));

      const gridLine = ItineraryPanelDom.el('div', 'itinerary-day-grid-line');
      const heightFraction = DayPlannerTimeline.timelineSlotRowHeightFraction(slotSpanMinutes);

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

   static appendTimelineBoundaryLabel(timeCell, label) {
      if (!timeCell || !label) {
         return;
      }

      timeCell.appendChild(ItineraryPanelDom.el('span', 'itinerary-day-time-boundary-label', label));

   }

   static makeUnavailableMessage(message) {
      return ItineraryPanelDom.el('div', 'itinerary-day-unavailable', message);

   }

   static appendScheduledItems(
      gridLine,
      scheduledRenderGroups = [],
      scheduleHandlers = {},
      strings = {}
   ) {
      (scheduledRenderGroups ?? []).forEach((renderGroup) => {
         const scheduledItem = DayPlannerTimeline.getRenderGroupPrimaryScheduledItem(renderGroup);

         if (scheduledItem && DayPlannerTimeline.usesScheduledTimelineEventBlock(scheduledItem)) {
            gridLine.appendChild(
               DayPlannerTimeline.makeScheduledItemBlock(
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
            label: DayPlannerTimeline.resolveRenderGroupLabel(renderGroup),
            offsetFraction: renderGroup.offsetFraction,
            durationMinutes: renderGroup.durationMinutes,
            displayDurationMinutes: renderGroup.displayDurationMinutes,
            slotSpanMinutes: renderGroup.slotSpanMinutes,
            startTime: DayPlannerTimeline.resolveRenderGroupStartTime(renderGroup),
            endTime: DayPlannerTimeline.resolveRenderGroupEndTime(renderGroup),
            onLabelClick: DayPlannerTimeline.resolveRenderGroupLabelClick(renderGroup),
            item: DayPlannerTimeline.resolveRenderGroupItem(renderGroup),
            ...DayPlannerTimeline.resolveRenderGroupPillOptions(
               renderGroup,
               scheduleHandlers,
               strings
            ),
         });
      });
   }
}
