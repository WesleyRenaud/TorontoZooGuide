import { Summary } from './wizard/diff/summary.js';
import { ItineraryDiff } from './wizard/itineraryDiff.js';

export class ItineraryValidationResult {
   static applyItineraryDiffToValidation(
      normalizedItinerary,
      diff,
      { adjustments = [] } = {},
   ) {
      const validation = normalizedItinerary.validation;

      validation.unscheduled = diff.unscheduled;
      validation.removed = ItineraryDiff.mergeRemovedValidationState(
         validation.removed,
         diff.removed);
      validation.adjustments = adjustments;
      validation.hasChanges = (
         Summary.hasAddedItems(validation.added)
         || Summary.hasRemovedItems(validation.removed)
         || Summary.hasUnscheduledItems(validation.unscheduled)
         || Summary.hasReducedVisibility(validation.reducedVisibility)
         || Summary.hasImprovedVisibility(validation.improvedVisibility)
         || validation.adjustments.length > 0
      );
   }
}
