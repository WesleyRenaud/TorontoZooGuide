import { ActionsBar } from './components/actionsBar.js';
import { BuildOnly } from './components/buildOnly.js';
import { DateCard } from './components/dateCard.js';
import { ItineraryPanelSectionBuilder } from './components/itineraryPanelSectionBuilder.js';
import { ItineraryPanelContentHelpers } from './itineraryPanelContentHelpers.js';
import { ItineraryPanelScheduleHandlers } from './itineraryPanelScheduleHandlers.js';
import { ItineraryPanelViewState } from './itineraryPanelViewState.js';
import { ItineraryServiceTime } from '../itineraryServiceTime.js';
import { SectionConfigs } from './sectionConfigs.js';

export class ItineraryPanelContent {
   static destroyRenderedPanelChildren(bodyEl) {
      Array.from(bodyEl?.children ?? []).forEach((child) => {
         child.__tzgCleanup?.();
      });
   }

   static clearRenderedPanel(bodyEl) {
      ItineraryPanelContent.destroyRenderedPanelChildren(bodyEl);
      bodyEl?.replaceChildren();
   }

   static buildItineraryPanelContent(
   itinerary,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
      const {
         makeViewShell = ItineraryPanelViewState.makeItineraryPanelViewShell,
         makeActions = ActionsBar.makeActionsBar,
         createDateCard = DateCard.makeDateCard,
         buildSections = SectionConfigs.buildSectionConfigs,
         createSection = ItineraryPanelSectionBuilder.makeSection,
         buildScheduleHandlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers,
         onAfterClear = null,
         setArrivalTime = ItineraryServiceTime.setItineraryArrivalTime,
         setDepartureTime = ItineraryServiceTime.setItineraryDepartureTime,
      } = deps;

      const fragment = document.createDocumentFragment();
      const {
         root,
         sharedHeader,
         listView,
         dayPlannerView,
      } = makeViewShell();

      sharedHeader.appendChild(
         makeActions({
            onAfterClear,
         })
      );

      const dateCard = createDateCard(itinerary);

      if (dateCard) {
         sharedHeader.appendChild(dateCard);
      }

      const scheduleHandlers = buildScheduleHandlers(itinerary, {
         onPanelRefresh,
         deps,
      });

      buildSections(itinerary, {
         onRemoveItem: scheduleHandlers.onRemoveItineraryItem,
      }).forEach((sectionConfig) => {
         listView.appendChild(
            createSection(sectionConfig)
         );
      });

      ItineraryPanelContentHelpers.appendDayPlannerViewWithHours(
         dayPlannerView,
         zooHours,
         itinerary,
         {
            onArrivalTimeChange: async (arrivalTime) => {
               await setArrivalTime(arrivalTime);
               await onPanelRefresh?.();
            },
            onDepartureTimeChange: async (departureTime) => {
               await setDepartureTime(departureTime);
               await onPanelRefresh?.();
            },
         },
         {
            onPanelRefresh,
            deps,
         }
      );
      fragment.appendChild(root);

      return fragment;
   }

   static buildEmptyItineraryPanelContent(
   bodyEl,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
      const {
         makeViewShell = ItineraryPanelViewState.makeItineraryPanelViewShell,
         renderEmptyState = BuildOnly.renderBuildOnly,
      } = deps;

      const {
         root,
         listView,
         dayPlannerView,
      } = makeViewShell();

      renderEmptyState(listView);
      renderEmptyState(dayPlannerView);
      ItineraryPanelContentHelpers.appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
         onPanelRefresh,
         deps,
      });
      bodyEl.appendChild(root);
   }
}
