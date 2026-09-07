import { ValueNormalizer } from './valueNormalizer.js';

export class ItinerarySelectorApiNormalizer {
   static normalizeRegion(region) {
      const source = ValueNormalizer.asObject(region);

      return {
         name: ValueNormalizer.asTrimmedString(source.name),
         exhibits: Array.isArray(source.exhibits)
            ? source.exhibits.map(ValueNormalizer.asTrimmedString).filter(Boolean)
            : [],
      };
   }

   static normalizeAnimal(animal) {
      const source = ValueNormalizer.asObject(animal);

      return {
         ...source,
         species: ValueNormalizer.asTrimmedString(source.species),
         exhibit: ValueNormalizer.asTrimmedString(source.exhibit),
      };
   }
}
