import { validateItineraryDraftRequest } from '../../api/itineraryApi.js';
import { normalizeItineraryDraft } from '../draftStorage.js';
import {
   buildItineraryDiff,
} from './itineraryDiff.js';

function getMonthName(dateObj) {
   return dateObj.toLocaleString('en-CA', { month: 'long' });
}

function getDayOfMonth(dateObj) {
   return dateObj.getDate();
}

function extractAnimalSpecies(items = []) {
   return items
      .map((item) => {
         if (typeof item === 'string') {
            return item.trim();
         }

         return String(item?.species ?? '').trim();
      })
      .filter(Boolean);
}

function extractNamedItems(items = []) {
   return items
      .map((item) => {
         if (typeof item === 'string') {
            return item.trim();
         }

         return String(item?.name ?? '').trim();
      })
      .filter(Boolean);
}

function normalizeDraftSelections(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return {
      animals: normalizedDraft.animals,
      attractions: normalizedDraft.attractions,
      guardiansTalks: normalizedDraft.guardiansTalks,
      wildEncounters: normalizedDraft.wildEncounters,
   };
}

function buildValidationPayload({ date, dateObj, draftState }) {
   return {
      date,
      month: getMonthName(dateObj),
      day: getDayOfMonth(dateObj),
      animals: extractAnimalSpecies(draftState.animals),
      attractions: extractNamedItems(draftState.attractions),
      guardiansTalks: extractNamedItems(draftState.guardiansTalks),
      wildEncounters: extractNamedItems(draftState.wildEncounters),
   };
}

export async function validateItineraryDraft({ date, dateObj, draft } = {}) {
   if (!date || !(dateObj instanceof Date) || !Number.isFinite(dateObj.getTime())) {
      return null;
   }

   const draftState = normalizeDraftSelections(draft);
   const result = await validateItineraryDraftRequest(
      buildValidationPayload({ date, dateObj, draftState })
   );

   const previous = result.previous;
   const validated = result.validated;
   const diff = buildItineraryDiff(previous, validated, result.removed);

   return {
      previous,
      validated,
      removed: diff.removed,
      reducedVisibility: diff.reducedVisibility,
      improvedVisibility: diff.improvedVisibility,
   };
}
