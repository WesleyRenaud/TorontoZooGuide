import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsClient } from '../../../scripts/api/animalsClient.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../../scripts/guardians/guardiansTalkLinkedAnimalOpener.js';
import { SpeciesFragment } from '../../../scripts/overlays/speciesFragment.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_GetGuardiansTalkLinkedAnimal_TestTalk_ExpectFirst', () => {
   const first = { species: 'African Lion', exhibit: 'African Savanna' };
   const talk = {
      linked_animals: [
         first,
         { species: 'Amur Tiger', exhibit: 'Eurasia' },
      ],
   };

   const linked = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal(talk);

   assert.deepEqual(linked, first);
});


test('Test_GetGuardiansTalkLinkedAnimal_TestEmpty_ExpectNull', () => {
   const talk = {};

   const linked = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal(talk);

   assert.equal(linked, null);
});


test('Test_OpenGuardiansTalkLinkedAnimal_TestLinked_ExpectOverlayOpened', async () => {
   const originalGet = AnimalsClient.getAnimalInformation;
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   const opened = [];
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   AnimalsClient.getAnimalInformation = async (linked) => ({ species: linked.species });
   SpeciesFragment.openAnimalSpeciesOverlay = (animal, options) => {
      opened.push({ animal, options });
   };

   try {
      await GuardiansTalkLinkedAnimalOpener.openGuardiansTalkLinkedAnimal({
         linked_animals: [{ species, exhibit }],
      });

      assert.equal(opened.length, Position.SECOND);
      assert.equal(opened.at(Position.FIRST).animal.species, species);
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
