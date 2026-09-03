export class ValueNormalizer {
   static asArray(value) {
      return Array.isArray(value) ? value : [];
   }

   static asObject(value) {
      return value && typeof value === 'object'
         ? value
         : {};
   }

   static asTrimmedString(value) {
      return typeof value === 'string'
         ? value.trim()
         : '';
   }

   static asTrimmedStringList(values) {
      return ValueNormalizer.asArray(values)
         .map((value) => String(value ?? '').trim())
         .filter(Boolean);
   }

   static asNullableString(value) {
      const stringValue = ValueNormalizer.asTrimmedString(value);
      return stringValue || null;
   }

   static asBoolean(value) {
      return value === true;
   }

   static normalizeNumber(value) {
      const number = Number(value);
      return Number.isFinite(number) ? number : null;
   }
}
