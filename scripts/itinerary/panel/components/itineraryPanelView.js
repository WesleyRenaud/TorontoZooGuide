import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPanelViewsHelper } from './itineraryPanelViewsHelper.js';
import { Strings } from '../../../strings.js';

export class ItineraryPanelView {
   static ITINERARY_PANEL_VIEWS = {
      list: 'list',
      dayPlanner: 'dayPlanner',
   };

   static makeItineraryPanelViews({
      activeView = ItineraryPanelView.ITINERARY_PANEL_VIEWS.list,
      onViewChange = null,
   } = {}) {
      const root = ItineraryPanelHelper.el('div', 'itin-panel-view-shell');
      const toggle = ItineraryPanelHelper.el('div', 'itin-panel-view-toggle');
      const sharedHeader = ItineraryPanelHelper.el('div', 'itin-panel-shared-header');
      const listView = ItineraryPanelHelper.el('div', 'itin-panel-view itin-panel-list-view');
      const dayPlannerView = ItineraryPanelHelper.el('div', 'itin-panel-view itin-panel-day-planner-view');

      listView.dataset.view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.list;
      dayPlannerView.dataset.view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;

      const selectView = (view) => {
         onViewChange?.(view);
         ItineraryPanelViewsHelper.setViewVisibility(root, view);
      };

      toggle.appendChild(
         ItineraryPanelViewsHelper.makeToggleButton({
            label: Strings.itinerary.dayPlanner.listViewLabel,
            view: ItineraryPanelView.ITINERARY_PANEL_VIEWS.list,
            activeView,
            onSelect: selectView,
         })
      );
      toggle.appendChild(
         ItineraryPanelViewsHelper.makeToggleButton({
            label: Strings.itinerary.dayPlanner.dayPlannerLabel,
            view: ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner,
            activeView,
            onSelect: selectView,
         })
      );

      root.appendChild(sharedHeader);
      root.appendChild(toggle);
      root.appendChild(listView);
      root.appendChild(dayPlannerView);
      ItineraryPanelViewsHelper.setViewVisibility(root, activeView);

      return {
         root,
         sharedHeader,
         listView,
         dayPlannerView,
      };
   }
}
