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

export function makeDayPlannerPreview(zooHours = null) {
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

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   header.appendChild(date);

   const openMinutes = parseClockTimeMinutes(hours.openTime);
   const lastAdmissionMinutes = parseClockTimeMinutes(hours.lastAdmissionTime);
   const closeMinutes = parseClockTimeMinutes(hours.closeTime);
   const halfHourSlotStarts = buildHalfHourSlotStarts(openMinutes, closeMinutes);

   if (halfHourSlotStarts.length === 0) {
      section.appendChild(header);
      section.appendChild(makeUnavailableMessage(strings.hoursUnavailable));
      return section;
   }

   halfHourSlotStarts.forEach((slotStart) => {
      const pillLabel = slotStart === openMinutes
         ? strings.openLabel
         : slotStart === lastAdmissionMinutes
            ? strings.lastAdmissionLabel
            : null;
      const [timeCell, gridLine] = makeTimelineRow(
         formatMinutesAsClockTime(slotStart),
         pillLabel
      );

      timeline.appendChild(timeCell);
      timeline.appendChild(gridLine);
   });

   timeline.append(...makeTimelineRow(closeTime, strings.closeLabel));

   section.appendChild(header);
   section.appendChild(timeline);

   return section;
}
