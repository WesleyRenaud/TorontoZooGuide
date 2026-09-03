import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodPresentation } from '../../../scripts/likelihood/likelihoodPresentation.js';

test('Test_GetLikelihoodPhrase_TestBoundaryValues_ExpectLabels', () => {
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(100), 'Very high');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(95), 'Very high');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(94), 'High');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(80), 'High');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(60), 'Medium');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(40), 'Moderate');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(20), 'Low');
   assert.equal(LikelihoodPresentation.getLikelihoodPhrase(19), 'Very low');
});
