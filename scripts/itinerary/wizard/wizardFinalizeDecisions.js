import { isItineraryEmpty } from '../itineraryService.js';

export class WizardFinalizeDecisions {
   static shouldBlockEmptyFinish(
      finalItinerary,
      allowEmpty = false,
      isEmpty = isItineraryEmpty
   ) {
      return !allowEmpty && isEmpty(finalItinerary);
   }

   static shouldShowSaveIssuesPopup(savedItinerary) {
      return Boolean(savedItinerary?.saveIssues?.length);
   }
}
