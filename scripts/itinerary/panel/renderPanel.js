import { DraftStorage } from '../draftStorage.js';
import { ItineraryPanelContent } from './itineraryPanelContent.js';
import { ItineraryService } from '../itineraryService.js';
import { ItineraryShape } from '../itineraryShape.js';
import { VisitDateEarliest } from '../visitDateEarliest.js';

let latestRenderToken = 0;

export class RenderPanel {
   static async clearStoredItinerary(deps = {}) {
      const {
         clearSavedItinerary = ItineraryService.clearItinerary,
         clearDraftStorage = DraftStorage.clearItineraryDraftStorage,
      } = deps;

      try {
         await clearSavedItinerary();
         clearDraftStorage();
      }
      catch (err) {
         console.error('Failed to clear itinerary:', err);
      }
   }

   static async renderItineraryPanelInto(
   bodyEl,
   deps = {}
) {
      if (!bodyEl) {
         return;
      }

      const {
         loadItinerary = ItineraryService.getItinerary,
         resolveHoursDate = VisitDateEarliest.resolveEffectiveItineraryHoursDateIso,
         loadZooHours = ItineraryService.getZooHours,
         itineraryIsEmpty = ItineraryShape.isItineraryCompletelyUnset,
         buildContent = ItineraryPanelContent.buildItineraryPanelContent,
         buildEmptyContent = ItineraryPanelContent.buildEmptyItineraryPanelContent,
         clearPanel = ItineraryPanelContent.clearRenderedPanel,
         onAfterClear = RenderPanel.clearStoredItinerary,
      } = deps;

      const renderToken = ++latestRenderToken;
      const itinerary = await loadItinerary();
      const hoursDate = await resolveHoursDate(itinerary);
      const zooHours = await loadZooHours(hoursDate);

      if (renderToken !== latestRenderToken) {
         return;
      }

      clearPanel(bodyEl);

      const refreshPanel = () => RenderPanel.renderItineraryPanelInto(bodyEl, deps);
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
}
