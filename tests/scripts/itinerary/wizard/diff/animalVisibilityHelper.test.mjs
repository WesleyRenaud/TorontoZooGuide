import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalVisibilityHelper } from '../../../../../scripts/itinerary/wizard/diff/animalVisibilityHelper.js';

test('Test_GetAnimalLikelihood_TestPercent_ExpectFraction', () => {
   assert.equal(AnimalVisibilityHelper.getAnimalLikelihood({ likelihood: 50 }), 0.5);
   assert.equal(AnimalVisibilityHelper.getAnimalLikelihood({}), null);
});

test('Test_BuildAnimalsBySpecies_TestBestLikelihood_ExpectMap', () => {
   const bySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies([
      { species: 'African Lion', likelihood: 20 },
      { species: 'African Lion', likelihood: 80 },
      { species: 'Amur Tiger', likelihood: 40 },
      { species: '', likelihood: 90 },
   ]);

   assert.equal(bySpecies.size, 2);
   assert.equal(bySpecies.get('african lion').likelihood, 80);
   assert.equal(bySpecies.get('amur tiger').likelihood, 40);
});

test('Test_BuildAnimalsBySpecies_TestMissingLikelihoodKeepsCurrent_ExpectUnchanged', () => {
   const bySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies([
      { species: 'African Lion', likelihood: 70 },
      { species: 'African Lion' },
   ]);

   assert.equal(bySpecies.get('african lion').likelihood, 70);
});

test('Test_BuildRemovedSpeciesKeys_TestAnimals_ExpectSet', () => {
   const keys = AnimalVisibilityHelper.buildRemovedSpeciesKeys([
      { species: 'African Lion' },
      { species: 'Amur Tiger' },
      { species: '' },
   ]);

   assert.equal(keys.has('african lion'), true);
   assert.equal(keys.has('amur tiger'), true);
   assert.equal(keys.size, 2);
});
