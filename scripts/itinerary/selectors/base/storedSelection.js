import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { StoredSelectionHelpers } from './storedSelectionHelpers.js';

export class StoredSelection {
   static normalizeStoredBoolean(value) {
      return value === true;
   }

   static normalizeStoredLink(value) {
      const link = ValueNormalizer.asTrimmedString(value);
      return link || null;
   }

   static normalizeStoredId(value, fallback = '') {
      return ValueNormalizer.asTrimmedString(value)
         || ValueNormalizer.asTrimmedString(fallback);
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
