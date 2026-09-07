import { ItineraryPanelDom } from '../itineraryPanelDom.js';
import { ItineraryPanelViewsHelpers } from './itineraryPanelViewsHelpers.js';
import { Strings } from '../../../strings.js';

export class ItineraryPanelViews {
   static ITINERARY_PANEL_VIEWS = {
      list: 'list',
      dayPlanner: 'dayPlanner',
   };

   static makeItineraryPanelViews({
      activeView = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list,
      onViewChange = null,
   } = {}) {
      const root = ItineraryPanelDom.el('div', 'itin-panel-view-shell');
      const toggle = ItineraryPanelDom.el('div', 'itin-panel-view-toggle');
      const sharedHeader = ItineraryPanelDom.el('div', 'itin-panel-shared-header');
      const listView = ItineraryPanelDom.el('div', 'itin-panel-view itin-panel-list-view');
      const dayPlannerView = ItineraryPanelDom.el('div', 'itin-panel-view itin-panel-day-planner-view');

      listView.dataset.view = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list;
      dayPlannerView.dataset.view = ItineraryPanelViews.ITINERARY_PANEL_VIEWS.dayPlanner;

      const selectView = (view) => {
         onViewChange?.(view);
         ItineraryPanelViewsHelpers.setViewVisibility(root, view);
      };

      toggle.appendChild(
         ItineraryPanelViewsHelpers.makeToggleButton({
            label: Strings.itinerary.dayPlanner.listViewLabel,
            view: ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list,
            activeView,
            onSelect: selectView,
         })
      );
      toggle.appendChild(
         ItineraryPanelViewsHelpers.makeToggleButton({
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
      ItineraryPanelViewsHelpers.setViewVisibility(root, activeView);

      return {
         root,
         sharedHeader,
         listView,
         dayPlannerView,
      };
   }
}
