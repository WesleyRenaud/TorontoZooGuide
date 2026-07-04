import { asTrimmedString } from '../api/normalizeValues.js';
import { DETAIL_SEPARATOR } from '../shared/constants.js';

export function formatAnimalTitleSuffix(enclosureName) {
   const normalizedEnclosureName = asTrimmedString(enclosureName);

   if (!normalizedEnclosureName) {
      return '';
   }

   return `${DETAIL_SEPARATOR}${normalizedEnclosureName}`;
}

export function formatSpeciesEnclosureLine(species, enclosureName) {
   const normalizedSpecies = asTrimmedString(species);
   const normalizedEnclosureName = asTrimmedString(enclosureName);

   if (!normalizedEnclosureName) {
      return normalizedSpecies;
   }

   return `${normalizedSpecies}${DETAIL_SEPARATOR}${normalizedEnclosureName}`;
}

export function formatExhibitEnclosureTypeLine(exhibit, enclosureType) {
   const normalizedExhibit = asTrimmedString(exhibit);
   const normalizedEnclosureType = asTrimmedString(enclosureType);

   if (!normalizedEnclosureType) {
      return normalizedExhibit;
   }

   return `${normalizedExhibit}${DETAIL_SEPARATOR}${normalizedEnclosureType}`;
}
