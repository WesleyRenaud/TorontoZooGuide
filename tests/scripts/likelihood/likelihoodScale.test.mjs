import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';

test('Test_ClampLikelihood_TestOutOfRangeAndInvalid_ExpectClamped', () => {
   assert.equal(LikelihoodScale.clampLikelihood(-10), LikelihoodScale.MIN_LIKELIHOOD);
   assert.equal(LikelihoodScale.clampLikelihood(30), 30);
   assert.equal(LikelihoodScale.clampLikelihood('80'), 80);
   assert.equal(LikelihoodScale.clampLikelihood(150), LikelihoodScale.MAX_LIKELIHOOD);
   assert.equal(LikelihoodScale.clampLikelihood('African Lion'), LikelihoodScale.MIN_LIKELIHOOD);
});
