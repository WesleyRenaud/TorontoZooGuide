function normalizeKeyPart(value) {
   if (typeof value !== 'string') {
      return '';
   }

   return value.trim().toLowerCase();
}

export function buildItemKey(item, field) {
   return normalizeKeyPart(item?.[field]);
}
