import { Strings } from '../scripts/strings.js';

function serializeStrings(value) {
   if (typeof value === 'function') {
      return undefined;
   }

   if (Array.isArray(value)) {
      return value
         .map((item) => serializeStrings(item))
         .filter((item) => item !== undefined);
   }

   if (value && typeof value === 'object') {
      return Object.fromEntries(
         Object.entries(value)
            .map(([key, item]) => [key, serializeStrings(item)])
            .filter(([, item]) => item !== undefined)
      );
   }

   return value;
}

process.stdout.write(JSON.stringify(serializeStrings(
   Object.fromEntries(
      Object.getOwnPropertyNames(Strings)
         .filter((key) => {
            const value = Strings[key];
            return value && typeof value === 'object';
         })
         .map((key) => [key, Strings[key]])
   )
)));
