import { ItineraryShape } from '../itineraryShape.js';
import { ItineraryWizardDraftMutator } from './itineraryWizardDraftMutator.js';

export class ItineraryWizardStore {
   static createItineraryWizardState(existing = {}) {
      const initialDraft = ItineraryShape.cloneItineraryDraft(
         ItineraryShape.hydrateWizardDraftFromSavedItinerary(existing)
      );
      const state = {
         ...ItineraryWizardDraftMutator.buildWizardDraftSnapshot(initialDraft),
         ...ItineraryWizardDraftMutator.createPendingValidationState(),
      };

      ItineraryWizardDraftMutator.writeDraftState(initialDraft);

      function persistDraft() {
         ItineraryWizardDraftMutator.writeDraftState(ItineraryWizardDraftMutator.buildWizardDraftSnapshot(state));
      }

      return {
         state,

         updateSelection(key, value, { preserveOnInvalid = false } = {}) {
            if (!ItineraryWizardDraftMutator.applySelectionUpdate(state, key, value, { preserveOnInvalid })) {
               return;
            }

            persistDraft();
         },

         applyValidationResult(date, result) {
            state.date = date;
            ItineraryWizardDraftMutator.applyPendingValidation(state, result ?? {});

            persistDraft();
         },

         consumePendingValidation() {
            return ItineraryWizardDraftMutator.consumePendingValidationState(state);
         },

         allowEmptyFinish(allowEmpty = false) {
            return state.pendingValidatedEmpty || allowEmpty === true;
         },

         hasUnsavedChanges() {
            const snapshot = ItineraryWizardDraftMutator.buildWizardDraftSnapshot(state);

            if (ItineraryShape.isItineraryEmptyDraft(snapshot) && ItineraryShape.isItineraryEmptyDraft(initialDraft)) {
               return false;
            }

            return !ItineraryShape.areItineraryDraftsSemanticallyEqual(snapshot, initialDraft);
         },

         discardChanges() {
            ItineraryWizardDraftMutator.assignWizardDraft(state, initialDraft);
            ItineraryWizardDraftMutator.resetPendingValidation(state);
            ItineraryWizardDraftMutator.writeDraftState(initialDraft);
         },
      };
   }
}
