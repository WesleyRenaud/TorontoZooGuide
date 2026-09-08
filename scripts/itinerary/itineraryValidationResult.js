import { WizardDiffPresenter } from './wizard/diff/wizardDiffPresenter.js';
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
         WizardDiffPresenter.hasAddedItems(validation.added)
         || WizardDiffPresenter.hasRemovedItems(validation.removed)
         || WizardDiffPresenter.hasUnscheduledItems(validation.unscheduled)
         || WizardDiffPresenter.hasReducedVisibility(validation.reducedVisibility)
         || WizardDiffPresenter.hasImprovedVisibility(validation.improvedVisibility)
         || validation.adjustments.length > 0
      );
   }
}
