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
   const sharedHeader = el('div', 'itin-panel-shared-header');
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

   root.appendChild(sharedHeader);
   root.appendChild(toggle);
   root.appendChild(listView);
   root.appendChild(dayPlannerView);
   setViewVisibility(root, activeView);

   return {
      root,
      sharedHeader,
      listView,
      dayPlannerView,
   };
}
