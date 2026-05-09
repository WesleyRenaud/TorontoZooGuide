import {
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
} from '../dayPlannerSchedule.js';
import { el } from '../dom.js';
import {
   formatClockTime,
   formatISODateFull,
} from '../format.js';
import {
   buildGuardiansRows,
   buildWildRows,
} from '../rows.js';
import { APP_STRINGS } from '../../../strings.js';

export const ITINERARY_PANEL_VIEWS = {
   list: 'list',
   dayPlanner: 'dayPlanner',
};

function makeToggleButton({ label, view, activeView, onSelect }) {
   const button = el('button', 'itin-panel-view-toggle-button', label);
   button.type = 'button';
   button.dataset.view = view;
   button.setAttribute('aria-pressed', view === activeView ? 'true' : 'false');
   button.addEventListener('click', () => onSelect(view));
   return button;
}

function setViewVisibility(root, selectedView) {
   root.querySelectorAll('.itin-panel-view-toggle-button').forEach((button) => {
      const isSelected = button.dataset.view === selectedView;
      button.classList.toggle('itin-panel-view-toggle-button-active', isSelected);
      button.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
   });

   root.querySelectorAll('.itin-panel-view').forEach((view) => {
      view.hidden = view.dataset.view !== selectedView;
   });
}

function makeTimelineRow(timeLabel, pillLabel) {
   const gridLine = el('div', 'itinerary-day-grid-line');

   if (pillLabel) {
      gridLine.appendChild(el('span', 'itinerary-day-open-pill', pillLabel));
   }

   return [
      el('div', 'itinerary-day-time', timeLabel),
      gridLine,
   ];
}

function makeUnavailableMessage(message) {
   return el('div', 'itinerary-day-unavailable', message);
}

function getScheduledDuration(item) {
   const duration = Number(item?.duration);
   return Number.isFinite(duration) && duration > 0 ? duration : null;
}

function makeScheduledItemBlock(itemRow, duration) {
   const block = el('div', 'itinerary-day-event');
   const slotSpan = Math.max(duration / 30, 1);

   block.style.setProperty('--itinerary-event-slot-span', slotSpan);
   itemRow.classList.add('itinerary-day-event-card');
   block.appendChild(itemRow);

   return block;
}

function buildScheduledItemRows(items, buildRows) {
   return items.map((item) => {
      const [row] = buildRows([item]);
      const duration = getScheduledDuration(item);
      return {
         item,
         row,
         startMinutes: parseClockTimeMinutes(item?.time_of_day),
         duration,
      };
   }).filter((scheduledItem) => (
      scheduledItem.row
      && Number.isFinite(scheduledItem.startMinutes)
      && Number.isFinite(scheduledItem.duration)
   ));
}

function buildScheduledItemRowsByStart({
   guardiansTalks = [],
   wildEncounters = [],
} = {}) {
   const scheduledItems = [
      ...buildScheduledItemRows(guardiansTalks, buildGuardiansRows),
      ...buildScheduledItemRows(wildEncounters, buildWildRows),
   ];

   return scheduledItems.reduce((itemsByStart, scheduledItem) => {
      const items = itemsByStart.get(scheduledItem.startMinutes) ?? [];
      items.push(scheduledItem);
      itemsByStart.set(scheduledItem.startMinutes, items);
      return itemsByStart;
   }, new Map());
}

function appendScheduledItems(gridLine, scheduledItems = []) {
   scheduledItems.forEach((scheduledItem) => {
      gridLine.appendChild(
         makeScheduledItemBlock(scheduledItem.row, scheduledItem.duration)
      );
   });
}

export function makeItineraryPanelViews({
   activeView = ITINERARY_PANEL_VIEWS.list,
   onViewChange = null,
} = {}) {
   const root = el('div', 'itin-panel-view-shell');
   const toggle = el('div', 'itin-panel-view-toggle');
   const listView = el('div', 'itin-panel-view itin-panel-list-view');
   const dayPlannerView = el('div', 'itin-panel-view itin-panel-day-planner-view');

   listView.dataset.view = ITINERARY_PANEL_VIEWS.list;
   dayPlannerView.dataset.view = ITINERARY_PANEL_VIEWS.dayPlanner;

   const selectView = (view) => {
      onViewChange?.(view);
      setViewVisibility(root, view);
   };

   toggle.appendChild(
      makeToggleButton({
         label: APP_STRINGS.itinerary.dayPlanner.listViewLabel,
         view: ITINERARY_PANEL_VIEWS.list,
         activeView,
         onSelect: selectView,
      })
   );
   toggle.appendChild(
      makeToggleButton({
         label: APP_STRINGS.itinerary.dayPlanner.dayPlannerLabel,
         view: ITINERARY_PANEL_VIEWS.dayPlanner,
         activeView,
         onSelect: selectView,
      })
   );

   root.appendChild(toggle);
   root.appendChild(listView);
   root.appendChild(dayPlannerView);
   setViewVisibility(root, activeView);

   return {
      root,
      listView,
      dayPlannerView,
   };
}

export function makeDayPlannerPreview(zooHours = null, itinerary = {}) {
   const strings = APP_STRINGS.itinerary.dayPlanner;
   const hours = zooHours && typeof zooHours === 'object'
      ? zooHours
      : {};
   const closeTime = formatClockTime(hours.closeTime, strings.thirdSlot);
   const section = el('section', 'itinerary-day-module');
   const header = el('div', 'itinerary-day-module-header');
   const titleWrap = el('div');
   const title = el('h3', '', strings.title);
   const date = el('span', 'itinerary-day-module-date', formatISODateFull(hours.date, strings.date));
   const timeline = el('div', 'itinerary-day-timeline');
   const scheduledItemRowsByStart = buildScheduledItemRowsByStart(itinerary);

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   header.appendChild(date);

   const earlyAdmissionMinutes = parseClockTimeMinutes(hours.earlyAdmissionTime);
   const openMinutes = parseClockTimeMinutes(hours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(hours.lastAdmissionTime);
   const closeMinutes = parseClockTimeMinutes(hours.closeTime);
   const timelineStartMinutes = Number.isFinite(earlyAdmissionMinutes)
      ? earlyAdmissionMinutes
      : openMinutes;
   const halfHourSlotStarts = buildHalfHourSlotStarts(timelineStartMinutes, closeMinutes);

   if (halfHourSlotStarts.length === 0) {
      section.appendChild(header);
      section.appendChild(makeUnavailableMessage(strings.hoursUnavailable));
      return section;
   }

   halfHourSlotStarts.forEach((slotStart) => {
      let pillLabel = null;

      if (slotStart === earlyAdmissionMinutes) {
         pillLabel = strings.earlyAdmissionLabel;
      } else if (slotStart === openMinutes) {
         pillLabel = strings.openLabel;
      } else if (slotStart === lastAdmissionMinutes) {
         pillLabel = strings.lastAdmissionLabel;
      }

      const [timeCell, gridLine] = makeTimelineRow(
         formatMinutesAsClockTime(slotStart),
         pillLabel
      );

      appendScheduledItems(gridLine, scheduledItemRowsByStart.get(slotStart));
      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);
   });

   timeline.append(...makeTimelineRow(closeTime, strings.closeLabel));

   section.appendChild(header);
   section.appendChild(timeline);

   return section;
}
