import { showRemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';
import {
   hasAddedItems,
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
   const added = pendingValidation?.added ?? null;
   const reducedVisibility = pendingValidation?.reducedVisibility ?? null;
   const improvedVisibility = pendingValidation?.improvedVisibility ?? null;
   const adjustments = pendingValidation?.adjustments ?? null;
   const isEmptyItinerary = pendingValidation?.isEmptyItinerary ?? false;

   if (
      !hasRemovedItems(removed) &&
      !hasAddedItems(added) &&
      !hasReducedVisibility(reducedVisibility) &&
      !hasImprovedVisibility(improvedVisibility) &&
      !adjustments?.length
   ) {
      return;
   }

   showRemovedItemsPopup({
      mountEl,
      added,
      removed,
      reducedVisibility,
      improvedVisibility,
      adjustments,
      isEmptyItinerary,
      onAccept: ({ animalsToKeep = [], attractionsToKeep = [] } = {}) => {
         void acceptItinerary({ animalsToKeep, attractionsToKeep });
      },
      onDismiss: () => {},
      onViewAlternatives,
   });
}
