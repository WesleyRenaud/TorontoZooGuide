import { validateItineraryDraftRequest } from '../../api/itineraryApi.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from '../storageKeys.js';
import {
   buildRemovedItems,
   buildReducedVisibility,
   buildImprovedVisibility,
} from './itineraryDiff.js';

function loadArray(key) {
   try {
      const raw = localStorage.getItem(key);
      const arr = JSON.parse(raw || '[]');
      return Array.isArray(arr) ? arr : [];
   } catch {
      return [];
   }
}

function extractNames(items, fields = []) {
   return items
      .map(item => {
         if (typeof item === 'string') {
            return item.trim();
         }

         for (const field of fields) {
            const value = item?.[field];
            if (typeof value === 'string' && value.trim()) {
               return value.trim();
            }
         }

         return '';
      })
      .filter(Boolean);
}

function getMonthName(dateObj) {
   return dateObj.toLocaleString('en-CA', { month: 'long' });
}

function getDayOfMonth(dateObj) {
   return dateObj.getDate();
}

function persistValidatedDraft({
   date,
   animals,
   attractions,
   guardiansTalks,
   wildEncounters,
}) {
   localStorage.setItem(DATE_KEY, date);
   localStorage.setItem(ANIMALS_KEY, JSON.stringify(animals));
   localStorage.setItem(ATTRACTIONS_KEY, JSON.stringify(attractions));
   localStorage.setItem(GUARDIANS_KEY, JSON.stringify(guardiansTalks));
   localStorage.setItem(WILD_KEY, JSON.stringify(wildEncounters));
}

function buildPreviousState(result, fallback) {
   return {
      animals: Array.isArray(result?.previous?.animals)
         ? result.previous.animals
         : fallback.animals,
      attractions: Array.isArray(result?.previous?.attractions)
         ? result.previous.attractions
         : fallback.attractions,
      guardiansTalks: Array.isArray(result?.previous?.guardiansTalks)
         ? result.previous.guardiansTalks
         : fallback.guardiansTalks,
      wildEncounters: Array.isArray(result?.previous?.wildEncounters)
         ? result.previous.wildEncounters
         : fallback.wildEncounters,
   };
}

function buildValidatedState(result) {
   return {
      animals: Array.isArray(result?.validated?.animals)
         ? result.validated.animals
         : Array.isArray(result?.animals)
            ? result.animals
            : [],
      attractions: Array.isArray(result?.validated?.attractions)
         ? result.validated.attractions
         : Array.isArray(result?.attractions)
            ? result.attractions
            : [],
      guardiansTalks: Array.isArray(result?.validated?.guardiansTalks)
         ? result.validated.guardiansTalks
         : Array.isArray(result?.guardiansTalks)
            ? result.guardiansTalks
            : [],
      wildEncounters: Array.isArray(result?.validated?.wildEncounters)
         ? result.validated.wildEncounters
         : Array.isArray(result?.wildEncounters)
            ? result.wildEncounters
            : [],
   };
}

export async function validateItineraryDraft({ date, dateObj } = {}) {
   if (!date || !(dateObj instanceof Date) || !Number.isFinite(dateObj.getTime())) {
      return null;
   }

   const draftState = {
      animals: loadArray(ANIMALS_KEY),
      attractions: loadArray(ATTRACTIONS_KEY),
      guardiansTalks: loadArray(GUARDIANS_KEY),
      wildEncounters: loadArray(WILD_KEY),
   };

   const result = await validateItineraryDraftRequest({
      date,
      month: getMonthName(dateObj),
      day: getDayOfMonth(dateObj),
      animals: extractNames(draftState.animals, ['species', 'name']),
      attractions: extractNames(draftState.attractions, ['name']),
      guardiansTalks: extractNames(draftState.guardiansTalks, ['name']),
      wildEncounters: extractNames(draftState.wildEncounters, ['name']),
   });

   const previous = buildPreviousState(result, draftState);
   const validated = buildValidatedState(result);

   const removed = buildRemovedItems(previous, validated, result?.removed);
   const reducedVisibility = buildReducedVisibility(previous, validated, removed);
   const improvedVisibility = buildImprovedVisibility(previous, validated, removed);

   persistValidatedDraft({
      date,
      animals: validated.animals,
      attractions: validated.attractions,
      guardiansTalks: validated.guardiansTalks,
      wildEncounters: validated.wildEncounters,
   });

   return {
      previous,
      validated,
      removed,
      reducedVisibility,
      improvedVisibility,
   };
}
