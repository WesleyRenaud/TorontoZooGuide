import assert from 'node:assert/strict';
import test from 'node:test';

import {
   likelihoodToFraction,
   likelihoodToPercent,
} from '../../scripts/likelihood/likelihoodValues.js';
import { buildAnimalAlert } from '../../scripts/itinerary/panel/rowAlerts.js';
import { buildItineraryValidationState } from '../../scripts/itinerary/itineraryValidation.js';

test('likelihoodToPercent treats integer API values as percents', () => {
   assert.equal(likelihoodToPercent(1), 1);
   assert.equal(likelihoodToPercent(20), 20);
   assert.equal(likelihoodToPercent(100), 100);
   assert.equal(likelihoodToPercent(0), 0);
});

test('likelihoodToPercent scales fractional client values', () => {
   assert.equal(likelihoodToPercent(0.25), 25);
   assert.equal(likelihoodToPercent(0.9), 90);
});

test('likelihoodToFraction matches percent semantics for low saved values', () => {
   assert.equal(likelihoodToFraction(1), 0.01);
   assert.equal(likelihoodToFraction(20), 0.2);
});

test('buildAnimalAlert does not inflate 1% saved likelihood to 100%', () => {
   const alert = buildAnimalAlert({
      likelihoodBefore: 1,
      likelihoodAfter: 20,
   });

   assert.equal(
      alert.line,
      'Projected visibility changed from 1% to 20% on your new date.'
   );
});

test('buildItineraryValidationState does not treat 1% as reduced when rising to 25%', () => {
   const validation = buildItineraryValidationState({
      animals: [
         {
            species: 'Marabou Stork',
            exhibit: 'Africa Savanna',
            old_likelihood: 1,
            likelihood: 25,
         },
      ],
   }, { animalVisibilityChangeThreshold: 20 });

   assert.deepEqual(
      validation.improvedVisibility.animals.map((animal) => animal.species),
      ['Marabou Stork']
   );
   assert.deepEqual(validation.reducedVisibility.animals, []);
});

test('likelihoodToPercent returns null for missing values', () => {
   assert.equal(likelihoodToPercent(null), null);
   assert.equal(likelihoodToPercent(undefined), null);
   assert.equal(likelihoodToPercent(''), null);
});
