import { clearItineraryDraftStorage } from '../draftStorage.js';
import {
   buildEmptyItineraryPanelContent,
   buildItineraryPanelContent,
   clearRenderedPanel,
} from './itineraryPanelContent.js';
import {
   clearItinerary,
   getItinerary,
   getZooHours,
} from '../itineraryService.js';
import { isItineraryCompletelyUnset } from '../itineraryShape.js';
import { resolveEffectiveItineraryHoursDateIso } from '../visitDateEarliest.js';

let latestRenderToken = 0;

export async function clearStoredItinerary(deps = {}) {
   const {
      clearSavedItinerary = clearItinerary,
      clearDraftStorage = clearItineraryDraftStorage,
   } = deps;

   try {
      await clearSavedItinerary();
      clearDraftStorage();
   }
   catch (err) {
      console.error('Failed to clear itinerary:', err);
   }
}

export async function renderItineraryPanelInto(
   bodyEl,
   deps = {}
) {
   if (!bodyEl) {
      return;
   }

   const {
      loadItinerary = getItinerary,
      resolveHoursDate = resolveEffectiveItineraryHoursDateIso,
      loadZooHours = getZooHours,
      itineraryIsEmpty = isItineraryCompletelyUnset,
      buildContent = buildItineraryPanelContent,
      buildEmptyContent = buildEmptyItineraryPanelContent,
      clearPanel = clearRenderedPanel,
      onAfterClear = clearStoredItinerary,
   } = deps;

   const renderToken = ++latestRenderToken;
   const itinerary = await loadItinerary();
   const hoursDate = await resolveHoursDate(itinerary);
   const zooHours = await loadZooHours(hoursDate);

   if (renderToken !== latestRenderToken) {
      return;
   }

   clearPanel(bodyEl);

   const refreshPanel = () => renderItineraryPanelInto(bodyEl, deps);
   const contentDeps = {
      onAfterClear,
      ...deps,
   };

   if (!itinerary || itineraryIsEmpty(itinerary)) {
      buildEmptyContent(bodyEl, zooHours, {
         onPanelRefresh: refreshPanel,
         deps: contentDeps,
      });
      return;
   }

   bodyEl.appendChild(
      buildContent(itinerary, zooHours, {
         onPanelRefresh: refreshPanel,
         deps: contentDeps,
      })
   );
}
