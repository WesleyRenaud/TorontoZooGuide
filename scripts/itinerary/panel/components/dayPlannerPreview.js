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
   buildItineraryTimeMarkers,
   buildMarkersByStart,
   resolveTimelinePillLabel,
} from '../dayPlannerTimelineMarkers.js';
import {
   appendScheduledItems,
   makeTimelineRow,
   makeUnavailableMessage,
} from './dayPlannerTimeline.js';
import { appendItineraryTimeMarkers } from './dayPlannerTimelinePills.js';
import { el } from '../dom.js';
import {
   formatISODateFull,
} from '../format.js';
import { makeSection } from './section.js';
import { buildSectionConfigs } from '../sectionConfigs.js';
import { APP_STRINGS } from '../../../strings.js';

function makeItemsListSection(itinerary = {}, sectionTitle = '') {
   const sectionConfigs = buildSectionConfigs(itinerary);

   if (sectionConfigs.length === 0) {
      return null;
   }

   const wrapper = el('section', 'itinerary-day-items-sections');
   const title = el('h4', 'itinerary-day-items-title', sectionTitle);

   wrapper.appendChild(title);
   sectionConfigs.forEach((sectionConfig) => {
      wrapper.appendChild(makeSection(sectionConfig));
   });

   return wrapper;
}

function buildTimelineSlotStarts(halfHourSlotStarts, itineraryTimeMarkers, closeMinutes) {
   return [
      ...new Set([
         ...halfHourSlotStarts,
         ...itineraryTimeMarkers.map((marker) => marker.startMinutes),
         closeMinutes,
      ].filter(Number.isFinite)),
   ].sort((left, right) => left - right);
}

export function makeDayPlannerPreview(
   zooHours = null,
   itinerary = {},
   timeHandlers = {}
) {
   const strings = APP_STRINGS.itinerary.dayPlanner;
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
      itineraryTimeMarkers,
      closeMinutes
   );
   const markersByStart = buildMarkersByStart(itineraryTimeMarkers);
   const scheduledRowsContext = buildScheduledItemRowsContext(
      itinerary,
      timelineSlotStarts
   );

   if (timelineSlotStarts.length === 0) {
      section.appendChild(header);
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
         formatMinutesAsClockTime(slotStart),
         pillLabel
      );

      appendItineraryTimeMarkers(gridLine, markersByStart, slotStart);
      appendScheduledItems(gridLine, scheduledRowsContext.itemsByStart.get(slotStart));
      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);
   });

   section.appendChild(header);
   section.appendChild(timeline);
   root.appendChild(section);

   const scheduledSection = makeItemsListSection(
      buildScheduledItinerary(itinerary, scheduledRowsContext),
      strings.scheduledTitle
   );
   const unscheduledSection = makeItemsListSection(
      buildUnscheduledItinerary(itinerary, scheduledRowsContext),
      strings.unscheduledTitle
   );

   if (scheduledSection) {
      root.appendChild(scheduledSection);
   }

   if (unscheduledSection) {
      root.appendChild(unscheduledSection);
   }

   return root;
}
