import { ItineraryValidationPresenter } from './itineraryValidationPresenter.js';
import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';
import { WizardDiffPresenter } from './wizard/diff/wizardDiffPresenter.js';

export class ItineraryValidator {
   static buildItineraryValidationState(
      itinerary = {},
      {
         animalVisibilityChangeThreshold,
         itineraryAnimalMinLikelihood,
      } = {}
   ) {
      const visibilityChangeThreshold = ItineraryItemFormatter.normalizeNonNegativeNumber(
         animalVisibilityChangeThreshold
      );
      const animalMinLikelihood = ItineraryItemFormatter.normalizeNonNegativeNumber(
         itineraryAnimalMinLikelihood
      );
      const visibilityAnimals = ItineraryValidationPresenter.aggregateAnimalsForVisibilityComparison(
         itinerary.animals
      );
      const removed = {
         animals: ItineraryValidationPresenter.buildRemovedAnimals(visibilityAnimals, animalMinLikelihood),
         attractions: ItineraryValidationPresenter.buildRemovedAttractions(
            itinerary.attractions,
            animalMinLikelihood
         ),
         guardiansTalks: ItineraryValidationPresenter.buildRemovedScheduledItems(itinerary.guardiansTalks),
         wildEncounters: ItineraryValidationPresenter.buildRemovedScheduledItems(itinerary.wildEncounters),
      };
      const added = {
         animals: ItineraryValidationPresenter.buildAddedAnimals(itinerary.animals),
      };
      const reducedVisibility = {
         animals: ItineraryValidationPresenter.buildReducedVisibilityAnimals(
            visibilityAnimals,
            visibilityChangeThreshold,
            animalMinLikelihood
         ),
      };
      const improvedVisibility = {
         animals: ItineraryValidationPresenter.buildImprovedVisibilityAnimals(
            visibilityAnimals,
            visibilityChangeThreshold
         ),
      };
      const unscheduled = {
         animals: [],
         attractions: [],
      };

      return {
         removed,
         unscheduled,
         added,
         reducedVisibility,
         improvedVisibility,
         adjustments: [],
         hasChanges: (
            WizardDiffPresenter.hasAddedItems(added)
            || WizardDiffPresenter.hasRemovedItems(removed)
            || WizardDiffPresenter.hasUnscheduledItems(unscheduled)
            || WizardDiffPresenter.hasReducedVisibility(reducedVisibility)
            || WizardDiffPresenter.hasImprovedVisibility(improvedVisibility)
         ),
      };
   }
}
