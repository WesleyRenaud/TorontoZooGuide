import {
   hasBulkScheduleAnimalsNotEnoughTimeIssue,
   showBulkScheduleAnimalsNotEnoughTimeNotice,
} from './bulkScheduleAnimalsNotEnoughTimeConfirmation.js';
import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import { makeDayPlannerPreview } from './components/dayPlanner.js';
import { makeSection } from './components/section.js';
import {
   buildItineraryPanelScheduleHandlers,
   openScheduleItemModule,
} from './itineraryPanelScheduleHandlers.js';
import { makeItineraryPanelViewShell } from './itineraryPanelViewState.js';
import { bulkScheduleAnimals } from '../itineraryService.js';
import {
   setItineraryArrivalTime,
   setItineraryDepartureTime,
} from '../itineraryServiceTime.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';
import { buildSectionConfigs } from './sectionConfigs.js';
import { showScheduleItemNotice } from './showScheduleItemNotice.js';
import { APP_STRINGS } from '../../strings.js';

export function destroyRenderedPanelChildren(bodyEl) {
   Array.from(bodyEl?.children ?? []).forEach((child) => {
      child.__tzgCleanup?.();
   });
}

export function clearRenderedPanel(bodyEl) {
   destroyRenderedPanelChildren(bodyEl);
   bodyEl?.replaceChildren();
}

function appendDayPlannerViewWithHours(
   dayPlannerView,
   zooHours,
   itinerary = {},
   timeHandlers = {},
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      openModule = openScheduleItemModule,
      bulkSchedule = bulkScheduleAnimals,
      hasNotEnoughTimeIssue = hasBulkScheduleAnimalsNotEnoughTimeIssue,
      showNotEnoughTimeNotice = showBulkScheduleAnimalsNotEnoughTimeNotice,
      showNotice = showScheduleItemNotice,
      buildEventTypes = buildSchedulableEventTypes,
      buildScheduleHandlers = buildItineraryPanelScheduleHandlers,
      makeDayPlanner = makeDayPlannerPreview,
      genericErrorMessage = APP_STRINGS.itinerary.errors.generic,
   } = deps;

   const scheduleHandlers = buildScheduleHandlers(itinerary, {
      onPanelRefresh,
      deps,
   });

   dayPlannerView.appendChild(
      makeDayPlanner(zooHours, itinerary, timeHandlers, {
         onScheduleItemClick: () => {
            openModule({
               itinerary,
               eventTypes: buildEventTypes(itinerary.itineraryConfig),
               onScheduled: onPanelRefresh,
            }, deps);
         },
         onBulkScheduleAnimalsClick: async () => {
            try {
               const { issues } = await bulkSchedule();

               if (typeof onPanelRefresh === 'function') {
                  await onPanelRefresh();
               }

               if (hasNotEnoughTimeIssue(issues)) {
                  showNotEnoughTimeNotice();
               }
            }
            catch (err) {
               console.error('Failed to bulk schedule animals:', err);
               showNotice(err?.message || genericErrorMessage);
            }
         },
         scheduleHandlers,
      })
   );
}

export function buildItineraryPanelContent(
   itinerary,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      makeViewShell = makeItineraryPanelViewShell,
      makeActions = makeActionsBar,
      createDateCard = makeDateCard,
      buildSections = buildSectionConfigs,
      createSection = makeSection,
      buildScheduleHandlers = buildItineraryPanelScheduleHandlers,
      onAfterClear = null,
      setArrivalTime = setItineraryArrivalTime,
      setDepartureTime = setItineraryDepartureTime,
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

   appendDayPlannerViewWithHours(
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

export function buildEmptyItineraryPanelContent(
   bodyEl,
   zooHours,
   {
      onPanelRefresh = null,
      deps = {},
   } = {}
) {
   const {
      makeViewShell = makeItineraryPanelViewShell,
      renderEmptyState = renderBuildOnly,
   } = deps;

   const {
      root,
      listView,
      dayPlannerView,
   } = makeViewShell();

   renderEmptyState(listView);
   renderEmptyState(dayPlannerView);
   appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
      onPanelRefresh,
      deps,
   });
   bodyEl.appendChild(root);
}
