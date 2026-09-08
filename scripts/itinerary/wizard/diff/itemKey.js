import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class ItemKey {
   static buildItemKey(item, field) {
      return ValueNormalizer.asTrimmedString(item?.[field]).toLowerCase();
   }
}
