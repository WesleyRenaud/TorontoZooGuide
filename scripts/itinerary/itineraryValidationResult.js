import { WizardDiffSummary } from './wizard/diff/wizardDiffSummary.js';
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
         WizardDiffSummary.hasAddedItems(validation.added)
         || WizardDiffSummary.hasRemovedItems(validation.removed)
         || WizardDiffSummary.hasUnscheduledItems(validation.unscheduled)
         || WizardDiffSummary.hasReducedVisibility(validation.reducedVisibility)
         || WizardDiffSummary.hasImprovedVisibility(validation.improvedVisibility)
         || validation.adjustments.length > 0
      );
   }
}
