function normalizeKeyPart(value) {
   if (typeof value !== 'string') {
      return '';
   }

   return value.trim().toLowerCase();
}

export class ItemKey {
   static buildItemKey(item, field) {
      return normalizeKeyPart(item?.[field]);
   }
}
