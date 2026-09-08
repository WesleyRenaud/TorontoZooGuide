import { WizardDiffPresenter } from './diff/wizardDiffPresenter.js';
import { RemovedItemsFragment } from '../../itinerary/panel/components/removedItemsFragment.js';
import { ItineraryService } from '../itineraryService.js';

export class ValidationFragment {
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
         !WizardDiffPresenter.hasRemovedItems(removed) &&
         !WizardDiffPresenter.hasUnscheduledItems(unscheduled) &&
         !WizardDiffPresenter.hasAddedItems(added) &&
         !WizardDiffPresenter.hasReducedVisibility(reducedVisibility) &&
         !WizardDiffPresenter.hasImprovedVisibility(improvedVisibility) &&
         !adjustments?.length
      ) {
         return;
      }

      RemovedItemsFragment.showRemovedItemsPopup({
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
