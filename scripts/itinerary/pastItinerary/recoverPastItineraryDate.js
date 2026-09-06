import { ItineraryServiceSave } from '../itineraryServiceSave.js';
import { ItineraryShape } from '../itineraryShape.js';
import { DateSelector } from '../selectors/dateSelector.js';
import { Strings } from '../../strings.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export class RecoverPastItineraryDate {
   static recoverPastItineraryDate({
      mountEl,
      itinerary,
      earliestSelectableDate,
      onComplete,
      onCancel,
      deps = {},
   } = {}) {
      const {
         createDateController = DateSelector.createItineraryDateSelectorController,
         saveItineraryFn = ItineraryServiceSave.saveItinerary,
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
         titleText: Strings.itinerary.stale.recoveryTitle,
         subtitleText: Strings.itinerary.stale.recoverySubtitle,
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
}
