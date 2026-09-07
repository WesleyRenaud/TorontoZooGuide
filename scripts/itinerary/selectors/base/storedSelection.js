import { StoredSelectionHelpers } from './storedSelectionHelpers.js';
export class StoredSelection {
   static normalizeStoredBoolean(value) {
      return value === true;
   }

   static normalizeStoredString(value) {
      return typeof value === 'string'
         ? value.trim()
         : '';
   }

   static normalizeStoredLink(value) {
      const link = StoredSelection.normalizeStoredString(value);
      return link || null;
   }

   static normalizeStoredId(value, fallback = '') {
      return StoredSelection.normalizeStoredString(value)
         || StoredSelection.normalizeStoredString(fallback);
   }

   static migrateStoredSelectionItems(items, {
      fromString = null,
      fromObject = null,
   } = {}) {
      return StoredSelectionHelpers.normalizeStoredSelectionItems(items)
         .map((item) => StoredSelectionHelpers.migrateStoredSelectionItem(item, {
            fromString,
            fromObject,
         }))
         .filter(Boolean);
   }
}
