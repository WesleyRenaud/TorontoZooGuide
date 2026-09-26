import assert from 'node:assert/strict';
import test from 'node:test';

import { LikelihoodValues } from '../../../../scripts/likelihood/likelihoodValues.js';
import { RowAlertPresenter } from '../../../../scripts/itinerary/panel/rowAlertPresenter.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_BuildAnimalAlert_TestRemovalReason_ExpectRemovalLine', () => {
   const reason = 'Closed exhibit';
   const animal = { removalReason: reason };

   const alert = RowAlertPresenter.buildAnimalAlert(animal);

   assert.deepEqual(alert, {
      line: Strings.itinerary.removedItems.unavailableReason(animal.removalReason),
      tone: 'default',
   });
});


test('Test_BuildAnimalAlert_TestVisibilityChange_ExpectVisibilityAlert', () => {
   const animal = {
      likelihoodBefore: 10,
      likelihoodAfter: 90,
   };

   const alert = RowAlertPresenter.buildAnimalAlert(animal);

   assert.deepEqual(alert, {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(
         LikelihoodValues.likelihoodToPercent(animal.likelihoodBefore),
         LikelihoodValues.likelihoodToPercent(animal.likelihoodAfter)
      ),
      tone: 'positive',
   });
});


test('Test_BuildAttractionRemovalReasonLine_TestEmpty_ExpectEmpty', () => {
   const attraction = {};

   const line = RowAlertPresenter.buildAttractionRemovalReasonLine(attraction);

   assert.equal(line, '');
});


test('Test_BuildAttractionRemovalReasonLine_TestReason_ExpectMessage', () => {
   const reason = 'Maintenance';
   const attraction = { removalReason: reason };

   const line = RowAlertPresenter.buildAttractionRemovalReasonLine(attraction);

   assert.equal(line, Strings.itinerary.removedItems.notAvailableOnDate(attraction.removalReason));
});


test('Test_BuildGuardiansRemovalReasonLine_TestEmpty_ExpectEmpty', () => {
   const talk = {};

   const line = RowAlertPresenter.buildGuardiansRemovalReasonLine(talk);

   assert.equal(line, '');
});


test('Test_BuildGuardiansRemovalReasonLine_TestReason_ExpectMessage', () => {
   const reason = 'Cancelled';
   const talk = { removalReason: reason };

   const line = RowAlertPresenter.buildGuardiansRemovalReasonLine(talk);

   assert.equal(line, Strings.itinerary.removedItems.notAvailableOnDate(talk.removalReason));
});


test('Test_BuildWildRemovalReasonLine_TestEmpty_ExpectEmpty', () => {
   const encounter = {};

   const line = RowAlertPresenter.buildWildRemovalReasonLine(encounter);

   assert.equal(line, '');
});


test('Test_BuildWildRemovalReasonLine_TestReason_ExpectMessage', () => {
   const reason = 'Weather';
   const encounter = { removalReason: reason };

   const line = RowAlertPresenter.buildWildRemovalReasonLine(encounter);

   assert.equal(line, Strings.itinerary.removedItems.notAvailableOnDate(encounter.removalReason));
});
