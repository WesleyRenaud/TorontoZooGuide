import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalPresenter } from '../../../../../scripts/itinerary/wizard/diff/animalPresenter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_BuildAnimalVisibilityChanges_TestReducedAndImproved_ExpectBuckets', () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const giraffe = 'Masai Giraffe';
   const minDelta = 0.2;
   const previousAnimals = [
      { species: lion, likelihood: 80 },
      { species: tiger, likelihood: 20 },
      { species: giraffe, likelihood: 50 },
   ];
   const validatedAnimals = [
      { species: lion, likelihood: 20 },
      { species: tiger, likelihood: 80 },
      { species: giraffe, likelihood: 55 },
   ];
   const removedAnimals = [{ species: giraffe }];

   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      previousAnimals,
      validatedAnimals,
      removedAnimals,
      minDelta
   );

   assert.equal(result.reduced.length, 1);
   assert.equal(result.reduced[Position.FIRST].species, lion);
   assert.equal(result.improved.length, 1);
   assert.equal(result.improved[Position.FIRST].species, tiger);
});


test('Test_BuildAnimalVisibilityChanges_TestBelowMinDelta_ExpectEmpty', () => {
   const lion = 'African Lion';
   const minDelta = 0.2;
   const previousAnimals = [{ species: lion, likelihood: 50 }];
   const validatedAnimals = [{ species: lion, likelihood: 55 }];

   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      previousAnimals,
      validatedAnimals,
      [],
      minDelta
   );

   assert.deepEqual(result, { reduced: [], improved: [] });
});


test('Test_BuildAnimalVisibilityChanges_TestMissingValidatedOrLikelihood_ExpectSkipped', () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const giraffe = 'Masai Giraffe';
   const minDelta = 0.2;
   const previousAnimals = [
      { species: lion, likelihood: 80 },
      { species: tiger, likelihood: null },
      { species: giraffe },
   ];
   const validatedAnimals = [
      { species: tiger, likelihood: null },
      { species: giraffe, likelihood: 40 },
   ];

   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      previousAnimals,
      validatedAnimals,
      [],
      minDelta
   );

   assert.deepEqual(result, { reduced: [], improved: [] });
});
