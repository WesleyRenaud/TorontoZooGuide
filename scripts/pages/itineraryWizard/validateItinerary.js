import { postJson } from '../../api/apiClient.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from './keys.js';

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

function buildKey(item, fields = []) {
   if (typeof item === 'string') {
      return item.trim().toLowerCase();
   }

   for (const field of fields) {
      const value = item?.[field];
      if (typeof value === 'string' && value.trim()) {
         return value.trim().toLowerCase();
      }
   }

   return '';
}

function findRemovedItems(previousItems, validatedItems, fields = []) {
   const validatedKeys = new Set(
      validatedItems
         .map(item => buildKey(item, fields))
         .filter(Boolean)
   );

   return previousItems.filter(item => {
      const key = buildKey(item, fields);
      return key && !validatedKeys.has(key);
   });
}

function getLikelihoodValue(animal) {
   const raw =
      animal?.likelihood ??
      animal?.LIKELIHOOD ??
      animal?.likelihood_value ??
      animal?.LIKELIHOOD_VALUE ??
      null;

   const value = Number(raw);
   return Number.isFinite(value) ? value : null;
}

function toNormalizedLikelihood(value) {
   if (typeof value !== 'number' || !Number.isFinite(value)) return null;
   return value > 1 ? value / 100 : value;
}

function findReducedVisibilityAnimals(previousAnimals, validatedAnimals, removedAnimals = [], minDrop = 0.2) {
   const validatedByKey = new Map(
      validatedAnimals
         .map(animal => [buildKey(animal, ['species', 'name']), animal])
         .filter(([key]) => Boolean(key))
   );

   const removedKeys = new Set(
      removedAnimals
         .map(animal => buildKey(animal, ['species', 'name']))
         .filter(Boolean)
   );

   return previousAnimals
      .map(previousAnimal => {
         const key = buildKey(previousAnimal, ['species', 'name']);
         if (!key || removedKeys.has(key)) return null;

         const validatedAnimal = validatedByKey.get(key);
         if (!validatedAnimal) return null;

         const before = toNormalizedLikelihood(getLikelihoodValue(previousAnimal));
         const after = toNormalizedLikelihood(getLikelihoodValue(validatedAnimal));

         if (before == null || after == null) return null;
         if (after >= before) return null;
         if ((before - after) < minDrop) return null;

         return {
            ...validatedAnimal,
            likelihoodBefore: before,
            likelihoodAfter: after,
         };
      })
      .filter(Boolean);
}

function findImprovedVisibilityAnimals(previousAnimals, validatedAnimals, removedAnimals = [], minIncrease = 0.2) {
   const validatedByKey = new Map(
      validatedAnimals
         .map(animal => [buildKey(animal, ['species', 'name']), animal])
         .filter(([key]) => Boolean(key))
   );

   const removedKeys = new Set(
      removedAnimals
         .map(animal => buildKey(animal, ['species', 'name']))
         .filter(Boolean)
   );

   return previousAnimals
      .map(previousAnimal => {
         const key = buildKey(previousAnimal, ['species', 'name']);
         if (!key || removedKeys.has(key)) return null;

         const validatedAnimal = validatedByKey.get(key);
         if (!validatedAnimal) return null;

         const before = toNormalizedLikelihood(getLikelihoodValue(previousAnimal));
         const after = toNormalizedLikelihood(getLikelihoodValue(validatedAnimal));

         if (before == null || after == null) return null;
         if (after <= before) return null;
         if ((after - before) < minIncrease) return null;

         return {
            ...validatedAnimal,
            likelihoodBefore: before,
            likelihoodAfter: after,
         };
      })
      .filter(Boolean);
}

export async function validateItinerary({ date, dateObj } = {}) {
   if (!date || !(dateObj instanceof Date) || !Number.isFinite(dateObj.getTime())) {
      return null;
   }

   const animals = loadArray(ANIMALS_KEY);
   const attractions = loadArray(ATTRACTIONS_KEY);
   const guardiansTalks = loadArray(GUARDIANS_KEY);
   const wildEncounters = loadArray(WILD_KEY);

   const result = await postJson('/validate-itinerary', {
      date,
      month: getMonthName(dateObj),
      day: getDayOfMonth(dateObj),
      animals: extractNames(animals, ['species', 'name']),
      attractions: extractNames(attractions, ['name']),
      guardiansTalks: extractNames(guardiansTalks, ['name']),
      wildEncounters: extractNames(wildEncounters, ['name']),
   });

   const previous = {
      animals: Array.isArray(result?.previous?.animals) ? result.previous.animals : animals,
      attractions: Array.isArray(result?.previous?.attractions) ? result.previous.attractions : attractions,
      guardiansTalks: Array.isArray(result?.previous?.guardiansTalks) ? result.previous.guardiansTalks : guardiansTalks,
      wildEncounters: Array.isArray(result?.previous?.wildEncounters) ? result.previous.wildEncounters : wildEncounters,
   };

   const validated = {
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

   const removed = {
      animals: Array.isArray(result?.removed?.animals)
         ? result.removed.animals
         : findRemovedItems(previous.animals, validated.animals, ['species', 'name']),
      attractions: Array.isArray(result?.removed?.attractions)
         ? result.removed.attractions
         : findRemovedItems(previous.attractions, validated.attractions, ['name']),
      guardiansTalks: Array.isArray(result?.removed?.guardiansTalks)
         ? result.removed.guardiansTalks
         : findRemovedItems(previous.guardiansTalks, validated.guardiansTalks, ['name']),
      wildEncounters: Array.isArray(result?.removed?.wildEncounters)
         ? result.removed.wildEncounters
         : findRemovedItems(previous.wildEncounters, validated.wildEncounters, ['name']),
   };

   const reducedVisibility = {
      animals: findReducedVisibilityAnimals(
         previous.animals,
         validated.animals,
         removed.animals,
         0.2
      ),
   };

   const improvedVisibility = {
      animals: findImprovedVisibilityAnimals(
         previous.animals,
         validated.animals,
         removed.animals,
         0.2
      ),
   };

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