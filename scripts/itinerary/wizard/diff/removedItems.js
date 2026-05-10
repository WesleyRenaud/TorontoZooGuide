import { buildItemKey } from './itemKey.js';

/**
 * Combines backend "removed" rows (with removalReason when present) with items
 * that appear in previous but not validated. The backend schedule filters talks
 * and wild encounters to the new day before unavailable handling, so names that
 * are absent from the new schedule never reach removed_* on the server — but
 * previous vs validated still shows the drop and the popup should list it.
 */
export function mergeRemovedItems(
   backendItems,
   previousItems = [],
   validatedItems = [],
   field
) {
   const inferred = findRemovedItemsByField(previousItems, validatedItems, field);
   const backend = Array.isArray(backendItems) ? backendItems : [];

   if (backend.length === 0) {
      return inferred;
   }

   if (inferred.length === 0) {
      return backend;
   }

   const backendKeys = new Set(
      backend.map((item) => buildItemKey(item, field)).filter(Boolean)
   );

   const merged = [...backend];

   for (const item of inferred) {
      const key = buildItemKey(item, field);
      if (key && !backendKeys.has(key)) {
         merged.push(item);
         backendKeys.add(key);
      }
   }

   return merged;
}

function buildValidatedItemKeySet(items = [], field) {
   return new Set(
      items
         .map((item) => buildItemKey(item, field))
         .filter(Boolean)
   );
}

export function findRemovedItemsByField(
   previousItems = [],
   validatedItems = [],
   field
) {
   const validatedKeys = buildValidatedItemKeySet(validatedItems, field);

   return previousItems.filter((item) => {
      const key = buildItemKey(item, field);
      return key && !validatedKeys.has(key);
   });
}
