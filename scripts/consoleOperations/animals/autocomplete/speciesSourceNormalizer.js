import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class SpeciesSourceNormalizer {
   static normalizeSpeciesList(species) {
      return [...new Set(
         (species || [])
            .map((value) => ValueNormalizer.asTrimmedString(value))
            .filter(Boolean)
      )].sort((a, b) => a.localeCompare(b));
   }
}
