import { AnimalIdentity } from './animalIdentity.js';
import { EnclosureType } from '../shared/enums/enclosureType.js';

export class SpeciesExhibitKeyHelpers {
   static buildViewingSpotSuffix(animal = {}) {
      const { enclosure_name: enclosureName } = AnimalIdentity.normalizeAnimalIdentitySearchFields(animal);

      if (enclosureName) {
         return enclosureName;
      }

      const enclosureType = EnclosureType.normalizeEnclosureType(animal?.enclosure_type);

      return enclosureType ? enclosureType.toLowerCase() : '';
   }
}
