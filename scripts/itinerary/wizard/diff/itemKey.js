import { ItemKeyHelper } from './itemKeyHelper.js';

export class ItemKey {
   static buildItemKey(item, field) {
      return ItemKeyHelper.normalizeKeyPart(item?.[field]);
   }
}
