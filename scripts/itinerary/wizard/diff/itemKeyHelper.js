export class ItemKeyHelper {
   static normalizeKeyPart(value) {
      if (typeof value !== 'string') {
         return '';
      }

      return value.trim().toLowerCase();
   }
}
