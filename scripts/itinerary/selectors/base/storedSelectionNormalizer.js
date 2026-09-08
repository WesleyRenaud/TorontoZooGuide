import { StoredSelectionHelper } from './storedSelectionHelper.js';
export class StoredSelectionNormalizer {
   static normalizeStoredBoolean(value) {
      return value === true;
   }

   static normalizeStoredString(value) {
      return typeof value === 'string'
         ? value.trim()
         : '';
   }

   static normalizeStoredLink(value) {
      const link = StoredSelectionNormalizer.normalizeStoredString(value);
      return link || null;
   }

   static normalizeStoredId(value, fallback = '') {
      return StoredSelectionNormalizer.normalizeStoredString(value)
         || StoredSelectionNormalizer.normalizeStoredString(fallback);
   }

   static migrateStoredSelectionItems(items, {
      fromString = null,
      fromObject = null,
   } = {}) {
      return StoredSelectionHelper.normalizeStoredSelectionItems(items)
         .map((item) => StoredSelectionHelper.migrateStoredSelectionItem(item, {
            fromString,
            fromObject,
         }))
         .filter(Boolean);
   }
}
