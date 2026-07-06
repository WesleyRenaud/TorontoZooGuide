import { clearPastItinerary } from './clearPastItinerary.js';
import { hasSavedItineraryContent } from '../itineraryShape.js';
import {
   isPastItineraryPromptOpen,
   setPastItineraryPromptOpen,
} from './promptSession.js';
import { recoverPastItineraryDate } from './recoverPastItineraryDate.js';
import { showPastItineraryChoicePrompt } from './showPastItineraryChoicePrompt.js';
import { resolveEarliestSelectableVisitDateNoon } from '../visitDateEarliest.js';
import { isVisitDateBeforeEarliestFloor } from '../../visitDates/visitDateRules.js';

/**
 * When a saved itinerary's visit day is no longer selectable, offer to clear it or
 * pick a new date. Returns true when the choice or recovery UI is shown.
 */
export async function offerPastItineraryClearOrRecovery({
   itinerary,
   mountEl,
   onCleared,
   onRecovered,
   deps = {},
} = {}) {
   const {
      hasContent = hasSavedItineraryContent,
      resolveEarliestVisitDate = resolveEarliestSelectableVisitDateNoon,
      isVisitDateBeforeFloor = isVisitDateBeforeEarliestFloor,
      showChoicePrompt = showPastItineraryChoicePrompt,
      clearItinerary = clearPastItinerary,
      recoverItineraryDate = recoverPastItineraryDate,
      isPromptOpen = isPastItineraryPromptOpen,
      setPromptOpen = setPastItineraryPromptOpen,
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
