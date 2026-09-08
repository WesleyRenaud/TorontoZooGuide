import { ItineraryShape } from '../itineraryShape.js';
import { PastItineraryClearer } from './pastItineraryClearer.js';
import { PastItineraryDateRecoverer } from './pastItineraryDateRecoverer.js';
import { PastItineraryPromptTracker } from './pastItineraryPromptTracker.js';
import { ShowPastItineraryChoiceFragment } from './showPastItineraryChoiceFragment.js';
import { VisitDateResolver } from '../visitDateResolver.js';
import { VisitDateValidator } from '../../visitDates/visitDateValidator.js';

/**
 * When a saved itinerary's visit day is no longer selectable, offer to clear it or
 * pick a new date. Returns true when the choice or recovery UI is shown.
 */
export class OfferPastItineraryClearOrRecoverer {
   static async offerPastItineraryClearOrRecovery({
      itinerary,
      mountEl,
      onCleared,
      onRecovered,
      deps = {},
   } = {}) {
      const {
         hasContent = ItineraryShape.hasSavedItineraryContent,
         resolveEarliestVisitDate = VisitDateResolver.resolveEarliestSelectableVisitDateNoon,
         isVisitDateBeforeFloor = VisitDateValidator.isVisitDateBeforeEarliestFloor,
         showChoicePrompt = ShowPastItineraryChoiceFragment.showPastItineraryChoicePrompt,
         clearItinerary = PastItineraryClearer.clearPastItinerary,
         recoverItineraryDate = PastItineraryDateRecoverer.recoverPastItineraryDate,
         isPromptOpen = PastItineraryPromptTracker.isPastItineraryPromptOpen,
         setPromptOpen = PastItineraryPromptTracker.setPastItineraryPromptOpen,
      } = deps;

      if (!mountEl) {
         return false;
      }

      if (isPromptOpen()) {
         return true;
      }

      if (!itinerary || !hasContent(itinerary)) {
         return false;
      }

      const earliestSelectableDate = await resolveEarliestVisitDate(deps);

      if (!isVisitDateBeforeFloor(itinerary.date, earliestSelectableDate)) {
         return false;
      }

      setPromptOpen(true);

      const showChoice = () => {
         showChoicePrompt({
            mountEl,
            onClear: () => {
               setPromptOpen(false);
               void clearItinerary(deps).then(() => {
                  onCleared?.();
               });
            },
            onRecover: () => {
               recoverItineraryDate({
                  mountEl,
                  itinerary,
                  earliestSelectableDate,
                  onComplete: (savedItinerary) => {
                     setPromptOpen(false);
                     onRecovered?.(savedItinerary);
                  },
                  onCancel: showChoice,
                  deps,
               });
            },
            deps,
         });
      };

      showChoice();
      return true;
   }
}
