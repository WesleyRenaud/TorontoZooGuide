import { ItemKey } from './itemKey.js';

/**
 * Combines backend "removed" rows (with removalReason when present) with items
 * that appear in previous but not validated. The backend schedule filters talks
 * and wild encounters to the new day before unavailable handling, so names that
 * are absent from the new schedule never reach removed_* on the server — but
 * previous vs validated still shows the drop and the popup should list it.
 */
function buildValidatedItemKeySet(items = [], field) {
   return new Set(
      items
         .map((item) => ItemKey.buildItemKey(item, field))
         .filter(Boolean)
   );
}

export class RemovedItems {
   static mergeRemovedItems(
      backendItems,
      previousItems = [],
      validatedItems = [],
      field
   ) {
      const inferred = RemovedItems.findRemovedItemsByField(
         previousItems,
         validatedItems,
         field
      );
      const backend = Array.isArray(backendItems) ? backendItems : [];

      if (backend.length === 0) {
         return inferred;
      }

      if (inferred.length === 0) {
         return backend;
      }

      const backendKeys = new Set(
         backend.map((item) => ItemKey.buildItemKey(item, field)).filter(Boolean)
      );

      const merged = [...backend];

      for (const item of inferred) {
         const key = ItemKey.buildItemKey(item, field);
         if (key && !backendKeys.has(key)) {
            merged.push(item);
            backendKeys.add(key);
         }
      }

      return merged;
   }

   static findRemovedItemsByField(
      previousItems = [],
      validatedItems = [],
      field
   ) {
      const validatedKeys = buildValidatedItemKeySet(validatedItems, field);

      return previousItems.filter((item) => {
         const key = ItemKey.buildItemKey(item, field);
         return key && !validatedKeys.has(key);
      });
   }
}
