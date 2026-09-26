import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodValues } from '../../../../scripts/likelihood/likelihoodValues.js';
import { RowAlertsBuilder } from '../../../../scripts/itinerary/panel/rowAlertsBuilder.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_GetLikelihoodPair_TestPercents_ExpectPair', () => {
   const animal = {
      likelihoodBefore: 40,
      likelihoodAfter: 70,
   };

   const pair = RowAlertsBuilder.getLikelihoodPair(animal);

   assert.deepEqual(pair, {
      before: LikelihoodValues.likelihoodToPercent(animal.likelihoodBefore),
      after: LikelihoodValues.likelihoodToPercent(animal.likelihoodAfter),
   });
});


test('Test_BuildAnimalRemovalReasonLine_TestEmpty_ExpectEmpty', () => {
   const animal = {};

   const line = RowAlertsBuilder.buildAnimalRemovalReasonLine(animal);

   assert.equal(line, '');
});


test('Test_BuildAnimalRemovalReasonLine_TestReason_ExpectUnavailable', () => {
   const reason = 'Closed exhibit';
   const animal = { removalReason: reason };

   const line = RowAlertsBuilder.buildAnimalRemovalReasonLine(animal);

   assert.equal(line, Strings.itinerary.removedItems.unavailableReason(animal.removalReason));
});


test('Test_BuildAnimalVisibilityChange_TestDecrease_ExpectDefaultTone', () => {
   const animal = {
      likelihoodBefore: 80,
      likelihoodAfter: 20,
   };

   const change = RowAlertsBuilder.buildAnimalVisibilityChange(animal);

   assert.deepEqual(change, {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(
         LikelihoodValues.likelihoodToPercent(animal.likelihoodBefore),
         LikelihoodValues.likelihoodToPercent(animal.likelihoodAfter)
      ),
      tone: 'default',
   });
});


test('Test_BuildAnimalVisibilityChange_TestIncrease_ExpectPositiveTone', () => {
   const animal = {
      likelihoodBefore: 20,
      likelihoodAfter: 80,
   };

   const change = RowAlertsBuilder.buildAnimalVisibilityChange(animal);

   assert.deepEqual(change, {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(
         LikelihoodValues.likelihoodToPercent(animal.likelihoodBefore),
         LikelihoodValues.likelihoodToPercent(animal.likelihoodAfter)
      ),
      tone: 'positive',
   });
});


test('Test_BuildAnimalVisibilityChange_TestUnchanged_ExpectEmpty', () => {
   const likelihood = 50;
   const animal = {
      likelihoodBefore: likelihood,
      likelihoodAfter: likelihood,
   };

   const change = RowAlertsBuilder.buildAnimalVisibilityChange(animal);

   assert.deepEqual(change, { line: '', tone: 'default' });
});
