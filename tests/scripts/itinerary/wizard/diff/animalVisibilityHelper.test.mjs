import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalVisibilityHelper } from '../../../../../scripts/itinerary/wizard/diff/animalVisibilityHelper.js';


test('Test_GetAnimalLikelihood_TestPercent_ExpectFraction', () => {
   const likelihoodPercent = 50;
   const animal = { likelihood: likelihoodPercent };

   const likelihood = AnimalVisibilityHelper.getAnimalLikelihood(animal);

   assert.equal(likelihood, likelihoodPercent / 100);
});


test('Test_GetAnimalLikelihood_TestMissing_ExpectNull', () => {
   const animal = {};

   const likelihood = AnimalVisibilityHelper.getAnimalLikelihood(animal);

   assert.equal(likelihood, null);
});


test('Test_BuildAnimalsBySpecies_TestBestLikelihood_ExpectMap', () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const lowerLikelihood = 20;
   const higherLikelihood = 80;
   const tigerLikelihood = 40;
   const animals = [
      { species: lion, likelihood: lowerLikelihood },
      { species: lion, likelihood: higherLikelihood },
      { species: tiger, likelihood: tigerLikelihood },
      { species: '', likelihood: 90 },
   ];

   const bySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies(animals);

   assert.equal(bySpecies.size, 2);
   assert.equal(bySpecies.get(lion.toLowerCase()).likelihood, higherLikelihood);
   assert.equal(bySpecies.get(tiger.toLowerCase()).likelihood, tigerLikelihood);
});


test('Test_BuildAnimalsBySpecies_TestMissingLikelihoodKeepsCurrent_ExpectUnchanged', () => {
   const lion = 'African Lion';
   const likelihood = 70;
   const animals = [
      { species: lion, likelihood },
      { species: lion },
   ];

   const bySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies(animals);

   assert.equal(bySpecies.get(lion.toLowerCase()).likelihood, likelihood);
});


test('Test_BuildRemovedSpeciesKeys_TestAnimals_ExpectSet', () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const animals = [
      { species: lion },
      { species: tiger },
      { species: '' },
   ];

   const keys = AnimalVisibilityHelper.buildRemovedSpeciesKeys(animals);

   assert.equal(keys.has(lion.toLowerCase()), true);
   assert.equal(keys.has(tiger.toLowerCase()), true);
   assert.equal(keys.size, 2);
});
