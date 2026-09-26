import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';


test('Test_ClampLikelihood_TestBelowMinimum_ExpectMin', () => {
   const likelihood = LikelihoodScale.MIN_LIKELIHOOD - 10;

   const clamped = LikelihoodScale.clampLikelihood(likelihood);

   assert.equal(clamped, LikelihoodScale.MIN_LIKELIHOOD);
});


test('Test_ClampLikelihood_TestInRange_ExpectSame', () => {
   const likelihood = 30;

   const clamped = LikelihoodScale.clampLikelihood(likelihood);

   assert.equal(clamped, likelihood);
});


test('Test_ClampLikelihood_TestNumericString_ExpectNumber', () => {
   const likelihood = '80';

   const clamped = LikelihoodScale.clampLikelihood(likelihood);

   assert.equal(clamped, Number(likelihood));
});


test('Test_ClampLikelihood_TestAboveMaximum_ExpectMax', () => {
   const likelihood = LikelihoodScale.MAX_LIKELIHOOD + 50;

   const clamped = LikelihoodScale.clampLikelihood(likelihood);

   assert.equal(clamped, LikelihoodScale.MAX_LIKELIHOOD);
});


test('Test_ClampLikelihood_TestNonNumeric_ExpectMin', () => {
   const likelihood = 'African Lion';

   const clamped = LikelihoodScale.clampLikelihood(likelihood);

   assert.equal(clamped, LikelihoodScale.MIN_LIKELIHOOD);
});
