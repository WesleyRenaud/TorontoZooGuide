export class ItemKeyHelpers {
   static normalizeKeyPart(value) {
      if (typeof value !== 'string') {
         return '';
      }

      return value.trim().toLowerCase();
   }
}
