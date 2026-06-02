import {
   loadArray,
   saveArray,
} from '../../draftStorage.js';
import { REMOVED_ANIMALS_KEY } from '../../storageKeys.js';

export {
   REMOVED_ANIMALS_KEY,
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
} from '../../storageKeys.js';

export function loadSelectedNames(storageKey) {
   return loadArray(storageKey)
      .map((name) => typeof name === 'string' ? name.trim() : '')
      .filter(Boolean);
}

export function saveSelectedNames(storageKey, names) {
   saveArray(
      storageKey,
      Array.from(names)
         .map((name) => typeof name === 'string' ? name.trim() : '')
         .filter(Boolean)
   );
}

function normalizeStoredAnimalKey(key) {
   return String(key ?? '').trim().toLowerCase();
}

export function loadRemovedAnimalKeys() {
   return new Set(
      loadArray(REMOVED_ANIMALS_KEY)
         .map(normalizeStoredAnimalKey)
         .filter(Boolean)
   );
}

export function addRemovedAnimalKey(key) {
   const normalizedKey = normalizeStoredAnimalKey(key);

   if (!normalizedKey) {
      return;
   }

   const removedKeys = loadRemovedAnimalKeys();
   removedKeys.add(normalizedKey);
   saveArray(REMOVED_ANIMALS_KEY, [...removedKeys]);
}

export function restoreRemovedAnimalKey(key) {
   const normalizedKey = normalizeStoredAnimalKey(key);
   const removedKeys = loadRemovedAnimalKeys();

   if (!removedKeys.delete(normalizedKey)) {
      return;
   }

   saveArray(REMOVED_ANIMALS_KEY, [...removedKeys]);
}

export function clearRemovedAnimalKeys() {
   saveArray(REMOVED_ANIMALS_KEY, []);
}

export function clearRemovedAnimalKeysForExhibit(exhibitName) {
   const normalizedExhibit = String(exhibitName ?? '').trim().toLowerCase();

   if (!normalizedExhibit) {
      return;
   }

   const exhibitSuffix = `||${normalizedExhibit}`;
   const removedKeys = loadRemovedAnimalKeys();
   const nextKeys = [...removedKeys].filter((key) => !key.endsWith(exhibitSuffix));

   if (nextKeys.length === removedKeys.size) {
      return;
   }

   saveArray(REMOVED_ANIMALS_KEY, nextKeys);
}
