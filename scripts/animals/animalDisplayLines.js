import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Constants } from '../shared/constants.js';

export class AnimalDisplayLines {
   static formatAnimalTitleSuffix(enclosureName) {
      const normalizedEnclosureName = ValueNormalizer.asTrimmedString(enclosureName);

      if (!normalizedEnclosureName) {
         return '';
      }

      return `${Constants.DETAIL_SEPARATOR}${normalizedEnclosureName}`;
   }

   static formatSpeciesEnclosureLine(species, enclosureName) {
      const normalizedSpecies = ValueNormalizer.asTrimmedString(species);
      const normalizedEnclosureName = ValueNormalizer.asTrimmedString(enclosureName);

      if (!normalizedEnclosureName) {
         return normalizedSpecies;
      }

      return `${normalizedSpecies}${Constants.DETAIL_SEPARATOR}${normalizedEnclosureName}`;
   }

   static formatExhibitEnclosureTypeLine(exhibit, enclosureType) {
      const normalizedExhibit = ValueNormalizer.asTrimmedString(exhibit);
      const normalizedEnclosureType = ValueNormalizer.asTrimmedString(enclosureType);

      if (!normalizedEnclosureType) {
         return normalizedExhibit;
      }

      return `${normalizedExhibit}${Constants.DETAIL_SEPARATOR}${normalizedEnclosureType}`;
   }
}
