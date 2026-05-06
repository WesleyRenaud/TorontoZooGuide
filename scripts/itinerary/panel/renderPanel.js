import { makeActionsBar } from './components/actionsBar.js';
import { renderBuildOnly } from './components/buildOnly.js';
import { makeDateCard } from './components/dateCard.js';
import { makeSection } from './components/section.js';
import { clearItineraryDraftStorage } from '../draftStorage.js';
import {
   clearItinerary,
   getItinerary,
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

function buildItineraryPanelContent(itinerary) {
   const fragment = document.createDocumentFragment();

   fragment.appendChild(
      makeActionsBar({
         onAfterClear: clearStoredItinerary,
      })
   );

   const dateCard = makeDateCard(itinerary);

   if (dateCard) {
      fragment.appendChild(dateCard);
   }

   buildSectionConfigs(itinerary).forEach((sectionConfig) => {
      fragment.appendChild(
         makeSection(sectionConfig)
      );
   });

   return fragment;
}

export async function renderItineraryPanelInto(bodyEl) {
   if (!bodyEl) {
      return;
   }

   const renderToken = ++latestRenderToken;
   const itinerary = await getItinerary();

   if (renderToken !== latestRenderToken) {
      return;
   }

   clearRenderedPanel(bodyEl);

   if (!itinerary || isItineraryEmpty(itinerary)) {
      renderBuildOnly(bodyEl);
      return;
   }

   bodyEl.appendChild(
      buildItineraryPanelContent(itinerary)
   );
}
