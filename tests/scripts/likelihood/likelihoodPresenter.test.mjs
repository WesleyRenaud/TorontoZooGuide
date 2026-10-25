import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodPresenter } from '../../../scripts/likelihood/likelihoodPresenter.js';
import { LikelihoodScale } from '../../../scripts/likelihood/likelihoodScale.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { Strings } from '../../../scripts/strings.js';


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
   const likelihood = veryHigh.minimum - LikelihoodPresenter.DISPLAY_STEP;

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
   const likelihood = low.minimum - LikelihoodPresenter.DISPLAY_STEP;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.LAST).label);
});


test('Test_GetLikelihoodPhrase_TestJustBelowHigh_ExpectHigh', () => {
   const high = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.SECOND);
   const likelihood = high.minimum - (LikelihoodPresenter.DISPLAY_STEP / 2);
   const rounded = high.minimum;

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);
   const displayed = LikelihoodPresenter.formatDisplayedLikelihood(likelihood);

   assert.equal(phrase, high.label);
   assert.equal(displayed, Strings.format.approximate(`${rounded}%`));
});


test('Test_GetLikelihoodPhrase_TestRoundsBelowHigh_ExpectMedium', () => {
   const high = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.SECOND);
   const medium = LikelihoodPresenter.LIKELIHOOD_PHRASES.at(Position.THIRD);
   const halfStep = LikelihoodPresenter.DISPLAY_STEP / 2;
   const likelihood = high.minimum - halfStep - (halfStep / 2);

   const phrase = LikelihoodPresenter.getLikelihoodPhrase(likelihood);

   assert.equal(phrase, medium.label);
});


test('Test_GetLikelihoodPhrase_TestNull_ExpectNull', () => {
   const phrase = LikelihoodPresenter.getLikelihoodPhrase(null);

   assert.equal(phrase, null);
});


test('Test_FormatDisplayedLikelihood_TestZero_ExpectZero', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(LikelihoodScale.MIN_LIKELIHOOD);

   assert.equal(label, Strings.format.approximate(`${LikelihoodScale.MIN_LIKELIHOOD}%`));
});


test('Test_FormatDisplayedLikelihood_TestBetweenZeroAndFive_ExpectBelowFive', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(LikelihoodPresenter.LOW_OPEN_PERCENT - 1);

   assert.equal(label, Strings.likelihood.belowDisplayedMinimum(LikelihoodPresenter.LOW_OPEN_PERCENT));
});


test('Test_FormatDisplayedLikelihood_TestLowBoundary_ExpectFive', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(LikelihoodPresenter.LOW_OPEN_PERCENT);

   assert.equal(label, Strings.format.approximate(`${LikelihoodPresenter.LOW_OPEN_PERCENT}%`));
});


test('Test_FormatDisplayedLikelihood_TestNearestFive_ExpectRounded', () => {
   const belowStep = 7;
   const aboveStep = 8;

   assert.equal(
      LikelihoodPresenter.formatDisplayedLikelihood(belowStep),
      Strings.format.approximate(`${LikelihoodPresenter.DISPLAY_STEP}%`)
   );
   assert.equal(
      LikelihoodPresenter.formatDisplayedLikelihood(aboveStep),
      Strings.format.approximate(`${LikelihoodPresenter.DISPLAY_STEP * 2}%`)
   );
});


test('Test_FormatDisplayedLikelihood_TestHighBoundary_ExpectNinetyFive', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(LikelihoodPresenter.HIGH_OPEN_PERCENT);

   assert.equal(label, Strings.format.approximate(`${LikelihoodPresenter.HIGH_OPEN_PERCENT}%`));
});


test('Test_FormatDisplayedLikelihood_TestAboveNinetyFive_ExpectAboveNinetyFive', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(LikelihoodScale.MAX_LIKELIHOOD);

   assert.equal(label, Strings.likelihood.aboveDisplayedMaximum(LikelihoodPresenter.HIGH_OPEN_PERCENT));
});


test('Test_FormatDisplayedLikelihood_TestNull_ExpectNull', () => {
   const label = LikelihoodPresenter.formatDisplayedLikelihood(null);

   assert.equal(label, null);
});
