export class StoredSelectionHelper {
   static normalizeStoredSelectionItems(items) {
      return Array.isArray(items)
         ? items
         : [];
   }

   static migrateStoredSelectionItem(item, {
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
}
