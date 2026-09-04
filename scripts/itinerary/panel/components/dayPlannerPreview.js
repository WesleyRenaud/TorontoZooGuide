import { DayPlannerActionFeedback } from '../dayPlannerActionFeedback.js';
import {
   appendDayPlannerActionFeedbackBanner,
   appendDayPlannerActionFeedbackSlot,
} from './dayPlannerActionFeedbackBanner.js';
import { makeDayPlannerControls } from './dayPlannerControls.js';
import {
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
   resolveDayPlannerTimelineStartMinutes,
} from '../dayPlannerSchedule.js';
import {
   buildScheduledItemRowsContext,
   buildScheduledItinerary,
   buildUnscheduledItinerary,
} from '../dayPlannerScheduledItems.js';
import {
   appendScheduledItems,
   appendTimelineBoundaryLabel,
   makeTimelineRow,
   makeUnavailableMessage,
} from './dayPlannerTimeline.js';
import { DayPlannerTimelineMarkers } from '../dayPlannerTimelineMarkers.js';
import { appendItineraryTimeMarkers } from './dayPlannerTimelinePillAppend.js';
import { el } from '../dom.js';
import { formatISODateFull } from '../format.js';
import { ScheduledPillRenderPlan } from './scheduledPillRenderPlan.js';
import {
   makeScheduleActionsBar,
   makeScheduleItemButton,
   runScheduleItemButtonAction,
} from './scheduleItemButton.js';
import { makeSection } from './section.js';
import {
   buildSectionConfigs,
   SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS,
   SCHEDULED_DAY_PLANNER_SECTION_KEYS,
   UNSCHEDULED_DAY_PLANNER_SECTION_KEYS,
} from '../sectionConfigs.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';
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
      sectionKeys = SCHEDULED_DAY_PLANNER_SECTION_KEYS,
      splitTransportationSequences = false,
   } = {}
) {
   const sectionConfigs = buildSectionConfigs(itinerary, {
      keys: sectionKeys,
      onUnscheduleItem,
      onScheduleItem,
      onRemoveItem,
      splitTransportationSequences,
   });

   if (sectionConfigs.length === 0) {
      return null;
   }

   const wrapper = el('section', 'itinerary-day-items-sections');
   const title = el('h4', 'itinerary-day-items-title', sectionTitle);

   wrapper.appendChild(title);
   sectionConfigs.forEach((sectionConfig) => {
      wrapper.appendChild(makeSection({
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
         makeScheduleItemButton({
            label: strings.scheduleItemButton,
            onClick: onScheduleItemClick,
         })
      );
   }

   if (typeof onRebuildScheduleClick === 'function') {
      const rebuildScheduleButton = makeScheduleItemButton({
         label: strings.rebuildScheduleButton,
         variant: 'secondary',
      });

      rebuildScheduleButton.addEventListener('click', () => {
         void runScheduleItemButtonAction(
            rebuildScheduleButton,
            onRebuildScheduleClick,
            strings.rebuildScheduleButtonBusy
         );
      });

      buttons.push(rebuildScheduleButton);
   }

   if (typeof onUnscheduleAllItemsClick === 'function') {
      const unscheduleAllButton = makeScheduleItemButton({
         label: strings.unscheduleAllButton,
         variant: 'destructive',
      });

      unscheduleAllButton.addEventListener('click', () => {
         void runScheduleItemButtonAction(
            unscheduleAllButton,
            onUnscheduleAllItemsClick,
            strings.unscheduleAllButtonBusy
         );
      });

      buttons.push(unscheduleAllButton);
   }

   if (buttons.length > 0) {
      container.appendChild(makeScheduleActionsBar(buttons));

      const feedbackSlot = appendDayPlannerActionFeedbackSlot(container);

      if (feedback) {
         appendDayPlannerActionFeedbackBanner(feedbackSlot, feedback);
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

export function makeDayPlannerPreview(
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
   const root = el('div', 'itinerary-day-planner-content');
   const section = el('section', 'itinerary-day-module');
   const header = el('div', 'itinerary-day-module-header');
   const headerAside = el('div', 'itinerary-day-module-header-aside');
   const scheduleActions = el('div', 'itinerary-day-module-schedule-actions');
   const titleWrap = el('div');
   const title = el('h3', '', strings.title);
   const date = formatISODateFull(hours.date, strings.date);
   const timeline = el('div', 'itinerary-day-timeline');

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   headerAside.appendChild(
      makeDayPlannerControls(date, itinerary, timeHandlers, strings, hours)
   );
   header.appendChild(headerAside);

   const earlyAdmissionMinutes = parseClockTimeMinutes(hours.earlyAdmissionTime);
   const openMinutes = parseClockTimeMinutes(hours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(hours.lastAdmissionTime);
   const closeMinutes = parseClockTimeMinutes(hours.closeTime);
   const timelineStartMinutes = resolveDayPlannerTimelineStartMinutes(hours, itinerary);
   const halfHourSlotStarts = buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);
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
   const scheduledRowsContext = buildScheduledItemRowsContext(
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

      section.appendChild(makeUnavailableMessage(strings.hoursUnavailable));
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
         : TIMELINE_SLOT_MINUTES;
      const pillLabel = DayPlannerTimelineMarkers.resolveTimelinePillLabel(slotStart, pillContext, strings);
      const [timeCell, gridLine] = makeTimelineRow(
         formatMinutesAsClockTime(slotStart),
         slotSpanMinutes
      );

      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);

      if (pillLabel) {
         appendTimelineBoundaryLabel(timeCell, pillLabel);
      }

      appendItineraryTimeMarkers(
         gridLine,
         markersByAnchorSlot,
         slotStart,
         timeHandlers,
         strings,
         itinerary.itineraryConfig?.visitBoundaryEventTypes
      );
      appendScheduledItems(
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
      buildScheduledItinerary(itinerary, scheduledRowsContext),
      strings.scheduledTitle,
      {
         editButtonSectionKeys: SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS,
         onUnscheduleItem: scheduleHandlers.onUnscheduleItineraryItem,
         onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
         splitTransportationSequences: true,
      }
   );
   const unscheduledSection = makeItemsListSection(
      buildUnscheduledItinerary(itinerary, scheduledRowsContext),
      strings.unscheduledTitle,
      {
         onScheduleItem: scheduleHandlers.onScheduleItineraryItem,
         onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
         sectionKeys: UNSCHEDULED_DAY_PLANNER_SECTION_KEYS,
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
