import { DayPlannerScheduledPillOptions } from './dayPlannerScheduledPillOptions.js';
import { DayPlannerTimelinePillAppender } from './dayPlannerTimelinePillAppender.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPillView } from './itineraryPillView.js';
import { SpeciesFragment } from '../../../overlays/speciesFragment.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';
import { RegionColors } from '../../../shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerTimelineView {
   static attachScheduledEventCardMenu(itemRow, {
      menuAriaLabel = '',
      menuItems = [],
   } = {}) {
      if (!itemRow || !menuItems.length) {
         return;
      }

      const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes(
         menuAriaLabel,
         menuItems
      );

      itemRow.classList.add('itinerary-day-event-card--with-menu');
      itemRow.appendChild(menu);
      ItineraryPillView.bindPillMenu(itemRow, {
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
      const block = ItineraryPanelHelper.el('div', 'itinerary-day-event');
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
      DayPlannerTimelineView.attachScheduledEventCardMenu(itemRow, menuOptions);
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

      return DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup)?.label ?? '';
   }

   static resolveRenderGroupStartTime(renderGroup = {}) {
      return DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup)?.item?.start_time ?? '';
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

      return () => SpeciesFragment.openAnimalSpeciesOverlay(scheduledItem.item);
   }

   static resolveRenderGroupLabelClick(renderGroup = {}) {
      if (renderGroup.items?.length !== 1) {
         return null;
      }

      const scheduledItem = DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup);

      if (scheduledItem.scheduleItemKind !== ScheduleItemKind.ANIMAL.itemType) {
         return null;
      }

      return () => SpeciesFragment.openAnimalSpeciesOverlay(scheduledItem.item);
   }

   static resolveRenderGroupItem(renderGroup = {}) {
      return DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup)?.item ?? null;
   }

   static resolveRenderGroupPillOptions(
      renderGroup = {},
      scheduleHandlers = {},
      strings = {}
   ) {
      if ((renderGroup.items ?? []).length === 1) {
         return DayPlannerScheduledPillOptions.resolveScheduledPillOptions(
            DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup),
            scheduleHandlers,
            strings
         );
      }

      return DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions(
         renderGroup.items,
         scheduleHandlers,
         strings,
         DayPlannerTimelineView.resolveScheduledItemLabelClick
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
      const timeCell = ItineraryPanelHelper.el('div', 'itinerary-day-time');

      timeCell.appendChild(ItineraryPanelHelper.el('span', 'itinerary-day-time-label', timeLabel));

      const gridLine = ItineraryPanelHelper.el('div', 'itinerary-day-grid-line');
      const heightFraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

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

      timeCell.appendChild(ItineraryPanelHelper.el('span', 'itinerary-day-time-boundary-label', label));

   }

   static makeUnavailableMessage(message) {
      return ItineraryPanelHelper.el('div', 'itinerary-day-unavailable', message);

   }

   static appendScheduledItems(
      gridLine,
      scheduledRenderGroups = [],
      scheduleHandlers = {},
      strings = {}
   ) {
      (scheduledRenderGroups ?? []).forEach((renderGroup) => {
         const scheduledItem = DayPlannerTimelineView.getRenderGroupPrimaryScheduledItem(renderGroup);

         if (scheduledItem && DayPlannerTimelineView.usesScheduledTimelineEventBlock(scheduledItem)) {
            gridLine.appendChild(
               DayPlannerTimelineView.makeScheduledItemBlock(
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

         DayPlannerTimelinePillAppender.appendScheduledDurationPill(gridLine, {
            label: DayPlannerTimelineView.resolveRenderGroupLabel(renderGroup),
            offsetFraction: renderGroup.offsetFraction,
            durationMinutes: renderGroup.durationMinutes,
            displayDurationMinutes: renderGroup.displayDurationMinutes,
            slotSpanMinutes: renderGroup.slotSpanMinutes,
            startTime: DayPlannerTimelineView.resolveRenderGroupStartTime(renderGroup),
            endTime: DayPlannerTimelineView.resolveRenderGroupEndTime(renderGroup),
            onLabelClick: DayPlannerTimelineView.resolveRenderGroupLabelClick(renderGroup),
            item: DayPlannerTimelineView.resolveRenderGroupItem(renderGroup),
            ...DayPlannerTimelineView.resolveRenderGroupPillOptions(
               renderGroup,
               scheduleHandlers,
               strings
            ),
         });
      });
   }
}
