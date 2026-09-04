import { AnimalIdentity } from '../../animalIdentity.js';
import { AnimalDisplayLines } from '../../../animals/animalDisplayLines.js';
import { AssetKeyNormalizer } from '../../../assets/assetKeyNormalizer.js';
import { StoredSelection } from '../base/storedSelection.js';
import { EnclosureType } from '../../../shared/enums/enclosureType.js';

function normalizeLegacyStoredSpecies(item) {
   return StoredSelection.normalizeStoredString(item.species)
      || StoredSelection.normalizeStoredString(item.SPECIES);
}

function normalizeLegacyStoredExhibit(item) {
   return StoredSelection.normalizeStoredString(item.exhibit)
      || StoredSelection.normalizeStoredString(item.EXHIBIT);
}

function normalizeLegacyStoredImageSrc(item) {
   return StoredSelection.normalizeStoredLink(item.imageSrc)
      || StoredSelection.normalizeStoredLink(item.image_src)
      || StoredSelection.normalizeStoredLink(item.image);
}

function createStoredAnimalFromString(item) {
   const species = StoredSelection.normalizeStoredString(item);

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
   const enclosureName = AnimalIdentity.normalizeAnimalIdentityFields(item).enclosure_name;
   const defaultId = enclosureName
      ? `${species}||${exhibit}||${enclosureName}`
      : `${species}||${exhibit}`;
   const id = StoredSelection.normalizeStoredId(item.id, defaultId);

   if (!id) {
      return null;
   }

   return {
      id,
      species,
      exhibit,
      ...(enclosureName ? { enclosure_name: enclosureName } : {}),
      imageSrc: normalizeLegacyStoredImageSrc(item),
   };
}

export class AnimalSelectorModel {
   static OFF_DISPLAY_WARNING_THRESHOLD = 80;

   static getAnimalSpecies(row) {
      return AnimalIdentity.normalizeAnimalIdentityFields(row).species;
   }

   static getAnimalExhibit(row) {
      return AnimalIdentity.normalizeAnimalIdentityFields(row).exhibit;
   }

   static getAnimalStoredEnclosureName(row) {
      return AnimalIdentity.normalizeAnimalIdentityFields(row).enclosure_name;
   }

   static getAnimalEnclosureName(row) {
      return AnimalSelectorModel.getAnimalStoredEnclosureName(row);
   }

   static getAnimalEnclosureType(row) {
      return EnclosureType.normalizeEnclosureType(row?.enclosure_type) ?? '';
   }

   static getAnimalTitleLine(row) {
      return AnimalDisplayLines.formatSpeciesEnclosureLine(
         AnimalSelectorModel.getAnimalSpecies(row),
         AnimalSelectorModel.getAnimalEnclosureName(row)
      );
   }

   static getAnimalId(row) {
      const species = AnimalSelectorModel.getAnimalSpecies(row);
      const exhibit = AnimalSelectorModel.getAnimalExhibit(row);
      const enclosureName = AnimalSelectorModel.getAnimalStoredEnclosureName(row);
      const base = `${species}||${exhibit}`;

      return enclosureName ? `${base}||${enclosureName}` : base;
   }

   static getAnimalLikelihood(row) {
      const value = row?.likelihood ?? null;
      const numberValue = Number(value);
      return Number.isFinite(numberValue) ? numberValue : null;
   }

   static getAnimalLikelihoodLevel(row) {
      const likelihood = AnimalSelectorModel.getAnimalLikelihood(row);

      if (likelihood === null) {
         return null;
      }

      if (likelihood < 40) {
         return 'low';
      }

      if (likelihood < AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD) {
         return 'medium';
      }

      return null;
   }

   static isLikelyOffDisplayAnimal(
      row,
      threshold = AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD
   ) {
      const likelihood = AnimalSelectorModel.getAnimalLikelihood(row);
      return likelihood !== null && likelihood < threshold;
   }

   static getAnimalSubtitle(row) {
      return AnimalSelectorModel.getAnimalExhibit(row);
   }

   static buildAnimalImageSrc(row) {
      const exhibitFile = AssetKeyNormalizer.normalize(
         AnimalSelectorModel.getAnimalExhibit(row)
      );
      const speciesFile = AssetKeyNormalizer.normalize(
         AnimalSelectorModel.getAnimalSpecies(row)
      );

      if (!exhibitFile || !speciesFile) {
         return null;
      }

      return `../images/details/animals/${exhibitFile}/${speciesFile}.png`;
   }

   static migrateStoredAnimals(items) {
      return StoredSelection.migrateStoredSelectionItems(items, {
         fromString: createStoredAnimalFromString,
         fromObject: createStoredAnimalFromObject,
      });
   }

   static makeAnimalSelection(row) {
      const species = AnimalSelectorModel.getAnimalSpecies(row);
      const exhibit = AnimalSelectorModel.getAnimalExhibit(row);
      const enclosureName = AnimalSelectorModel.getAnimalStoredEnclosureName(row);

      return {
         id: AnimalSelectorModel.getAnimalId(row),
         species,
         exhibit,
         ...(enclosureName ? { enclosure_name: enclosureName } : {}),
         imageSrc: AnimalSelectorModel.buildAnimalImageSrc(row),
      };
   }

   static buildOffDisplayWarningMessage(row) {
      const species = AnimalSelectorModel.getAnimalSpecies(row) || 'This animal';
      const likelihood = AnimalSelectorModel.getAnimalLikelihood(row);

      if (likelihood === null) {
         return `The ${species} may be off display on your visit date. Do you still want to add it to your itinerary?`;
      }

      return `The ${species} has a viewing likelihood below ${AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD}% (${likelihood}%) for your visit date and may be off display. Do you still want to add it to your itinerary?`;
   }
}
