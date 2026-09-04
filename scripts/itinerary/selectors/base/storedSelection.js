function normalizeStoredSelectionItems(items) {
   return Array.isArray(items)
      ? items
      : [];
}

function migrateStoredSelectionItem(item, {
   fromString = null,
   fromObject = null,
} = {}) {
   if (typeof item === 'string') {
      return typeof fromString === 'function'
         ? fromString(item)
         : null;
   }

   if (item && typeof item === 'object') {
      return typeof fromObject === 'function'
         ? fromObject(item)
         : null;
   }

   return null;
}

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
      return normalizeStoredSelectionItems(items)
         .map((item) => migrateStoredSelectionItem(item, {
            fromString,
            fromObject,
         }))
         .filter(Boolean);
   }
}
