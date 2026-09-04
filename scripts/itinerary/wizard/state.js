import { Summary } from './diff/summary.js';
import { DraftStorage } from '../draftStorage.js';
import { ItineraryShape } from '../itineraryShape.js';

function createPendingValidationState() {
   return {
      pendingRemovedItems: null,
      pendingUnscheduledItems: null,
      pendingReducedVisibility: null,
      pendingImprovedVisibility: null,
      pendingValidatedEmpty: false,
   };
}

function buildWizardDraftSnapshot(state = {}) {
   return ItineraryShape.cloneItineraryDraft(state);
}

function writeDraftState(draft) {
   DraftStorage.writeStoredItineraryDraft(draft);
}

function assignWizardDraft(state, draft) {
   const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

   state.date = normalizedDraft.date;
   state.animals = normalizedDraft.animals.slice();
   state.attractions = normalizedDraft.attractions.slice();
   state.guardiansTalks = normalizedDraft.guardiansTalks.slice();
   state.wildEncounters = normalizedDraft.wildEncounters.slice();
   state.transportations = normalizedDraft.transportations.slice();
   state.transportationStations = normalizedDraft.transportationStations.slice();
}

function resetPendingValidation(state) {
   state.pendingRemovedItems = null;
   state.pendingUnscheduledItems = null;
   state.pendingReducedVisibility = null;
   state.pendingImprovedVisibility = null;
   state.pendingValidatedEmpty = false;
}

function consumePendingValidationState(state) {
   const pendingValidation = {
      removed: state.pendingRemovedItems,
      unscheduled: state.pendingUnscheduledItems,
      reducedVisibility: state.pendingReducedVisibility,
      improvedVisibility: state.pendingImprovedVisibility,
      isEmptyItinerary: state.pendingValidatedEmpty,
   };

   resetPendingValidation(state);
   return pendingValidation;
}

function applySelectionUpdate(state, key, value, { preserveOnInvalid = false } = {}) {
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

function applyPendingValidation(state, {
   removed = null,
   unscheduled = null,
   reducedVisibility = null,
   improvedVisibility = null,
   validated = null,
} = {}) {
   if (validated) {
      assignWizardDraft(state, {
         ...buildWizardDraftSnapshot(state),
         ...validated,
      });
   }

   state.pendingRemovedItems = Summary.hasRemovedItems(removed) ? removed : null;
   state.pendingUnscheduledItems = Summary.hasUnscheduledItems(unscheduled) ? unscheduled : null;
   state.pendingReducedVisibility = Summary.hasReducedVisibility(reducedVisibility) ? reducedVisibility : null;
   state.pendingImprovedVisibility = Summary.hasImprovedVisibility(improvedVisibility) ? improvedVisibility : null;
   state.pendingValidatedEmpty = validated != null
      ? Summary.isValidatedItineraryEmpty(validated)
      : false;
}

export function createItineraryWizardState(existing = {}) {
   const initialDraft = ItineraryShape.cloneItineraryDraft(
      ItineraryShape.hydrateWizardDraftFromSavedItinerary(existing)
   );
   const state = {
      ...buildWizardDraftSnapshot(initialDraft),
      ...createPendingValidationState(),
   };

   writeDraftState(initialDraft);

   function persistDraft() {
      writeDraftState(buildWizardDraftSnapshot(state));
   }

   return {
      state,

      updateSelection(key, value, { preserveOnInvalid = false } = {}) {
         if (!applySelectionUpdate(state, key, value, { preserveOnInvalid })) {
            return;
         }

         persistDraft();
      },

      applyValidationResult(date, result) {
         state.date = date;
         applyPendingValidation(state, result ?? {});

         persistDraft();
      },

      consumePendingValidation() {
         return consumePendingValidationState(state);
      },

      allowEmptyFinish(allowEmpty = false) {
         return state.pendingValidatedEmpty || allowEmpty === true;
      },

      hasUnsavedChanges() {
         const snapshot = buildWizardDraftSnapshot(state);

         if (ItineraryShape.isItineraryEmptyDraft(snapshot) && ItineraryShape.isItineraryEmptyDraft(initialDraft)) {
            return false;
         }

         return !ItineraryShape.areItineraryDraftsSemanticallyEqual(snapshot, initialDraft);
      },

      discardChanges() {
         assignWizardDraft(state, initialDraft);
         resetPendingValidation(state);
         writeDraftState(initialDraft);
      },
   };
}
