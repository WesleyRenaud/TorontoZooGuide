import { Dom } from '../dom.js';
import { Strings } from '../../../strings.js';

function makeToggleButton({ label, view, activeView, onSelect }) {
   const button = Dom.el('button', 'itin-panel-view-toggle-button', label);
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

export class ItineraryPanelViews {
   static ITINERARY_PANEL_VIEWS = {
      list: 'list',
      dayPlanner: 'dayPlanner',
   };

   static makeItineraryPanelViews({
      activeView = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list,
      onViewChange = null,
   } = {}) {
      const root = Dom.el('div', 'itin-panel-view-shell');
      const toggle = Dom.el('div', 'itin-panel-view-toggle');
      const sharedHeader = Dom.el('div', 'itin-panel-shared-header');
      const listView = Dom.el('div', 'itin-panel-view itin-panel-list-view');
      const dayPlannerView = Dom.el('div', 'itin-panel-view itin-panel-day-planner-view');

      listView.dataset.view = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list;
      dayPlannerView.dataset.view = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.dayPlanner;

      const selectView = (view) => {
         onViewChange?.(view);
         setViewVisibility(root, view);
      };

      toggle.appendChild(
         makeToggleButton({
            label: Strings.itinerary.dayPlanner.listViewLabel,
            view: ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list,
            activeView,
            onSelect: selectView,
         })
      );
      toggle.appendChild(
         makeToggleButton({
            label: Strings.itinerary.dayPlanner.dayPlannerLabel,
            view: ItineraryPanelViews.ITINERARY_PANEL_VIEWS.dayPlanner,
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
}
