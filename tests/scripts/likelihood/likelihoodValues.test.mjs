import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryValidator } from '../../../scripts/itinerary/itineraryValidator.js';
import { RowAlertPresenter } from '../../../scripts/itinerary/panel/rowAlertPresenter.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
import { LikelihoodValues } from '../../../scripts/likelihood/likelihoodValues.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_LikelihoodToPercent_TestOne_ExpectSame', () => {
   const value = 1;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value);
});


test('Test_LikelihoodToPercent_TestInteger_ExpectSame', () => {
   const value = 20;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value);
});


test('Test_LikelihoodToPercent_TestMaximum_ExpectSame', () => {
   const value = LikelihoodScale.MAX_LIKELIHOOD;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value);
});


test('Test_LikelihoodToPercent_TestZero_ExpectSame', () => {
   const value = 0;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value);
});


test('Test_LikelihoodToPercent_TestQuarterFraction_ExpectScaled', () => {
   const value = 0.25;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value * 100);
});


test('Test_LikelihoodToPercent_TestHighFraction_ExpectScaled', () => {
   const value = 0.9;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value * 100);
});


test('Test_LikelihoodToFraction_TestOne_ExpectPercentSemantics', () => {
   const value = 1;

   const fraction = LikelihoodValues.likelihoodToFraction(value);

   assert.equal(fraction, LikelihoodValues.likelihoodToPercent(value) / 100);
});


test('Test_LikelihoodToFraction_TestInteger_ExpectPercentSemantics', () => {
   const value = 20;

   const fraction = LikelihoodValues.likelihoodToFraction(value);

   assert.equal(fraction, LikelihoodValues.likelihoodToPercent(value) / 100);
});


test('Test_BuildAnimalAlert_TestOnePercentLikelihood_ExpectNotInflated', () => {
   const likelihoodBefore = 1;
   const likelihoodAfter = 20;

   const alert = RowAlertPresenter.buildAnimalAlert({
      likelihoodBefore,
      likelihoodAfter,
   });

   assert.equal(
      alert.line,
      Strings.itinerary.removedItems.projectedVisibilityChanged(
         LikelihoodValues.likelihoodToPercent(likelihoodBefore),
         LikelihoodValues.likelihoodToPercent(likelihoodAfter)
      )
   );
});


test('Test_BuildItineraryValidationState_TestOnePercentRising_ExpectImproved', () => {
   const species = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const oldLikelihood = 1;
   const likelihood = 25;
   const threshold = 20;

   const validation = ItineraryValidator.buildItineraryValidationState({
      animals: [
         {
            species,
            exhibit,
            old_likelihood: oldLikelihood,
            likelihood,
         },
      ],
   }, { animalVisibilityChangeThreshold: threshold });

   assert.deepEqual(
      validation.improvedVisibility.animals.map((animal) => animal.species),
      [species]
   );
   assert.deepEqual(validation.reducedVisibility.animals, []);
});


test('Test_LikelihoodToPercent_TestNull_ExpectNull', () => {
   const value = null;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, null);
});


test('Test_LikelihoodToPercent_TestUndefined_ExpectNull', () => {
   const value = undefined;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, null);
});


test('Test_LikelihoodToPercent_TestEmptyString_ExpectNull', () => {
   const value = '';

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, null);
});


test('Test_LikelihoodToPercent_TestNonNumeric_ExpectNull', () => {
   const value = 'not-a-number';

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, null);
});


test('Test_LikelihoodToPercent_TestNaN_ExpectNull', () => {
   const value = Number.NaN;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, null);
});


test('Test_LikelihoodToPercent_TestNonIntegerOutsideUnit_ExpectSame', () => {
   const value = 12.5;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, value);
});


test('Test_LikelihoodToPercent_TestAboveMaximum_ExpectClamped', () => {
   const value = LikelihoodScale.MAX_LIKELIHOOD + 50.5;

   const percent = LikelihoodValues.likelihoodToPercent(value);

   assert.equal(percent, LikelihoodScale.MAX_LIKELIHOOD);
});


test('Test_LikelihoodToFraction_TestNull_ExpectNull', () => {
   const value = null;

   const fraction = LikelihoodValues.likelihoodToFraction(value);

   assert.equal(fraction, null);
});


test('Test_LikelihoodToFraction_TestEmptyString_ExpectNull', () => {
   const value = '';

   const fraction = LikelihoodValues.likelihoodToFraction(value);

   assert.equal(fraction, null);
});
