import { AnimalIdentity } from '../../animalIdentity.js';
import { AnimalDisplayFormatter } from '../../../animals/animalDisplayFormatter.js';
import { AnimalSelectorStoredAnimalFactory } from './animalSelectorStoredAnimalFactory.js';
import { AssetKeyNormalizer } from '../../../assets/assetKeyNormalizer.js';
import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { EnclosureType } from '../../../shared/enums/enclosureType.js';
import { Strings } from '../../../strings.js';

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
      return AnimalDisplayFormatter.formatSpeciesEnclosureLine(
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
      return StoredSelectionNormalizer.migrateStoredSelectionItems(items, {
         fromString: AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString,
         fromObject: AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject,
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
      const species = AnimalSelectorModel.getAnimalSpecies(row)
         || Strings.itinerary.confirmation.animalFallbackName;
      const likelihood = AnimalSelectorModel.getAnimalLikelihood(row);

      if (likelihood === null) {
         return Strings.itinerary.confirmation.animalOffDisplayUnknownLikelihoodMessage(species);
      }

      return Strings.itinerary.confirmation.animalOffDisplayLowLikelihoodMessage(
         species,
         AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD,
         likelihood
      );
   }
}
