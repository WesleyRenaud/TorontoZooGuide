import { ItemKey } from './itemKey.js';

export class RemovedItemsHelper {
   static buildValidatedItemKeySet(items = [], field) {
      return new Set(
         items
            .map((item) => ItemKey.buildItemKey(item, field))
            .filter(Boolean)
      );
   }
}
