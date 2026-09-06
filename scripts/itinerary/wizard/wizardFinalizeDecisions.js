import { ItineraryService } from '../itineraryService.js';

export class WizardFinalizeDecisions {
   static shouldBlockEmptyFinish(
      finalItinerary,
      allowEmpty = false,
      isEmpty = ItineraryService.isItineraryEmpty
   ) {
      return !allowEmpty && isEmpty(finalItinerary);
   }

   static shouldShowSaveIssuesPopup(savedItinerary) {
      return Boolean(savedItinerary?.saveIssues?.length);
   }
}
