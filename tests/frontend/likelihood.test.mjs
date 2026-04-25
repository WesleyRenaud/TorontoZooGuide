import assert from 'node:assert/strict';
import test from 'node:test';

import { getLikelihoodPhrase } from '../../scripts/likelihood/likelihoodPresentation.js';
import {
   clampLikelihood,
   MAX_LIKELIHOOD,
   MIN_LIKELIHOOD,
} from '../../scripts/likelihood/likelihoodScale.js';

test('clamps likelihood values to the supported percentage range', () => {
   assert.equal(clampLikelihood(-10), MIN_LIKELIHOOD);
   assert.equal(clampLikelihood(30), 30);
   assert.equal(clampLikelihood('80'), 80);
   assert.equal(clampLikelihood(150), MAX_LIKELIHOOD);
   assert.equal(clampLikelihood('African Lion'), MIN_LIKELIHOOD);
});

test('labels likelihood phrase boundaries', () => {
   assert.equal(getLikelihoodPhrase(100), 'Very high');
   assert.equal(getLikelihoodPhrase(95), 'Very high');
   assert.equal(getLikelihoodPhrase(94), 'High');
   assert.equal(getLikelihoodPhrase(80), 'High');
   assert.equal(getLikelihoodPhrase(60), 'Medium');
   assert.equal(getLikelihoodPhrase(40), 'Moderate');
   assert.equal(getLikelihoodPhrase(20), 'Low');
   assert.equal(getLikelihoodPhrase(19), 'Very low');
});
