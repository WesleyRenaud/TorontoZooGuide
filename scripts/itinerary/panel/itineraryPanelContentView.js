import { ActionsView } from './components/actionsView.js';
import { BuildOnlyBuilder } from './components/buildOnlyBuilder.js';
import { DateView } from './components/dateView.js';
import { ItineraryPanelSectionBuilder } from './components/itineraryPanelSectionBuilder.js';
import { ItineraryPanelContentHelper } from './itineraryPanelContentHelper.js';
import { ItineraryPanelScheduleHandler } from './itineraryPanelScheduleHandler.js';
import { ItineraryPanelViewStore } from './itineraryPanelViewStore.js';
import { ItineraryServiceFormatter } from '../itineraryServiceFormatter.js';
import { SectionConfigs } from './sectionConfigs.js';

export class ItineraryPanelContentView {
   static destroyRenderedPanelChildren(bodyEl) {
      Array.from(bodyEl?.children ?? []).forEach((child) => {
         child.__tzgCleanup?.();
      });
   }

   static clearRenderedPanel(bodyEl) {
      ItineraryPanelContentView.destroyRenderedPanelChildren(bodyEl);
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
         makeViewShell = ItineraryPanelViewStore.makeItineraryPanelViewShell,
         makeActions = ActionsView.makeActionsBar,
         createDateCard = DateView.makeDateCard,
         buildSections = SectionConfigs.buildSectionConfigs,
         createSection = ItineraryPanelSectionBuilder.makeSection,
         buildScheduleHandlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers,
         onAfterClear = null,
         setArrivalTime = ItineraryServiceFormatter.setItineraryArrivalTime,
         setDepartureTime = ItineraryServiceFormatter.setItineraryDepartureTime,
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

      ItineraryPanelContentHelper.appendDayPlannerViewWithHours(
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
         makeViewShell = ItineraryPanelViewStore.makeItineraryPanelViewShell,
         renderEmptyState = BuildOnlyBuilder.renderBuildOnly,
      } = deps;

      const {
         root,
         listView,
         dayPlannerView,
      } = makeViewShell();

      renderEmptyState(listView);
      renderEmptyState(dayPlannerView);
      ItineraryPanelContentHelper.appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
         onPanelRefresh,
         deps,
      });
      bodyEl.appendChild(root);
   }
}
