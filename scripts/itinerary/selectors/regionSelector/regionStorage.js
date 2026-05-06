import {
   loadArray,
   saveArray,
} from '../../draftStorage.js';

export {
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
