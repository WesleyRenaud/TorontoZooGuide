import { WizardDiffSummary } from './diff/wizardDiffSummary.js';
import { RemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';
import { ItineraryService } from '../itineraryService.js';

export class ValidationPopup {
   static showWizardValidationPopupIfNeeded({
      mountEl,
      pendingValidation,
      onViewAlternatives,
   } = {}) {
      const removed = pendingValidation?.removed ?? null;
      const unscheduled = pendingValidation?.unscheduled ?? null;
      const added = pendingValidation?.added ?? null;
      const reducedVisibility = pendingValidation?.reducedVisibility ?? null;
      const improvedVisibility = pendingValidation?.improvedVisibility ?? null;
      const adjustments = pendingValidation?.adjustments ?? null;
      const isEmptyItinerary = pendingValidation?.isEmptyItinerary ?? false;

      if (
         !WizardDiffSummary.hasRemovedItems(removed) &&
         !WizardDiffSummary.hasUnscheduledItems(unscheduled) &&
         !WizardDiffSummary.hasAddedItems(added) &&
         !WizardDiffSummary.hasReducedVisibility(reducedVisibility) &&
         !WizardDiffSummary.hasImprovedVisibility(improvedVisibility) &&
         !adjustments?.length
      ) {
         return;
      }

      RemovedItemsPopup.showRemovedItemsPopup({
         mountEl,
         added,
         removed,
         unscheduled,
         reducedVisibility,
         improvedVisibility,
         adjustments,
         isEmptyItinerary,
         onAccept: ({ animalsToKeep = [], attractionsToKeep = [] } = {}) => {
            void ItineraryService.acceptItinerary({ animalsToKeep, attractionsToKeep });
         },
         onDismiss: () => {},
         onViewAlternatives,
      });
   }
}
