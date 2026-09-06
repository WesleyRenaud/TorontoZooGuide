import { DayPlannerActionFeedback } from '../dayPlannerActionFeedback.js';
import { DayPlannerActionFeedbackBanner } from './dayPlannerActionFeedbackBanner.js';
import { DayPlannerControls } from './dayPlannerControls.js';
import { DayPlannerSchedule } from '../dayPlannerSchedule.js';
import { DayPlannerScheduledItems } from '../dayPlannerScheduledItems.js';
import { DayPlannerTimeline } from './dayPlannerTimeline.js';
import { DayPlannerTimelineMarkers } from '../dayPlannerTimelineMarkers.js';
import { DayPlannerTimelinePillAppend } from './dayPlannerTimelinePillAppend.js';
import { Dom } from '../dom.js';
import { Format } from '../format.js';
import { ScheduledPillRenderPlan } from './scheduledPillRenderPlan.js';
import { ScheduleItemButton } from './scheduleItemButton.js';
import { Section } from './section.js';
import { SectionConfigs } from '../sectionConfigs.js';
import { Constants } from '../../../shared/constants.js';
import { APP_STRINGS } from '../../../strings.js';
import { labels } from '../../../strings/common.js';

function resolveSectionShowEditButton(
   sectionKey,
   {
      showEditButton = true,
      editButtonSectionKeys = null,
   } = {}
) {
   if (editButtonSectionKeys) {
      return editButtonSectionKeys.includes(sectionKey);
   }

   return showEditButton;
}

function makeItemsListSection(
   itinerary = {},
   sectionTitle = '',
   {
      showEditButton = true,
      editButtonSectionKeys = null,
      onUnscheduleItem = null,
      onScheduleItem = null,
      onRemoveItem = null,
      sectionKeys = SectionConfigs.SCHEDULED_DAY_PLANNER_SECTION_KEYS,
      splitTransportationSequences = false,
   } = {}
) {
   const sectionConfigs = SectionConfigs.buildSectionConfigs(itinerary, {
      keys: sectionKeys,
      onUnscheduleItem,
      onScheduleItem,
      onRemoveItem,
      splitTransportationSequences,
   });

   if (sectionConfigs.length === 0) {
      return null;
   }

   const wrapper = Dom.el('section', 'itinerary-day-items-sections');
   const title = Dom.el('h4', 'itinerary-day-items-title', sectionTitle);

   wrapper.appendChild(title);
   sectionConfigs.forEach((sectionConfig) => {
      wrapper.appendChild(Section.makeSection({
         ...sectionConfig,
         showEditButton: resolveSectionShowEditButton(sectionConfig.key, {
            showEditButton,
            editButtonSectionKeys,
         }),
      }));
   });

   return wrapper;
}

function appendScheduleActionButtons(
   container,
   {
      onScheduleItemClick = null,
      onRebuildScheduleClick = null,
      onUnscheduleAllItemsClick = null,
      strings = {},
   } = {}
) {
   const buttons = [];
   const feedback = DayPlannerActionFeedback.consumePendingDayPlannerActionFeedback();

   if (typeof onScheduleItemClick === 'function') {
      buttons.push(
         ScheduleItemButton.makeScheduleItemButton({
            label: strings.scheduleItemButton,
            onClick: onScheduleItemClick,
         })
      );
   }

   if (typeof onRebuildScheduleClick === 'function') {
      const rebuildScheduleButton = ScheduleItemButton.makeScheduleItemButton({
         label: strings.rebuildScheduleButton,
         variant: 'secondary',
      });

      rebuildScheduleButton.addEventListener('click', () => {
         void ScheduleItemButton.runScheduleItemButtonAction(
            rebuildScheduleButton,
            onRebuildScheduleClick,
            strings.rebuildScheduleButtonBusy
         );
      });

      buttons.push(rebuildScheduleButton);
   }

   if (typeof onUnscheduleAllItemsClick === 'function') {
      const unscheduleAllButton = ScheduleItemButton.makeScheduleItemButton({
         label: strings.unscheduleAllButton,
         variant: 'destructive',
      });

      unscheduleAllButton.addEventListener('click', () => {
         void ScheduleItemButton.runScheduleItemButtonAction(
            unscheduleAllButton,
            onUnscheduleAllItemsClick,
            strings.unscheduleAllButtonBusy
         );
      });

      buttons.push(unscheduleAllButton);
   }

   if (buttons.length > 0) {
      container.appendChild(ScheduleItemButton.makeScheduleActionsBar(buttons));

      const feedbackSlot = DayPlannerActionFeedbackBanner.appendDayPlannerActionFeedbackSlot(container);

      if (feedback) {
         DayPlannerActionFeedbackBanner.appendDayPlannerActionFeedbackBanner(feedbackSlot, feedback);
      }
   }
}

function buildTimelinePointPillMarkers({
   earlyAdmissionMinutes,
   openMinutes,
   lastAdmissionMinutes,
   closeMinutes,
   itineraryTimeMarkers = [],
} = {}) {
   return [
      earlyAdmissionMinutes,
      openMinutes,
      lastAdmissionMinutes,
      closeMinutes,
      ...itineraryTimeMarkers.map((marker) => marker.startMinutes),
   ]
      .filter((startMinutes) => Number.isFinite(startMinutes))
      .map((startMinutes) => ({ startMinutes }));
}

function buildTimelineSlotStarts(halfHourSlotStarts, closeMinutes) {
   const slotStarts = [...halfHourSlotStarts];

   if (Number.isFinite(closeMinutes) && !slotStarts.includes(closeMinutes)) {
      slotStarts.push(closeMinutes);
      slotStarts.sort((left, right) => left - right);
   }

   return slotStarts;
}

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
         ...APP_STRINGS.itinerary.dayPlanner,
         timeOrderInvalid: APP_STRINGS.itinerary.errors.timeOrderInvalid,
         departureLabel: labels.departure,
      };
      const hours = zooHours && typeof zooHours === 'object'
         ? zooHours
         : {};
      const root = Dom.el('div', 'itinerary-day-planner-content');
      const section = Dom.el('section', 'itinerary-day-module');
      const header = Dom.el('div', 'itinerary-day-module-header');
      const headerAside = Dom.el('div', 'itinerary-day-module-header-aside');
      const scheduleActions = Dom.el('div', 'itinerary-day-module-schedule-actions');
      const titleWrap = Dom.el('div');
      const title = Dom.el('h3', '', strings.title);
      const date = Format.formatISODateFull(hours.date, strings.date);
      const timeline = Dom.el('div', 'itinerary-day-timeline');

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
      const timelineSlotStarts = buildTimelineSlotStarts(
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
         buildTimelinePointPillMarkers({
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
         appendScheduleActionButtons(scheduleActions, scheduleActionOptions);

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
            : Constants.TIMELINE_SLOT_MINUTES;
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

      appendScheduleActionButtons(scheduleActions, scheduleActionOptions);
      section.appendChild(header);

      if (scheduleActions.children.length > 0) {
         section.appendChild(scheduleActions);
      }

      section.appendChild(timeline);
      root.appendChild(section);

      const scheduledSection = makeItemsListSection(
         DayPlannerScheduledItems.buildScheduledItinerary(itinerary, scheduledRowsContext),
         strings.scheduledTitle,
         {
            editButtonSectionKeys: SectionConfigs.SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS,
            onUnscheduleItem: scheduleHandlers.onUnscheduleItineraryItem,
            onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
            splitTransportationSequences: true,
         }
      );
      const unscheduledSection = makeItemsListSection(
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
