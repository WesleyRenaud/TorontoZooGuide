import { AnimalsClient } from '../api/animalsClient.js';
import { GuardiansTalkLinkedAnimalNormalizer } from './guardiansTalkLinkedAnimalNormalizer.js';
import { SpeciesFragment } from '../overlays/speciesFragment.js';

export class GuardiansTalkLinkedAnimalOpener {
   static getGuardiansTalkLinkedAnimal(talk = {}) {
      return GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(
         talk.linked_animals
      )[0] ?? null;
   }

   static async openGuardiansTalkLinkedAnimal(talk) {
      const linkedAnimals = GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(
         talk.linked_animals
      );
      const linked = linkedAnimals[0];

      if (!linked) {
         return;
      }

      const animal = await AnimalsClient.getAnimalInformation(linked);

      if (animal) {
         SpeciesFragment.openAnimalSpeciesOverlay(animal, { linkedAnimals });
      }
   }
}
