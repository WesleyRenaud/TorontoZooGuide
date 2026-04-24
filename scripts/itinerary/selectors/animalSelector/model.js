import { normalizeAssetKey } from '../../../assets/normalizeAssetKey.js';
import {
   migrateStoredSelectionItems,
   normalizeStoredId,
   normalizeStoredLink,
   normalizeStoredString,
} from '../base/storedSelection.js';

export const OFF_DISPLAY_WARNING_THRESHOLD = 80;

export function getAnimalSpecies(row) {
   return typeof row?.species === 'string'
      ? row.species
      : '';
}

export function getAnimalExhibit(row) {
   return typeof row?.exhibit === 'string'
      ? row.exhibit
      : '';
}

export function getAnimalId(row) {
   return `${getAnimalSpecies(row)}||${getAnimalExhibit(row)}`;
}

export function getAnimalLikelihood(row) {
   const value = row?.likelihood ?? null;
   const numberValue = Number(value);
   return Number.isFinite(numberValue) ? numberValue : null;
}

export function getAnimalLikelihoodLevel(row) {
   const likelihood = getAnimalLikelihood(row);

   if (likelihood === null) {
      return null;
   }

   if (likelihood < 40) {
      return 'low';
   }

   if (likelihood < OFF_DISPLAY_WARNING_THRESHOLD) {
      return 'medium';
   }

   return null;
}

export function isLikelyOffDisplayAnimal(row, threshold = OFF_DISPLAY_WARNING_THRESHOLD) {
   const likelihood = getAnimalLikelihood(row);
   return likelihood !== null && likelihood < threshold;
}

export function getAnimalSubtitle(row) {
   const exhibit = getAnimalExhibit(row);
   return exhibit ? `Exhibit: ${exhibit}` : '';
}

export function buildAnimalImageSrc(row) {
   const exhibitFile = normalizeAssetKey(getAnimalExhibit(row));
   const speciesFile = normalizeAssetKey(getAnimalSpecies(row));

   if (!exhibitFile || !speciesFile) {
      return null;
   }

   return `../images/animals/${exhibitFile}/${speciesFile}.png`;
}

function normalizeLegacyStoredSpecies(item) {
   return normalizeStoredString(item.species)
      || normalizeStoredString(item.SPECIES);
}

function normalizeLegacyStoredExhibit(item) {
   return normalizeStoredString(item.exhibit)
      || normalizeStoredString(item.EXHIBIT);
}

function normalizeLegacyStoredImageSrc(item) {
   return normalizeStoredLink(item.imageSrc)
      || normalizeStoredLink(item.image_src)
      || normalizeStoredLink(item.image);
}

function createStoredAnimalFromString(item) {
   const species = normalizeStoredString(item);

   if (!species) {
      return null;
   }

   return {
      id: `${species}||`,
      species,
      exhibit: '',
      imageSrc: null,
   };
}

function createStoredAnimalFromObject(item) {
   const species = normalizeLegacyStoredSpecies(item);
   const exhibit = normalizeLegacyStoredExhibit(item);
   const id = normalizeStoredId(item.id, `${species}||${exhibit}`);

   if (!id) {
      return null;
   }

   return {
      id,
      species,
      exhibit,
      imageSrc: normalizeLegacyStoredImageSrc(item),
   };
}

export function migrateStoredAnimals(items) {
   return migrateStoredSelectionItems(items, {
      fromString: createStoredAnimalFromString,
      fromObject: createStoredAnimalFromObject,
   });
}

export function makeAnimalSelection(row) {
   return {
      id: getAnimalId(row),
      species: getAnimalSpecies(row),
      exhibit: getAnimalExhibit(row),
      imageSrc: buildAnimalImageSrc(row),
   };
}

export function buildOffDisplayWarningMessage(row) {
   const species = getAnimalSpecies(row) || 'This animal';
   const likelihood = getAnimalLikelihood(row);

   if (likelihood === null) {
      return `The ${species} may be off display on your visit date. Do you still want to add it to your itinerary?`;
   }

   return `The ${species} has a viewing likelihood below ${OFF_DISPLAY_WARNING_THRESHOLD}% (${likelihood}%) for your visit date and may be off display. Do you still want to add it to your itinerary?`;
}
