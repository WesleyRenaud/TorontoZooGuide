import { WizardDiffSummaryHelper } from './wizardDiffSummaryHelper.js';

export class WizardDiffPresenter {
   static hasRemovedItems(removed) {
      if (!removed || typeof removed !== 'object') {
         return false;
      }

      return (
         WizardDiffSummaryHelper.hasItems(removed.animals) ||
         WizardDiffSummaryHelper.hasItems(removed.attractions) ||
         WizardDiffSummaryHelper.hasItems(removed.guardiansTalks) ||
         WizardDiffSummaryHelper.hasItems(removed.wildEncounters)
      );
   }

   static hasAddedItems(added) {
      if (!added || typeof added !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelper.hasItems(added.animals);
   }

   static hasReducedVisibility(reducedVisibility) {
      if (!reducedVisibility || typeof reducedVisibility !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelper.hasItems(reducedVisibility.animals);
   }

   static hasImprovedVisibility(improvedVisibility) {
      if (!improvedVisibility || typeof improvedVisibility !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelper.hasItems(improvedVisibility.animals);
   }

   static hasUnscheduledItems(unscheduled) {
      if (!unscheduled || typeof unscheduled !== 'object') {
         return false;
      }

      return WizardDiffSummaryHelper.hasItems(unscheduled.animals)
         || WizardDiffSummaryHelper.hasItems(unscheduled.attractions);
   }

   static isValidatedItineraryEmpty(validated) {
      if (!validated || typeof validated !== 'object') {
         return true;
      }

      return (
         !WizardDiffSummaryHelper.hasItems(validated.animals) &&
         !WizardDiffSummaryHelper.hasItems(validated.attractions) &&
         !WizardDiffSummaryHelper.hasItems(validated.guardiansTalks) &&
         !WizardDiffSummaryHelper.hasItems(validated.wildEncounters) &&
         !WizardDiffSummaryHelper.hasItems(validated.transportations)
      );
   }
}
