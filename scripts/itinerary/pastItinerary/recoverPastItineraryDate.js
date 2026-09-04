import { saveItinerary } from '../itineraryServiceSave.js';
import { ItineraryShape } from '../itineraryShape.js';
import { createItineraryDateSelectorController } from '../selectors/dateSelector.js';
import { APP_STRINGS } from '../../strings.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export function recoverPastItineraryDate({
   mountEl,
   itinerary,
   earliestSelectableDate,
   onComplete,
   onCancel,
   deps = {},
} = {}) {
   const {
      createDateController = createItineraryDateSelectorController,
      saveItineraryFn = saveItinerary,
      normalizeDraft = ItineraryShape.normalizeItineraryDraft,
      toIso = VisitDateRules.toISODate,
   } = deps;

   if (!mountEl || !itinerary) {
      return null;
   }

   const initialDate = earliestSelectableDate ?? null;

   const dateController = createDateController({
      mountEl,
      initialDate,
      earliestSelectableDate: initialDate,
      hideNextButton: true,
      titleText: APP_STRINGS.itinerary.stale.recoveryTitle,
      subtitleText: APP_STRINGS.itinerary.stale.recoverySubtitle,
      onClose: () => {
         dateController.hide();
         onCancel?.();
      },
      onFinish: async (dateIso) => {
         const savedItinerary = await saveItineraryFn({
            ...normalizeDraft(itinerary),
            date: typeof dateIso === 'string' ? dateIso : toIso(dateIso),
         }, {
            selectedExhibits: Array.isArray(itinerary.selectedExhibits)
               ? itinerary.selectedExhibits
               : [],
         });

         if (!savedItinerary) {
            return;
         }

         dateController.hide();
         onComplete?.(savedItinerary);
      },
   });

   dateController.show();

   return dateController;
}
