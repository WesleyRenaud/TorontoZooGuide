import { WizardDiffPresenter } from './diff/wizardDiffPresenter.js';
import { DraftStore } from '../draftStore.js';
import { ItineraryShape } from '../itineraryShape.js';

export class ItineraryWizardDraftMutator {
   static createPendingValidationState() {
      return {
         pendingRemovedItems: null,
         pendingUnscheduledItems: null,
         pendingReducedVisibility: null,
         pendingImprovedVisibility: null,
         pendingValidatedEmpty: false,
      };
   }

   static buildWizardDraftSnapshot(state = {}) {
      return ItineraryShape.cloneItineraryDraft(state);
   }

   static writeDraftState(draft) {
      DraftStore.writeStoredItineraryDraft(draft);
   }

   static assignWizardDraft(state, draft) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

      state.date = normalizedDraft.date;
      state.animals = normalizedDraft.animals.slice();
      state.attractions = normalizedDraft.attractions.slice();
      state.guardiansTalks = normalizedDraft.guardiansTalks.slice();
      state.wildEncounters = normalizedDraft.wildEncounters.slice();
      state.transportations = normalizedDraft.transportations.slice();
      state.transportationStations = normalizedDraft.transportationStations.slice();
   }

   static resetPendingValidation(state) {
      state.pendingRemovedItems = null;
      state.pendingUnscheduledItems = null;
      state.pendingReducedVisibility = null;
      state.pendingImprovedVisibility = null;
      state.pendingValidatedEmpty = false;
   }

   static consumePendingValidationState(state) {
      const pendingValidation = {
         removed: state.pendingRemovedItems,
         unscheduled: state.pendingUnscheduledItems,
         reducedVisibility: state.pendingReducedVisibility,
         improvedVisibility: state.pendingImprovedVisibility,
         isEmptyItinerary: state.pendingValidatedEmpty,
      };

      ItineraryWizardDraftMutator.resetPendingValidation(state);
      return pendingValidation;
   }

   static applySelectionUpdate(state, key, value, { preserveOnInvalid = false } = {}) {
      if (value == null) {
         if (preserveOnInvalid) {
            return false;
         }

         state[key] = [];
         return true;
      }

      state[key] = value.slice();
      return true;
   }

   static applyPendingValidation(state, {
      removed = null,
      unscheduled = null,
      reducedVisibility = null,
      improvedVisibility = null,
      validated = null,
   } = {}) {
      if (validated) {
         ItineraryWizardDraftMutator.assignWizardDraft(state, {
            ...ItineraryWizardDraftMutator.buildWizardDraftSnapshot(state),
            ...validated,
         });
      }

      state.pendingRemovedItems = WizardDiffPresenter.hasRemovedItems(removed) ? removed : null;
      state.pendingUnscheduledItems = WizardDiffPresenter.hasUnscheduledItems(unscheduled) ? unscheduled : null;
      state.pendingReducedVisibility = WizardDiffPresenter.hasReducedVisibility(reducedVisibility) ? reducedVisibility : null;
      state.pendingImprovedVisibility = WizardDiffPresenter.hasImprovedVisibility(improvedVisibility) ? improvedVisibility : null;
      state.pendingValidatedEmpty = validated != null
         ? WizardDiffPresenter.isValidatedItineraryEmpty(validated)
         : false;
   }
}
