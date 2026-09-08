export class RemovedItemsPopupHelpers {
   static toggleKeptItem(keptItemsByKey, item, buildKey, normalizeItem) {
      const key = buildKey(item);

      if (!key) {
         return;
      }

      if (keptItemsByKey.has(key)) {
         keptItemsByKey.delete(key);
         return;
      }

      keptItemsByKey.set(key, normalizeItem(item));
   }
}
