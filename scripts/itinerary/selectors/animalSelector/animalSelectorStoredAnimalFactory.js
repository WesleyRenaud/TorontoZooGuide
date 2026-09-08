import { AnimalIdentity } from '../../animalIdentity.js';
import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';

export class AnimalSelectorStoredAnimalFactory {
   static normalizeLegacyStoredSpecies(item) {
      return StoredSelectionNormalizer.normalizeStoredString(item.species)
         || StoredSelectionNormalizer.normalizeStoredString(item.SPECIES);
   }

   static normalizeLegacyStoredExhibit(item) {
      return StoredSelectionNormalizer.normalizeStoredString(item.exhibit)
         || StoredSelectionNormalizer.normalizeStoredString(item.EXHIBIT);
   }

   static normalizeLegacyStoredImageSrc(item) {
      return StoredSelectionNormalizer.normalizeStoredLink(item.imageSrc)
         || StoredSelectionNormalizer.normalizeStoredLink(item.image_src)
         || StoredSelectionNormalizer.normalizeStoredLink(item.image);
   }

   static createStoredAnimalFromString(item) {
      const species = StoredSelectionNormalizer.normalizeStoredString(item);

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

   static createStoredAnimalFromObject(item) {
      const species = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredSpecies(item);
      const exhibit = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredExhibit(item);
      const enclosureName = AnimalIdentity.normalizeAnimalIdentityFields(item).enclosure_name;
      const defaultId = enclosureName
         ? `${species}||${exhibit}||${enclosureName}`
         : `${species}||${exhibit}`;
      const id = StoredSelectionNormalizer.normalizeStoredId(item.id, defaultId);

      if (!id) {
         return null;
      }

      return {
         id,
         species,
         exhibit,
         ...(enclosureName ? { enclosure_name: enclosureName } : {}),
         imageSrc: AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredImageSrc(item),
      };
   }
}
