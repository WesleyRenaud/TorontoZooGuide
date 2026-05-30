import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import {
   makeDayPlannerPreview,
   makeItineraryPanelViews,
} from './components/dayPlanner.js';
import { showScheduleItemModule } from './components/scheduleItemModule.js';
import { makeSection } from './components/section.js';
import { clearItineraryDraftStorage } from '../draftStorage.js';
import {
   getItineraryPanelViewFromUrl,
   setItineraryPanelViewInUrl,
} from './itineraryPanelViewUrl.js';
import {
   clearItinerary,
   getItinerary,
   getZooHours,
   isItineraryEmpty,
   setItineraryArrivalTime,
   setItineraryDepartureTime,
} from '../itineraryService.js';
import { buildSchedulableEventTypes } from './scheduleItemTypes.js';
import { buildSectionConfigs } from './sectionConfigs.js';
import { resolveEffectiveItineraryHoursDateIso } from '../visitDateEarliest.js';

let latestRenderToken = 0;
let activePanelView = getItineraryPanelViewFromUrl();

function destroyRenderedPanelChildren(bodyEl) {
   Array.from(bodyEl?.children ?? []).forEach((child) => {
      child.__tzgCleanup?.();
   });
}

function clearRenderedPanel(bodyEl) {
   destroyRenderedPanelChildren(bodyEl);
   bodyEl?.replaceChildren();
}

async function clearStoredItinerary() {
   try {
      await clearItinerary();
      clearItineraryDraftStorage();
   }
   catch (err) {
      console.error('Failed to clear itinerary:', err);
   }
}

function makePanelViewShell() {
   return makeItineraryPanelViews({
      activeView: activePanelView,
      onViewChange: (view) => {
         activePanelView = view;
         setItineraryPanelViewInUrl(view);
      },
   });
}

function appendDayPlannerViewWithHours(
   dayPlannerView,
   zooHours,
   itinerary = {},
   timeHandlers = {},
   { onPanelRefresh = null } = {}
) {
   dayPlannerView.appendChild(
      makeDayPlannerPreview(zooHours, itinerary, timeHandlers, {
         onScheduleItemClick: () => {
            showScheduleItemModule({
               itinerary,
               eventTypes: buildSchedulableEventTypes(itinerary.itineraryConfig),
               onScheduled: onPanelRefresh,
            });
         },
      })
   );
}

function buildItineraryPanelContent(bodyEl, itinerary, zooHours) {
   const fragment = document.createDocumentFragment();
   const {
      root,
      sharedHeader,
      listView,
      dayPlannerView,
   } = makePanelViewShell();

   sharedHeader.appendChild(
      makeActionsBar({
         onAfterClear: clearStoredItinerary,
      })
   );

   const dateCard = makeDateCard(itinerary);

   if (dateCard) {
      sharedHeader.appendChild(dateCard);
   }

   buildSectionConfigs(itinerary).forEach((sectionConfig) => {
      listView.appendChild(
         makeSection(sectionConfig)
      );
   });

   appendDayPlannerViewWithHours(
      dayPlannerView,
      zooHours,
      itinerary,
      {
         onArrivalTimeChange: async (arrivalTime) => {
            await setItineraryArrivalTime(arrivalTime);
            await renderItineraryPanelInto(bodyEl);
         },
         onDepartureTimeChange: async (departureTime) => {
            await setItineraryDepartureTime(departureTime);
            await renderItineraryPanelInto(bodyEl);
         },
      },
      {
         onPanelRefresh: () => renderItineraryPanelInto(bodyEl),
      }
   );
   fragment.appendChild(root);

   return fragment;
}

function buildEmptyItineraryPanelContent(bodyEl, zooHours) {
   const {
      root,
      listView,
      dayPlannerView,
   } = makePanelViewShell();

   renderBuildOnly(listView);
   renderBuildOnly(dayPlannerView);
   appendDayPlannerViewWithHours(dayPlannerView, zooHours, {}, {}, {
      onPanelRefresh: () => renderItineraryPanelInto(bodyEl),
   });
   bodyEl.appendChild(root);
}

export async function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) {
      return;
   }

   const renderToken = ++latestRenderToken;
   const itinerary = await getItinerary();
   const hoursDate = await resolveEffectiveItineraryHoursDateIso(itinerary);
   const zooHours = await getZooHours(hoursDate);

   if (renderToken !== latestRenderToken) {
      return;
   }

   clearRenderedPanel(bodyEl);

   if (!itinerary || isItineraryEmpty(itinerary)) {
      buildEmptyItineraryPanelContent(bodyEl, zooHours);
      return;
   }

   bodyEl.appendChild(
      buildItineraryPanelContent(bodyEl, itinerary, zooHours)
   );
}
