import { showRemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';
import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
} from './itineraryDiff.js';
import { acceptItinerary } from '../itineraryService.js';

export function showWizardValidationPopupIfNeeded({
   mountEl,
   pendingValidation,
   onViewAlternatives,
} = {}) {
   const removed = pendingValidation?.removed ?? null;
   const reducedVisibility = pendingValidation?.reducedVisibility ?? null;
   const improvedVisibility = pendingValidation?.improvedVisibility ?? null;
   const isEmptyItinerary = pendingValidation?.isEmptyItinerary ?? false;

   if (
      !hasRemovedItems(removed) &&
      !hasReducedVisibility(reducedVisibility) &&
      !hasImprovedVisibility(improvedVisibility)
   ) {
      return;
   }

   showRemovedItemsPopup({
      mountEl,
      removed,
      reducedVisibility,
      improvedVisibility,
      isEmptyItinerary,
      onAccept: () => {
         void acceptItinerary();
      },
      onDismiss: () => {},
      onViewAlternatives,
   });
}
