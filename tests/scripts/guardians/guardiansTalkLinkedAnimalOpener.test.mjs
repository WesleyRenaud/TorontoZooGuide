import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { SpeciesFragment } from '../../../scripts/overlays/speciesFragment.js';

test('Test_GetGuardiansTalkLinkedAnimal_TestTalk_ExpectFirstOrNull', () => {
   assert.deepEqual(
      GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal({
         linked_animals: [
            { species: 'African Lion', exhibit: 'African Savanna' },
            { species: 'Amur Tiger', exhibit: 'Eurasia' },
         ],
      }),
      { species: 'African Lion', exhibit: 'African Savanna' }
   );
   assert.equal(GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal({}), null);
});

test('Test_OpenGuardiansTalkLinkedAnimal_TestLinked_ExpectOverlayOpened', async () => {
   const originalGet = AnimalsClient.getAnimalInformation;
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   const opened = [];

   AnimalsClient.getAnimalInformation = async (linked) => ({ species: linked.species });
   SpeciesFragment.openAnimalSpeciesOverlay = (animal, options) => {
      opened.push({ animal, options });
   };

   try {
      await GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal({
         linked_animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
      });
      assert.equal(opened.length, 1);
      assert.equal(opened[0].animal.species, 'African Lion');
   } finally {
      AnimalsClient.getAnimalInformation = originalGet;
      SpeciesFragment.openAnimalSpeciesOverlay = originalOpen;
   }
});

test('Test_OpenGuardiansTalkLinkedAnimal_TestMissingLinked_ExpectNoOp', async () => {
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   let opened = false;
   SpeciesFragment.openAnimalSpeciesOverlay = () => { opened = true; };

   try {
      await GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal({});
      assert.equal(opened, false);
   } finally {
      SpeciesFragment.openAnimalSpeciesOverlay = originalOpen;
   }
});
