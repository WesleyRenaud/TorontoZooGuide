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
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';
import { APP_STRINGS } from '../../strings.js';

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

function buildSectionConfigs({
   animals = [],
   attractions = [],
   guardiansTalks = [],
   wildEncounters = [],
} = {}) {
   return [
      {
         title: APP_STRINGS.site.nav.animals,
         count: animals.length,
         children: buildAnimalRows(animals),
         stepKey: 'animals',
      },
      {
         title: APP_STRINGS.map.filter.attractions,
         count: attractions.length,
         children: buildAttractionRows(attractions),
         stepKey: 'attractions',
      },
      {
         title: APP_STRINGS.site.nav.meetTheGuardians,
         count: guardiansTalks.length,
         children: buildGuardiansRows(guardiansTalks),
         stepKey: 'guardiansTalks',
      },
      {
         title: APP_STRINGS.site.nav.wildEncounters,
         count: wildEncounters.length,
         children: buildWildRows(wildEncounters),
         stepKey: 'wildEncounters',
      },
   ];
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
      listView,
      dayPlannerView,
   } = makePanelViewShell();

   listView.appendChild(
      makeActionsBar({
         onAfterClear: clearStoredItinerary,
      })
   );

   const dateCard = makeDateCard(itinerary);

   if (dateCard) {
      listView.appendChild(dateCard);
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
