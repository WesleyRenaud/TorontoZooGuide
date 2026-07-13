import { getAnimalInformation } from '../api/animalsApi.js';
import { normalizeGuardiansTalkLinkedAnimals } from './normalizeGuardiansTalkLinkedAnimals.js';
import { openAnimalSpeciesOverlay } from '../overlays/speciesOverlay.js';

export function getGuardiansTalkLinkedAnimal(talk = {}) {
   return normalizeGuardiansTalkLinkedAnimals(talk.linked_animals)[0] ?? null;
}

export async function openGuardiansTalkLinkedAnimal(talk) {
   const linked = getGuardiansTalkLinkedAnimal(talk);

   if (!linked) {
      return;
   }

   const animal = await getAnimalInformation(linked);

   if (animal) {
      openAnimalSpeciesOverlay(animal);
   }
}
