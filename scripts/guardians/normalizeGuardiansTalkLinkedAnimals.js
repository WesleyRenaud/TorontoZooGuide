import {
   asArray,
   asObject,
   asTrimmedString,
} from '../api/normalizeValues.js';

export function normalizeGuardiansTalkLinkedAnimals(value) {
   return asArray(value)
      .map((entry) => {
         const linked = asObject(entry);

         return {
            species: asTrimmedString(linked.species),
            exhibit: asTrimmedString(linked.exhibit),
         };
      })
      .filter((linked) => linked.species && linked.exhibit);
}
