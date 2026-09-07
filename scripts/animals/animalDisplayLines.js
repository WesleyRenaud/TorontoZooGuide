import { ValueNormalizer } from '../api/valueNormalizer.js';
import { TimelineLayoutConstants } from '../shared/timelineLayoutConstants.js';

export class AnimalDisplayLines {
   static formatAnimalTitleSuffix(enclosureName) {
      const normalizedEnclosureName = ValueNormalizer.asTrimmedString(enclosureName);

      if (!normalizedEnclosureName) {
         return '';
      }

      return `${TimelineLayoutConstants.DETAIL_SEPARATOR}${normalizedEnclosureName}`;
   }

   static formatSpeciesEnclosureLine(species, enclosureName) {
      const normalizedSpecies = ValueNormalizer.asTrimmedString(species);
      const normalizedEnclosureName = ValueNormalizer.asTrimmedString(enclosureName);

      if (!normalizedEnclosureName) {
         return normalizedSpecies;
      }

      return `${normalizedSpecies}${TimelineLayoutConstants.DETAIL_SEPARATOR}${normalizedEnclosureName}`;
   }

   static formatExhibitEnclosureTypeLine(exhibit, enclosureType) {
      const normalizedExhibit = ValueNormalizer.asTrimmedString(exhibit);
      const normalizedEnclosureType = ValueNormalizer.asTrimmedString(enclosureType);

      if (!normalizedEnclosureType) {
         return normalizedExhibit;
      }

      return `${normalizedExhibit}${TimelineLayoutConstants.DETAIL_SEPARATOR}${normalizedEnclosureType}`;
   }
}
