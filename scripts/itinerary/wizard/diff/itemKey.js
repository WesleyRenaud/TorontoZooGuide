import { ItemKeyHelpers } from './itemKeyHelpers.js';

export class ItemKey {
   static buildItemKey(item, field) {
      return ItemKeyHelpers.normalizeKeyPart(item?.[field]);
   }
}
