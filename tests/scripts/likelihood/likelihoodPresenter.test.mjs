import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodPresenter } from '../../../scripts/likelihood/likelihoodPresenter.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_GetLikelihoodPhrase_TestMaximum_ExpectVeryHigh', () => {
   const likelihood = LikelihoodScale.MAX_LIKELIHOOD;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.FIRST).label);
});


test('Test_GetLikelihoodPhrase_TestVeryHighMinimum_ExpectVeryHigh', () => {
   const veryHigh = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.FIRST);
   const likelihood = veryHigh.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, veryHigh.label);
});


test('Test_GetLikelihoodPhrase_TestBelowVeryHigh_ExpectHigh', () => {
   const veryHigh = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.FIRST);
   const high = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.SECOND);
   const likelihood = veryHigh.minimum - 1;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, high.label);
});


test('Test_GetLikelihoodPhrase_TestHighMinimum_ExpectHigh', () => {
   const high = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.SECOND);
   const likelihood = high.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, high.label);
});


test('Test_GetLikelihoodPhrase_TestMediumMinimum_ExpectMedium', () => {
   const medium = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.THIRD);
   const likelihood = medium.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, medium.label);
});


test('Test_GetLikelihoodPhrase_TestModerateMinimum_ExpectModerate', () => {
   const moderate = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.FOURTH);
   const likelihood = moderate.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, moderate.label);
});


test('Test_GetLikelihoodPhrase_TestLowMinimum_ExpectLow', () => {
   const low = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.LAST - 1);
   const likelihood = low.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, low.label);
});


test('Test_GetLikelihoodPhrase_TestBelowLow_ExpectVeryLow', () => {
   const low = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.LAST - 1);
   const likelihood = low.minimum - 1;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.LAST).label);
});
