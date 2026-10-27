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


test('Test_ToGradient_TestScale_ExpectEachColorInOrder', () => {
   const colors = LikelihoodColors.LIKELIHOOD_COLORS;
   const lastIndex = colors.length - 1;

   const gradient = LikelihoodColors.toGradient();

   assert.equal(gradient.startsWith('linear-gradient(to right, '), true);
   assert.equal(gradient.includes(`${colors.at(Position.FIRST)} 0%`), true);
   assert.equal(gradient.endsWith(`${colors.at(Position.LAST)} 100%)`), true);
   assert.equal(
      gradient.includes(`${colors[1]} ${(1 / lastIndex) * 100}%`),
      true
   );
   assert.equal(gradient.split('#').length - 1, colors.length);
});
