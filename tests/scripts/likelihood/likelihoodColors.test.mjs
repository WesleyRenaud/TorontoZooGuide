import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodColors } from '../../../scripts/likelihood/likelihoodColors.js';

test('Test_LikelihoodToColor_TestBoundaryValues_ExpectEndpoints', () => {
   assert.equal(LikelihoodColors.likelihoodToColor(0), '#7a0000');
   assert.equal(LikelihoodColors.likelihoodToColor(100), '#1fa544');
   assert.equal(LikelihoodColors.likelihoodToColor(-10), '#7a0000');
   assert.equal(LikelihoodColors.likelihoodToColor(150), '#1fa544');
});
