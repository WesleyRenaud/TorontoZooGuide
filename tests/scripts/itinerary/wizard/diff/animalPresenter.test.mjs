import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalPresenter } from '../../../../../scripts/itinerary/wizard/diff/animalPresenter.js';

test('Test_BuildAnimalVisibilityChanges_TestReducedAndImproved_ExpectBuckets', () => {
   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      [
         { species: 'African Lion', likelihood: 80 },
         { species: 'Amur Tiger', likelihood: 20 },
         { species: 'Giraffe', likelihood: 50 },
      ],
      [
         { species: 'African Lion', likelihood: 20 },
         { species: 'Amur Tiger', likelihood: 80 },
         { species: 'Giraffe', likelihood: 55 },
      ],
      [{ species: 'Giraffe' }],
      0.2
   );

   assert.equal(result.reduced.length, 1);
   assert.equal(result.reduced[0].species, 'African Lion');
   assert.equal(result.improved.length, 1);
   assert.equal(result.improved[0].species, 'Amur Tiger');
});

test('Test_BuildAnimalVisibilityChanges_TestBelowMinDelta_ExpectEmpty', () => {
   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      [{ species: 'African Lion', likelihood: 50 }],
      [{ species: 'African Lion', likelihood: 55 }],
      [],
      0.2
   );

   assert.deepEqual(result, { reduced: [], improved: [] });
});

test('Test_BuildAnimalVisibilityChanges_TestMissingValidatedOrLikelihood_ExpectSkipped', () => {
   const result = AnimalPresenter.buildAnimalVisibilityChanges(
      [
         { species: 'African Lion', likelihood: 80 },
         { species: 'Amur Tiger', likelihood: null },
         { species: 'Giraffe' },
      ],
      [
         { species: 'Amur Tiger', likelihood: null },
         { species: 'Giraffe', likelihood: 40 },
      ],
      [],
      0.2
   );

   assert.deepEqual(result, { reduced: [], improved: [] });
});
