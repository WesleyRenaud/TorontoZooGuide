import assert from 'node:assert/strict';
import test from 'node:test';

import { StepRounder } from '../../../scripts/shared/stepRounder.js';


test('Test_RoundToStep_TestBelowHalf_ExpectLowerStep', () => {
   const value = 7;
   const step = 5;

   const rounded = StepRounder.roundToStep(value, step);

   assert.equal(rounded, step);
});


test('Test_RoundToStep_TestAboveHalf_ExpectHigherStep', () => {
   const value = 8;
   const step = 5;

   const rounded = StepRounder.roundToStep(value, step);

   assert.equal(rounded, step * 2);
});


test('Test_RoundToStep_TestExactStep_ExpectSame', () => {
   const value = 600;
   const step = 5;

   const rounded = StepRounder.roundToStep(value, step);

   assert.equal(rounded, value);
});
