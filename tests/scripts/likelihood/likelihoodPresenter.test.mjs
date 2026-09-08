import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodPresenter } from '../../../scripts/likelihood/likelihoodPresenter.js';

test('Test_GetLikelihoodPhrase_TestBoundaryValues_ExpectLabels', () => {
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(100), 'Very high');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(95), 'Very high');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(94), 'High');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(80), 'High');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(60), 'Medium');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(40), 'Moderate');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(20), 'Low');
   assert.equal(LikelihoodPresenter.getLikelihoodPhrase(19), 'Very low');
});
