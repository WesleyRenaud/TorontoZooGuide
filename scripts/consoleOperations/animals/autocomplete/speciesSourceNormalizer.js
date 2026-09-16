import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class SpeciesSourceNormalizer {
   static normalizeSpeciesList(species) {
      return [...new Set(ValueNormalizer.asTrimmedStringList(species))]
         .sort((a, b) => a.localeCompare(b));
   }

   static normalizeExhibitKey(exhibit) {
      return ValueNormalizer.asTrimmedString(exhibit);
   }
}
