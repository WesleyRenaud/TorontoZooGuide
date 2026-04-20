import { buildItemKey } from './itemKey.js';

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
