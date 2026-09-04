import { ValueNormalizer } from '../api/valueNormalizer.js';

export class NormalizeGuardiansTalkLinkedAnimals {
   static normalizeGuardiansTalkLinkedAnimals(value) {
      return ValueNormalizer.asArray(value)
         .map((entry) => {
            const linked = ValueNormalizer.asObject(entry);

            return {
               species: ValueNormalizer.asTrimmedString(linked.species),
               exhibit: ValueNormalizer.asTrimmedString(linked.exhibit),
            };
         })
         .filter((linked) => linked.species && linked.exhibit);
   }
}
