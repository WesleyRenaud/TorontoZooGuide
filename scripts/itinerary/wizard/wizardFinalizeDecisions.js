import { isItineraryEmpty } from '../itineraryService.js';

export function shouldBlockEmptyFinish(
   finalItinerary,
   allowEmpty = false,
   isEmpty = isItineraryEmpty
) {
   return !allowEmpty && isEmpty(finalItinerary);
}

export function shouldShowSaveIssuesPopup(savedItinerary) {
   return Boolean(savedItinerary?.saveIssues?.length);
}
