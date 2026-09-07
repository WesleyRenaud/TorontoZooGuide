import { DayPlannerControls } from './dayPlannerControls.js';
import { DayPlannerPreviewBuilder } from './dayPlannerPreviewBuilder.js';
import { DayPlannerSchedule } from '../dayPlannerSchedule.js';
import { DayPlannerScheduledItems } from '../dayPlannerScheduledItems.js';
import { DayPlannerTimeline } from './dayPlannerTimeline.js';
import { DayPlannerTimelineMarkers } from '../dayPlannerTimelineMarkers.js';
import { DayPlannerTimelinePillAppend } from './dayPlannerTimelinePillAppend.js';
import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ScheduledPillRenderPlan } from './scheduledPillRenderPlan.js';
import { SectionConfigs } from '../sectionConfigs.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';
import { Strings } from '../../../strings.js';

export class DayPlannerPreview {
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
      const root = ItineraryPanelDom.el('div', 'itinerary-day-planner-content');
      const section = ItineraryPanelDom.el('section', 'itinerary-day-module');
      const header = ItineraryPanelDom.el('div', 'itinerary-day-module-header');
      const headerAside = ItineraryPanelDom.el('div', 'itinerary-day-module-header-aside');
      const scheduleActions = ItineraryPanelDom.el('div', 'itinerary-day-module-schedule-actions');
      const titleWrap = ItineraryPanelDom.el('div');
      const title = ItineraryPanelDom.el('h3', '', strings.title);
      const date = ItineraryItemFormatter.formatISODateFull(hours.date, strings.date);
      const timeline = ItineraryPanelDom.el('div', 'itinerary-day-timeline');

      section.setAttribute('aria-label', strings.aria);
      timeline.setAttribute('aria-hidden', 'true');

      titleWrap.appendChild(title);
      header.appendChild(titleWrap);
      headerAside.appendChild(
         DayPlannerControls.makeDayPlannerControls(date, itinerary, timeHandlers, strings, hours)
      );
      header.appendChild(headerAside);

      const earlyAdmissionMinutes = DayPlannerSchedule.parseClockTimeMinutes(hours.earlyAdmissionTime);
      const openMinutes = DayPlannerSchedule.parseClockTimeMinutes(hours.openTime);
      const lastAdmissionMinutes = DayPlannerSchedule.parseClockTimeMinutes(hours.lastAdmissionTime);
      const closeMinutes = DayPlannerSchedule.parseClockTimeMinutes(hours.closeTime);
      const timelineStartMinutes = DayPlannerSchedule.resolveDayPlannerTimelineStartMinutes(hours, itinerary);
      const halfHourSlotStarts = DayPlannerSchedule.buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);
      const itineraryTimeMarkers = DayPlannerTimelineMarkers.buildItineraryTimeMarkers(itinerary, strings);
      const timelineSlotStarts = DayPlannerPreviewBuilder.buildTimelineSlotStarts(
         halfHourSlotStarts,
         closeMinutes
      );
      const markersByAnchorSlot = DayPlannerTimelineMarkers.buildMarkersByAnchorSlot(
         itineraryTimeMarkers,
         timelineSlotStarts,
         closeMinutes
      );
      const scheduledRowsContext = DayPlannerScheduledItems.buildScheduledItemRowsContext(
         itinerary,
         timelineSlotStarts,
         closeMinutes
      );
      const scheduledPillRenderGroupsByAnchor = ScheduledPillRenderPlan.planScheduledPillRenderGroupsByAnchor(
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

         section.appendChild(DayPlannerTimeline.makeUnavailableMessage(strings.hoursUnavailable));
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
         const pillLabel = DayPlannerTimelineMarkers.resolveTimelinePillLabel(slotStart, pillContext, strings);
         const [timeCell, gridLine] = DayPlannerTimeline.makeTimelineRow(
            DayPlannerSchedule.formatMinutesAsClockTime(slotStart),
            slotSpanMinutes
         );

         timeline.appendChild(timeCell);
         timeline.appendChild(gridLine);

         if (pillLabel) {
            DayPlannerTimeline.appendTimelineBoundaryLabel(timeCell, pillLabel);
         }

         DayPlannerTimelinePillAppend.appendItineraryTimeMarkers(
            gridLine,
            markersByAnchorSlot,
            slotStart,
            timeHandlers,
            strings,
            itinerary.itineraryConfig?.visitBoundaryEventTypes
         );
         DayPlannerTimeline.appendScheduledItems(
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
