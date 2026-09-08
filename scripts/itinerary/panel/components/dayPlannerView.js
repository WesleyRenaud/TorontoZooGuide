import { DayPlannerController } from './dayPlannerController.js';
import { DayPlannerPreviewBuilder } from './dayPlannerPreviewBuilder.js';
import { DayPlannerScheduleController } from '../dayPlannerScheduleController.js';
import { DayPlannerScheduledItems } from '../dayPlannerScheduledItems.js';
import { DayPlannerTimelinePillAppender } from './dayPlannerTimelinePillAppender.js';
import { DayPlannerTimelineRenderer } from '../dayPlannerTimelineRenderer.js';
import { DayPlannerTimelineView } from './dayPlannerTimelineView.js';
import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ScheduledPillRenderBuilder } from './scheduledPillRenderBuilder.js';
import { SectionConfigs } from '../sectionConfigs.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';
import { Strings } from '../../../strings.js';

export class DayPlannerView {
   static makeDayPlannerPreview(
      zooHours = null,
      itinerary = {},
      timeHandlers = {},
      {
      onScheduleItemClick = null,
      onRebuildScheduleClick = null,
      onUnscheduleAllItemsClick = null,
      scheduleHandlers = {},
      } = {}
   ) {
      const strings = {
         ...Strings.itinerary.dayPlanner,
         timeOrderInvalid: Strings.itinerary.errors.timeOrderInvalid,
         departureLabel: Strings.labels.departure,
      };
      const hours = zooHours && typeof zooHours === 'object'
         ? zooHours
         : {};
      const root = ItineraryPanelHelper.el('div', 'itinerary-day-planner-content');
      const section = ItineraryPanelHelper.el('section', 'itinerary-day-module');
      const header = ItineraryPanelHelper.el('div', 'itinerary-day-module-header');
      const headerAside = ItineraryPanelHelper.el('div', 'itinerary-day-module-header-aside');
      const scheduleActions = ItineraryPanelHelper.el('div', 'itinerary-day-module-schedule-actions');
      const titleWrap = ItineraryPanelHelper.el('div');
      const title = ItineraryPanelHelper.el('h3', '', strings.title);
      const date = ItineraryItemFormatter.formatISODateFull(hours.date, strings.date);
      const timeline = ItineraryPanelHelper.el('div', 'itinerary-day-timeline');

      section.setAttribute('aria-label', strings.aria);
      timeline.setAttribute('aria-hidden', 'true');

      titleWrap.appendChild(title);
      header.appendChild(titleWrap);
      headerAside.appendChild(
         DayPlannerController.makeDayPlannerControls(date, itinerary, timeHandlers, strings, hours)
      );
      header.appendChild(headerAside);

      const earlyAdmissionMinutes = DayPlannerScheduleController.parseClockTimeMinutes(hours.earlyAdmissionTime);
      const openMinutes = DayPlannerScheduleController.parseClockTimeMinutes(hours.openTime);
      const lastAdmissionMinutes = DayPlannerScheduleController.parseClockTimeMinutes(hours.lastAdmissionTime);
      const closeMinutes = DayPlannerScheduleController.parseClockTimeMinutes(hours.closeTime);
      const timelineStartMinutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(hours, itinerary);
      const halfHourSlotStarts = DayPlannerScheduleController.buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);
      const itineraryTimeMarkers = DayPlannerTimelineRenderer.buildItineraryTimeMarkers(itinerary, strings);
      const timelineSlotStarts = DayPlannerPreviewBuilder.buildTimelineSlotStarts(
         halfHourSlotStarts,
         closeMinutes
      );
      const markersByAnchorSlot = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
         itineraryTimeMarkers,
         timelineSlotStarts,
         closeMinutes
      );
      const scheduledRowsContext = DayPlannerScheduledItems.buildScheduledItemRowsContext(
         itinerary,
         timelineSlotStarts,
         closeMinutes
      );
      const scheduledPillRenderGroupsByAnchor = ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor(
         [...scheduledRowsContext.itemsByStart.values()].flat(),
         DayPlannerPreviewBuilder.buildTimelinePointPillMarkers({
            earlyAdmissionMinutes,
            openMinutes,
            lastAdmissionMinutes,
            closeMinutes,
            itineraryTimeMarkers,
         })
      );

      const scheduleActionOptions = {
         onScheduleItemClick,
         onRebuildScheduleClick,
         onUnscheduleAllItemsClick,
         strings,
      };

      if (timelineSlotStarts.length === 0) {
         section.appendChild(header);
         DayPlannerPreviewBuilder.appendScheduleActionButtons(scheduleActions, scheduleActionOptions);

         if (scheduleActions.children.length > 0) {
            section.appendChild(scheduleActions);
         }

         section.appendChild(DayPlannerTimelineView.makeUnavailableMessage(strings.hoursUnavailable));
         root.appendChild(section);
         return root;
      }

      const pillContext = {
         earlyAdmissionMinutes,
         openMinutes,
         lastAdmissionMinutes,
         closeMinutes,
      };

      timelineSlotStarts.forEach((slotStart, slotIndex) => {
         const nextSlotStart = timelineSlotStarts[slotIndex + 1];
         const slotSpanMinutes = Number.isFinite(nextSlotStart)
            ? nextSlotStart - slotStart
            : TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
         const pillLabel = DayPlannerTimelineRenderer.resolveTimelinePillLabel(slotStart, pillContext, strings);
         const [timeCell, gridLine] = DayPlannerTimelineView.makeTimelineRow(
            DayPlannerScheduleController.formatMinutesAsClockTime(slotStart),
            slotSpanMinutes
         );

         timeline.appendChild(timeCell);
         timeline.appendChild(gridLine);

         if (pillLabel) {
            DayPlannerTimelineView.appendTimelineBoundaryLabel(timeCell, pillLabel);
         }

         DayPlannerTimelinePillAppender.appendItineraryTimeMarkers(
            gridLine,
            markersByAnchorSlot,
            slotStart,
            timeHandlers,
            strings,
            itinerary.itineraryConfig?.visitBoundaryEventTypes
         );
         DayPlannerTimelineView.appendScheduledItems(
            gridLine,
            scheduledPillRenderGroupsByAnchor.get(slotStart),
            scheduleHandlers,
            strings
         );
      });

      DayPlannerPreviewBuilder.appendScheduleActionButtons(scheduleActions, scheduleActionOptions);
      section.appendChild(header);

      if (scheduleActions.children.length > 0) {
         section.appendChild(scheduleActions);
      }

      section.appendChild(timeline);
      root.appendChild(section);

      const scheduledSection = DayPlannerPreviewBuilder.makeItemsListSection(
         DayPlannerScheduledItems.buildScheduledItinerary(itinerary, scheduledRowsContext),
         strings.scheduledTitle,
         {
            editButtonSectionKeys: SectionConfigs.SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS,
            onUnscheduleItem: scheduleHandlers.onUnscheduleItineraryItem,
            onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
            splitTransportationSequences: true,
         }
      );
      const unscheduledSection = DayPlannerPreviewBuilder.makeItemsListSection(
         DayPlannerScheduledItems.buildUnscheduledItinerary(itinerary, scheduledRowsContext),
         strings.unscheduledTitle,
         {
            onScheduleItem: scheduleHandlers.onScheduleItineraryItem,
            onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
            sectionKeys: SectionConfigs.UNSCHEDULED_DAY_PLANNER_SECTION_KEYS,
         }
      );

      if (scheduledSection) {
         root.appendChild(scheduledSection);
      }

      if (unscheduledSection) {
         root.appendChild(unscheduledSection);
      }

      return root;
   }
}
