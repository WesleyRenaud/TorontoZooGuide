import { AnimalsApi } from '../api/animalsApi.js';
import { NormalizeGuardiansTalkLinkedAnimals } from './normalizeGuardiansTalkLinkedAnimals.js';
import { openAnimalSpeciesOverlay } from '../overlays/speciesOverlay.js';

export class OpenGuardiansTalkLinkedAnimal {
   static getGuardiansTalkLinkedAnimal(talk = {}) {
      return NormalizeGuardiansTalkLinkedAnimals.normalizeGuardiansTalkLinkedAnimals(
         talk.linked_animals
      )[0] ?? null;
   }

   static async openGuardiansTalkLinkedAnimal(talk) {
      const linkedAnimals = NormalizeGuardiansTalkLinkedAnimals.normalizeGuardiansTalkLinkedAnimals(
         talk.linked_animals
      );
      const linked = linkedAnimals[0];

      if (!linked) {
         return;
      }

      const animal = await AnimalsApi.getAnimalInformation(linked);

      if (animal) {
         openAnimalSpeciesOverlay(animal, { linkedAnimals });
      }
   }
}
