import { asTrimmedString } from '../api/normalizeValues.js';
import { DETAIL_SEPARATOR } from '../shared/constants.js';
import { isEnclosureType } from '../shared/enums/enclosureType.js';

function normalizeDisplayDetail(value) {
   const normalized = asTrimmedString(value);

   if (isEnclosureType(normalized)) {
      return '';
   }

   return normalized;
}

export function formatAnimalTitleSuffix(enclosureName) {
   const normalizedEnclosureName = normalizeDisplayDetail(enclosureName);

   if (!normalizedEnclosureName) {
      return '';
   }

   return `${DETAIL_SEPARATOR}${normalizedEnclosureName}`;
}

export function formatSpeciesEnclosureLine(species, enclosureName) {
   const normalizedSpecies = asTrimmedString(species);
   const normalizedEnclosureName = normalizeDisplayDetail(enclosureName);

   if (!normalizedEnclosureName) {
      return normalizedSpecies;
   }

   return `${normalizedSpecies}${DETAIL_SEPARATOR}${normalizedEnclosureName}`;
}

export function formatExhibitEnclosureTypeLine(exhibit, enclosureType) {
   const normalizedExhibit = asTrimmedString(exhibit);
   const normalizedEnclosureType = normalizeDisplayDetail(enclosureType);

   if (!normalizedEnclosureType) {
      return normalizedExhibit;
   }

   return `${normalizedExhibit}${DETAIL_SEPARATOR}${normalizedEnclosureType}`;
}
