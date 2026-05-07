import { el } from '../dom.js';
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

export function makeDayPlannerPreview() {
   const strings = APP_STRINGS.itinerary.dayPlanner;
   const section = el('section', 'itinerary-day-module');
   const header = el('div', 'itinerary-day-module-header');
   const titleWrap = el('div');
   const kicker = el('div', 'itinerary-day-module-kicker', APP_STRINGS.site.nav.itinerary);
   const title = el('h3', '', strings.title);
   const date = el('span', 'itinerary-day-module-date', strings.date);
   const timeline = el('div', 'itinerary-day-timeline');

   section.setAttribute('aria-label', strings.aria);
   timeline.setAttribute('aria-hidden', 'true');

   titleWrap.appendChild(kicker);
   titleWrap.appendChild(title);
   header.appendChild(titleWrap);
   header.appendChild(date);

   timeline.appendChild(el('div', 'itinerary-day-time', strings.firstSlot));
   timeline.appendChild(el('div', 'itinerary-day-grid-line'));

   const eventLine = el('div', 'itinerary-day-grid-line');
   const event = el('article', 'itinerary-day-event');
   event.appendChild(
      el('div', 'itinerary-day-event-time', `${strings.secondSlot} - ${strings.eventEnd}`)
   );
   event.appendChild(el('div', 'itinerary-day-event-title', strings.eventTitle));
   event.appendChild(el('div', 'itinerary-day-event-location', strings.eventLocation));
   eventLine.appendChild(event);

   timeline.appendChild(el('div', 'itinerary-day-time', strings.secondSlot));
   timeline.appendChild(eventLine);

   const openLine = el('div', 'itinerary-day-grid-line');
   openLine.appendChild(el('span', 'itinerary-day-open-pill', strings.openLabel));

   timeline.appendChild(el('div', 'itinerary-day-time', strings.thirdSlot));
   timeline.appendChild(openLine);

   section.appendChild(header);
   section.appendChild(timeline);

   return section;
}
