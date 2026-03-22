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

export async function validateItinerary({ date, dateObj } = {}) {
   if (!date || !(dateObj instanceof Date) || !Number.isFinite(dateObj.getTime())) {
      return null;
   }

   const animals = loadArray(ANIMALS_KEY);
   const attractions = loadArray(ATTRACTIONS_KEY);
   const guardiansTalks = loadArray(GUARDIANS_KEY);
   const wildEncounters = loadArray(WILD_KEY);

   const result = await postJson('/validate-itinerary', {
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
      attractions: findRemovedItems(previous.attractions, validated.attractions, ['name']),
      guardiansTalks: findRemovedItems(previous.guardiansTalks, validated.guardiansTalks, ['name']),
      wildEncounters: findRemovedItems(previous.wildEncounters, validated.wildEncounters, ['name']),
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
   };
}