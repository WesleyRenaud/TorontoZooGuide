import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
   mergeRemovedValidationState,
} from './wizard/itineraryDiff.js';

export function applyItineraryDiffToValidation(
   normalizedItinerary,
   diff,
   { adjustments = [] } = {},
) {
   const validation = normalizedItinerary.validation;

   validation.unscheduled = diff.unscheduled;
   validation.removed = mergeRemovedValidationState(
      validation.removed,
      diff.removed);
   validation.adjustments = adjustments;
   validation.hasChanges = (
      hasAddedItems(validation.added)
      || hasRemovedItems(validation.removed)
      || hasUnscheduledItems(validation.unscheduled)
      || hasReducedVisibility(validation.reducedVisibility)
      || hasImprovedVisibility(validation.improvedVisibility)
      || validation.adjustments.length > 0
   );
}
