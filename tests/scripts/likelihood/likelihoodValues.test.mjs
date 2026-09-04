import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodValues } from '../../../scripts/likelihood/likelihoodValues.js';
import { RowAlerts } from '../../../scripts/itinerary/panel/rowAlerts.js';
import { ItineraryValidation } from '../../../scripts/itinerary/itineraryValidation.js';

test('Test_LikelihoodToPercent_TestIntegerApiValues_ExpectPercents', () => {
   assert.equal(LikelihoodValues.likelihoodToPercent(1), 1);
   assert.equal(LikelihoodValues.likelihoodToPercent(20), 20);
   assert.equal(LikelihoodValues.likelihoodToPercent(100), 100);
   assert.equal(LikelihoodValues.likelihoodToPercent(0), 0);
});

test('Test_LikelihoodToPercent_TestFractionalClientValues_ExpectScaled', () => {
   assert.equal(LikelihoodValues.likelihoodToPercent(0.25), 25);
   assert.equal(LikelihoodValues.likelihoodToPercent(0.9), 90);
});

test('Test_LikelihoodToFraction_TestLowSavedValues_ExpectPercentSemantics', () => {
   assert.equal(LikelihoodValues.likelihoodToFraction(1), 0.01);
   assert.equal(LikelihoodValues.likelihoodToFraction(20), 0.2);
});

test('Test_BuildAnimalAlert_TestOnePercentLikelihood_ExpectNotInflated', () => {
   const alert = RowAlerts.buildAnimalAlert({
      likelihoodBefore: 1,
      likelihoodAfter: 20,
   });

   assert.equal(
      alert.line,
      'Projected visibility changed from 1% to 20% on your new date.'
   );
});

test('Test_BuildItineraryValidationState_TestOnePercentRising_ExpectImproved', () => {
   const validation = ItineraryValidation.buildItineraryValidationState({
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

test('Test_LikelihoodToPercent_TestMissingValues_ExpectNull', () => {
   assert.equal(LikelihoodValues.likelihoodToPercent(null), null);
   assert.equal(LikelihoodValues.likelihoodToPercent(undefined), null);
   assert.equal(LikelihoodValues.likelihoodToPercent(''), null);
});
