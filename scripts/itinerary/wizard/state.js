import { loadArray } from '../panel/localStorage.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from '../storageKeys.js';
import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
} from './itineraryDiff.js';

function getDraftState() {
   return {
      date: localStorage.getItem(DATE_KEY) || '',
      animals: loadArray(ANIMALS_KEY),
      attractions: loadArray(ATTRACTIONS_KEY),
      guardiansTalks: loadArray(GUARDIANS_KEY),
      wildEncounters: loadArray(WILD_KEY),
   };
}

function writeDraftState({
   date = '',
   animals = [],
   attractions = [],
   guardiansTalks = [],
   wildEncounters = [],
}) {
   if (date) {
      localStorage.setItem(DATE_KEY, date);
   } else {
      localStorage.removeItem(DATE_KEY);
   }

   localStorage.setItem(ANIMALS_KEY, JSON.stringify(Array.isArray(animals) ? animals : []));
   localStorage.setItem(ATTRACTIONS_KEY, JSON.stringify(Array.isArray(attractions) ? attractions : []));
   localStorage.setItem(GUARDIANS_KEY, JSON.stringify(Array.isArray(guardiansTalks) ? guardiansTalks : []));
   localStorage.setItem(WILD_KEY, JSON.stringify(Array.isArray(wildEncounters) ? wildEncounters : []));
}

function snapshotStorage() {
   return {
      [DATE_KEY]: localStorage.getItem(DATE_KEY),
      [ANIMALS_KEY]: localStorage.getItem(ANIMALS_KEY),
      [ATTRACTIONS_KEY]: localStorage.getItem(ATTRACTIONS_KEY),
      [GUARDIANS_KEY]: localStorage.getItem(GUARDIANS_KEY),
      [WILD_KEY]: localStorage.getItem(WILD_KEY),
   };
}

function restoreStorageSnapshot(snapshot) {
   Object.entries(snapshot).forEach(([key, value]) => {
      if (value == null) {
         localStorage.removeItem(key);
      } else {
         localStorage.setItem(key, value);
      }
   });
}

function getWizardSelections(state) {
   return {
      date: state.date,
      animals: state.animals,
      attractions: state.attractions,
      guardiansTalks: state.guardiansTalks,
      wildEncounters: state.wildEncounters,
   };
}

function applyValidatedSelections(state, validated) {
   if (!validated) return;

   state.animals = Array.isArray(validated.animals) ? validated.animals : [];
   state.attractions = Array.isArray(validated.attractions) ? validated.attractions : [];
   state.guardiansTalks = Array.isArray(validated.guardiansTalks) ? validated.guardiansTalks : [];
   state.wildEncounters = Array.isArray(validated.wildEncounters) ? validated.wildEncounters : [];
}

export function createItineraryWizardState(existing = {}) {
   const state = {
      date: existing.date || '',
      animals: Array.isArray(existing.animals) ? existing.animals : [],
      attractions: Array.isArray(existing.attractions) ? existing.attractions : [],
      guardiansTalks: Array.isArray(existing.guardiansTalks) ? existing.guardiansTalks : [],
      wildEncounters: Array.isArray(existing.wildEncounters) ? existing.wildEncounters : [],
      pendingRemovedItems: null,
      pendingReducedVisibility: null,
      pendingImprovedVisibility: null,
      pendingValidatedEmpty: false,
   };

   writeDraftState(getWizardSelections(state));

   const initialStorageSnapshot = snapshotStorage();
   const initialDraftStateJSON = JSON.stringify(getDraftState());

   function persistDraft() {
      writeDraftState(getWizardSelections(state));
   }

   return {
      state,

      updateSelection(key, value, { preserveOnInvalid = false } = {}) {
         state[key] = Array.isArray(value)
            ? value
            : preserveOnInvalid
               ? state[key]
               : [];

         persistDraft();
      },

      applyValidationResult(date, result) {
         const validated = result?.validated ?? null;
         const removed = result?.removed ?? null;
         const reducedVisibility = result?.reducedVisibility ?? null;
         const improvedVisibility = result?.improvedVisibility ?? null;

         applyValidatedSelections(state, validated);

         state.date = date;
         state.pendingRemovedItems = hasRemovedItems(removed) ? removed : null;
         state.pendingReducedVisibility = hasReducedVisibility(reducedVisibility) ? reducedVisibility : null;
         state.pendingImprovedVisibility = hasImprovedVisibility(improvedVisibility) ? improvedVisibility : null;
         state.pendingValidatedEmpty = isValidatedItineraryEmpty(validated);

         persistDraft();
      },

      consumePendingValidation() {
         const pending = {
            removed: state.pendingRemovedItems,
            reducedVisibility: state.pendingReducedVisibility,
            improvedVisibility: state.pendingImprovedVisibility,
            isEmptyItinerary: state.pendingValidatedEmpty,
         };

         state.pendingRemovedItems = null;
         state.pendingReducedVisibility = null;
         state.pendingImprovedVisibility = null;
         state.pendingValidatedEmpty = false;

         return pending;
      },

      allowEmptyFinish(allowEmpty = false) {
         return state.pendingValidatedEmpty || allowEmpty === true;
      },

      hasUnsavedChanges() {
         return JSON.stringify(getDraftState()) !== initialDraftStateJSON;
      },

      discardChanges() {
         restoreStorageSnapshot(initialStorageSnapshot);
      },
   };
}
