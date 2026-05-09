import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import {
   ITINERARY_PANEL_VIEWS,
   makeDayPlannerPreview,
   makeItineraryPanelViews,
} from './components/dayPlanner.js';
import { makeSection } from './components/section.js';
import {
   clearItineraryDraftStorage,
   getStoredItineraryDate,
} from '../draftStorage.js';
import {
   clearItinerary,
   getItinerary,
   getZooHours,
   isItineraryEmpty,
} from '../itineraryService.js';
import { buildSectionConfigs } from './sectionConfigs.js';

let latestRenderToken = 0;
let activePanelView = ITINERARY_PANEL_VIEWS.list;

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
      },
   });
}

function appendDayPlannerViewWithHours(dayPlannerView, zooHours, itinerary = {}) {
   dayPlannerView.appendChild(makeDayPlannerPreview(zooHours, itinerary));
}

function getDayPlannerDate(itinerary) {
   return itinerary?.date || getStoredItineraryDate();
}

function buildItineraryPanelContent(itinerary, zooHours) {
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

   appendDayPlannerViewWithHours(dayPlannerView, zooHours, itinerary);
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
   appendDayPlannerViewWithHours(dayPlannerView, zooHours);
   bodyEl.appendChild(root);
}

export async function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) {
      return;
   }

   const renderToken = ++latestRenderToken;
   const itinerary = await getItinerary();
   const zooHours = await getZooHours(getDayPlannerDate(itinerary));

   if (renderToken !== latestRenderToken) {
      return;
   }

   clearRenderedPanel(bodyEl);

   if (!itinerary || isItineraryEmpty(itinerary)) {
      buildEmptyItineraryPanelContent(bodyEl, zooHours);
      return;
   }

   bodyEl.appendChild(
      buildItineraryPanelContent(itinerary, zooHours)
   );
}
