import { ItineraryValidationVisibility } from './itineraryValidationVisibility.js';
import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';
import { WizardDiffSummary } from './wizard/diff/wizardDiffSummary.js';

export class ItineraryValidation {
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
      const visibilityAnimals = ItineraryValidationVisibility.aggregateAnimalsForVisibilityComparison(
         itinerary.animals
      );
      const removed = {
         animals: ItineraryValidationVisibility.buildRemovedAnimals(visibilityAnimals, animalMinLikelihood),
         attractions: ItineraryValidationVisibility.buildRemovedAttractions(
            itinerary.attractions,
            animalMinLikelihood
         ),
         guardiansTalks: ItineraryValidationVisibility.buildRemovedScheduledItems(itinerary.guardiansTalks),
         wildEncounters: ItineraryValidationVisibility.buildRemovedScheduledItems(itinerary.wildEncounters),
      };
      const added = {
         animals: ItineraryValidationVisibility.buildAddedAnimals(itinerary.animals),
      };
      const reducedVisibility = {
         animals: ItineraryValidationVisibility.buildReducedVisibilityAnimals(
            visibilityAnimals,
            visibilityChangeThreshold,
            animalMinLikelihood
         ),
      };
      const improvedVisibility = {
         animals: ItineraryValidationVisibility.buildImprovedVisibilityAnimals(
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
            WizardDiffSummary.hasAddedItems(added)
            || WizardDiffSummary.hasRemovedItems(removed)
            || WizardDiffSummary.hasUnscheduledItems(unscheduled)
            || WizardDiffSummary.hasReducedVisibility(reducedVisibility)
            || WizardDiffSummary.hasImprovedVisibility(improvedVisibility)
         ),
      };
   }
}
