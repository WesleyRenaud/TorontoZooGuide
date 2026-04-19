import { validateItineraryDraftRequest } from '../../api/itineraryApi.js';
import {
   loadArray,
   saveArray,
   setStoredItineraryDate,
} from '../panel/localStorage.js';
import {
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from '../storageKeys.js';
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

function loadDraftSelections() {
   return {
      animals: loadArray(ANIMALS_KEY),
      attractions: loadArray(ATTRACTIONS_KEY),
      guardiansTalks: loadArray(GUARDIANS_KEY),
      wildEncounters: loadArray(WILD_KEY),
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

function persistValidatedDraft(date, validated) {
   setStoredItineraryDate(date);
   saveArray(ANIMALS_KEY, validated.animals);
   saveArray(ATTRACTIONS_KEY, validated.attractions);
   saveArray(GUARDIANS_KEY, validated.guardiansTalks);
   saveArray(WILD_KEY, validated.wildEncounters);
}

export async function validateItineraryDraft({ date, dateObj } = {}) {
   if (!date || !(dateObj instanceof Date) || !Number.isFinite(dateObj.getTime())) {
      return null;
   }

   const draftState = loadDraftSelections();
   const result = await validateItineraryDraftRequest(
      buildValidationPayload({ date, dateObj, draftState })
   );

   const previous = result.previous;
   const validated = result.validated;
   const diff = buildItineraryDiff(previous, validated, result.removed);

   persistValidatedDraft(date, validated);

   return {
      previous,
      validated,
      removed: diff.removed,
      reducedVisibility: diff.reducedVisibility,
      improvedVisibility: diff.improvedVisibility,
   };
}
