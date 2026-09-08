import { WizardDiffSummaryHelpers } from './wizardDiffSummaryHelpers.js';

export class WizardDiffSummary {
   static hasRemovedItems(removed) {
      if (!removed || typeof removed !== 'object') {
         return false;
      }

      return (
         WizardDiffSummaryHelpers.hasItems(removed.animals) ||
         WizardDiffSummaryHelpers.hasItems(removed.attractions) ||
         WizardDiffSummaryHelpers.hasItems(removed.guardiansTalks) ||
         WizardDiffSummaryHelpers.hasItems(removed.wildEncounters)
      );
   }

   static hasAddedItems(added) {
      if (!added || typeof added !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelpers.hasItems(added.animals);
   }

   static hasReducedVisibility(reducedVisibility) {
      if (!reducedVisibility || typeof reducedVisibility !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelpers.hasItems(reducedVisibility.animals);
   }

   static hasImprovedVisibility(improvedVisibility) {
      if (!improvedVisibility || typeof improvedVisibility !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelpers.hasItems(improvedVisibility.animals);
   }

   static hasUnscheduledItems(unscheduled) {
      if (!unscheduled || typeof unscheduled !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelpers.hasItems(unscheduled.animals)
         || WizardDiffSummaryHelpers.hasItems(unscheduled.attractions);
   }

   static isValidatedItineraryEmpty(validated) {
      if (!validated || typeof validated !== 'object') {
         return true;
      }

      return (
         !WizardDiffSummaryHelpers.hasItems(validated.animals) &&
         !WizardDiffSummaryHelpers.hasItems(validated.attractions) &&
         !WizardDiffSummaryHelpers.hasItems(validated.guardiansTalks) &&
         !WizardDiffSummaryHelpers.hasItems(validated.wildEncounters) &&
         !WizardDiffSummaryHelpers.hasItems(validated.transportations)
      );
   }
}
