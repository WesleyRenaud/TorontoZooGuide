import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodColors } from '../../../scripts/likelihood/likelihoodColors.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_LikelihoodToColor_TestMinimum_ExpectFirstColor', () => {
   const likelihood = LikelihoodScale.MIN_LIKELIHOOD;

   const color = LikelihoodColors.likelihoodToColor(likelihood);

   assert.equal(color, LikelihoodColors.LIKELIHOOD_COLORS.at(Position.FIRST));
});


test('Test_LikelihoodToColor_TestMaximum_ExpectLastColor', () => {
   const likelihood = LikelihoodScale.MAX_LIKELIHOOD;

   const color = LikelihoodColors.likelihoodToColor(likelihood);

   assert.equal(color, LikelihoodColors.LIKELIHOOD_COLORS.at(Position.LAST));
});


test('Test_LikelihoodToColor_TestBelowMinimum_ExpectFirstColor', () => {
   const likelihood = LikelihoodScale.MIN_LIKELIHOOD - 10;

   const color = LikelihoodColors.likelihoodToColor(likelihood);

   assert.equal(color, LikelihoodColors.LIKELIHOOD_COLORS.at(Position.FIRST));
});


test('Test_LikelihoodToColor_TestAboveMaximum_ExpectLastColor', () => {
   const likelihood = LikelihoodScale.MAX_LIKELIHOOD + 50;

   const color = LikelihoodColors.likelihoodToColor(likelihood);

   assert.equal(color, LikelihoodColors.LIKELIHOOD_COLORS.at(Position.LAST));
});
