import { AnimalIdentity } from '../../animalIdentity.js';
import { StoredSelection } from '../base/storedSelection.js';

export class AnimalSelectorStoredAnimalFactory {
   static normalizeLegacyStoredSpecies(item) {
      return StoredSelection.normalizeStoredString(item.species)
         || StoredSelection.normalizeStoredString(item.SPECIES);
   }

   static normalizeLegacyStoredExhibit(item) {
      return StoredSelection.normalizeStoredString(item.exhibit)
         || StoredSelection.normalizeStoredString(item.EXHIBIT);
   }

   static normalizeLegacyStoredImageSrc(item) {
      return StoredSelection.normalizeStoredLink(item.imageSrc)
         || StoredSelection.normalizeStoredLink(item.image_src)
         || StoredSelection.normalizeStoredLink(item.image);
   }

   static createStoredAnimalFromString(item) {
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

   static createStoredAnimalFromObject(item) {
      const species = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredSpecies(item);
      const exhibit = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredExhibit(item);
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
         imageSrc: AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredImageSrc(item),
      };
   }
}
