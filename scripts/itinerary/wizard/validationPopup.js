import { showRemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';
import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
} from './itineraryDiff.js';

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
      onAccept: () => {},
      onDismiss: () => {},
      onViewAlternatives,
   });
}
