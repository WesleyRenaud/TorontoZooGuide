import { DraftStore } from '../draftStore.js';
import { ItineraryPanelContentView } from './itineraryPanelContentView.js';
import { ItineraryService } from '../itineraryService.js';
import { ItineraryShape } from '../itineraryShape.js';
import { VisitDateResolver } from '../visitDateResolver.js';

export class RenderView {
   static latestRenderToken = 0;

   static async clearStoredItinerary(deps = {}) {
      const {
         clearSavedItinerary = ItineraryService.clearItinerary,
         clearDraftStorage = DraftStore.clearItineraryDraftStorage,
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
         resolveHoursDate = VisitDateResolver.resolveEffectiveItineraryHoursDateIso,
         loadZooHours = ItineraryService.getZooHours,
         itineraryIsEmpty = ItineraryShape.isItineraryCompletelyUnset,
         buildContent = ItineraryPanelContentView.buildItineraryPanelContent,
         buildEmptyContent = ItineraryPanelContentView.buildEmptyItineraryPanelContent,
         clearPanel = ItineraryPanelContentView.clearRenderedPanel,
         onAfterClear = RenderView.clearStoredItinerary,
      } = deps;

      const renderToken = ++RenderView.latestRenderToken;
      const itinerary = await loadItinerary();
      const hoursDate = await resolveHoursDate(itinerary);
      const zooHours = await loadZooHours(hoursDate);

      if (renderToken !== RenderView.latestRenderToken) {
         return;
      }

      clearPanel(bodyEl);

      const refreshPanel = () => RenderView.renderItineraryPanelInto(bodyEl, deps);
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
