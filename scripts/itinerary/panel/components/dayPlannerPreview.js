import { makeDayPlannerControls } from './dayPlannerControls.js';
import {
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
} from '../dayPlannerSchedule.js';
import {
   buildScheduledItemRowsContext,
   buildScheduledItinerary,
   buildUnscheduledItinerary,
} from '../dayPlannerScheduledItems.js';
import {
   appendScheduledItems,
   makeTimelineRow,
   makeUnavailableMessage,
} from './dayPlannerTimeline.js';
import {
   buildItineraryTimeMarkers,
   buildMarkersByAnchorSlot,
   resolveTimelinePillLabel,
} from '../dayPlannerTimelineMarkers.js';
import {
   appendItineraryTimeMarkers,
   appendTimelinePill,
} from './dayPlannerTimelinePills.js';
import { el } from '../dom.js';
import { formatISODateFull } from '../format.js';
import { makeScheduleItemButton } from './scheduleItemButton.js';
import { makeSection } from './section.js';
import { buildSectionConfigs } from '../sectionConfigs.js';
import { APP_STRINGS } from '../../../strings.js';
import { labels } from '../../../strings/common.js';

function makeItemsListSection(
   itinerary = {},
   sectionTitle = '',
   {
      showEditButton = true,
      onUnscheduleItem = null,
      onScheduleItem = null,
   } = {}
) {
   const sectionConfigs = buildSectionConfigs(itinerary, {
      onUnscheduleItem,
      onScheduleItem,
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
         showEditButton,
      }));
   });

   return wrapper;
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
   { onScheduleItemClick = null, scheduleHandlers = {} } = {}
) {
   const strings = {
      ...APP_STRINGS.itinerary.dayPlanner,
      departureLabel: labels.departure,
   };
   const hours = zooHours && typeof zooHours === 'object'
      ? zooHours
      : {};
   const root = el('div', 'itinerary-day-planner-content');
   const section = el('section', 'itinerary-day-module');
   const header = el('div', 'itinerary-day-module-header');
   const titleWrap = el('div');
   const title = el('h3', '', strings.title);
   const date = formatISODateFull(hours.date, strings.date);
   const timeline = el('div', 'itinerary-day-timeline');

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   header.appendChild(
      makeDayPlannerControls(date, itinerary, timeHandlers, strings, hours)
   );

   const earlyAdmissionMinutes = parseClockTimeMinutes(hours.earlyAdmissionTime);
   const openMinutes = parseClockTimeMinutes(hours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(hours.lastAdmissionTime);
   const closeMinutes = parseClockTimeMinutes(hours.closeTime);
   const timelineStartMinutes = Number.isFinite(earlyAdmissionMinutes)
      ? earlyAdmissionMinutes
      : openMinutes;
   const halfHourSlotStarts = buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);
   const itineraryTimeMarkers = buildItineraryTimeMarkers(itinerary, strings);
   const timelineSlotStarts = buildTimelineSlotStarts(
      halfHourSlotStarts,
      closeMinutes
   );
   const markersByAnchorSlot = buildMarkersByAnchorSlot(
      itineraryTimeMarkers,
      timelineSlotStarts,
      closeMinutes
   );
   const scheduledRowsContext = buildScheduledItemRowsContext(
      itinerary,
      timelineSlotStarts,
      closeMinutes
   );

   if (timelineSlotStarts.length === 0) {
      section.appendChild(header);

      if (typeof onScheduleItemClick === 'function') {
         section.appendChild(
            makeScheduleItemButton({
               label: strings.scheduleItemButton,
               onClick: onScheduleItemClick,
            })
         );
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

   timelineSlotStarts.forEach((slotStart) => {
      const pillLabel = resolveTimelinePillLabel(slotStart, pillContext, strings);
      const [timeCell, gridLine] = makeTimelineRow(
         formatMinutesAsClockTime(slotStart)
      );

      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);

      if (pillLabel) {
         appendTimelinePill(gridLine, pillLabel);
      }

      appendScheduledItems(
         gridLine,
         scheduledRowsContext.itemsByStart.get(slotStart),
         scheduleHandlers,
         strings
      );
      appendItineraryTimeMarkers(
         gridLine,
         markersByAnchorSlot,
         slotStart,
         timeHandlers,
         strings,
         itinerary.itineraryConfig?.visitBoundaryEventTypes
      );
   });

   section.appendChild(header);

   if (typeof onScheduleItemClick === 'function') {
      section.appendChild(
         makeScheduleItemButton({
            label: strings.scheduleItemButton,
            onClick: onScheduleItemClick,
         })
      );
   }

   section.appendChild(timeline);
   root.appendChild(section);

   const scheduledSection = makeItemsListSection(
      buildScheduledItinerary(itinerary, scheduledRowsContext),
      strings.scheduledTitle,
      {
         showEditButton: false,
         onUnscheduleItem: scheduleHandlers.onUnscheduleItineraryItem,
      }
   );
   const unscheduledSection = makeItemsListSection(
      buildUnscheduledItinerary(itinerary, scheduledRowsContext),
      strings.unscheduledTitle,
      { onScheduleItem: scheduleHandlers.onScheduleItineraryItem }
   );

   if (scheduledSection) {
      root.appendChild(scheduledSection);
   }

   if (unscheduledSection) {
      root.appendChild(unscheduledSection);
   }

   return root;
}
