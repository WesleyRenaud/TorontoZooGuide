import assert from 'node:assert/strict';
import test from 'node:test';

import { RowAlertPresenter } from '../../../../scripts/itinerary/panel/rowAlertPresenter.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_BuildAnimalAlert_TestRemovalReason_ExpectRemovalLine', () => {
   assert.deepEqual(RowAlertPresenter.buildAnimalAlert({
      removalReason: 'Closed exhibit',
   }), {
      line: Strings.itinerary.removedItems.unavailableReason('Closed exhibit'),
      tone: 'default',
   });
});

test('Test_BuildAnimalAlert_TestVisibilityChange_ExpectVisibilityAlert', () => {
   assert.deepEqual(RowAlertPresenter.buildAnimalAlert({
      likelihoodBefore: 10,
      likelihoodAfter: 90,
   }), {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(10, 90),
      tone: 'positive',
   });
});

test('Test_BuildAttractionRemovalReasonLine_TestReason_ExpectMessage', () => {
   assert.equal(RowAlertPresenter.buildAttractionRemovalReasonLine({}), '');
   assert.equal(
      RowAlertPresenter.buildAttractionRemovalReasonLine({ removalReason: 'Maintenance' }),
      Strings.itinerary.removedItems.notAvailableOnDate('Maintenance')
   );
});

test('Test_BuildGuardiansRemovalReasonLine_TestReason_ExpectMessage', () => {
   assert.equal(RowAlertPresenter.buildGuardiansRemovalReasonLine({}), '');
   assert.equal(
      RowAlertPresenter.buildGuardiansRemovalReasonLine({ removalReason: 'Cancelled' }),
      Strings.itinerary.removedItems.notAvailableOnDate('Cancelled')
   );
});

test('Test_BuildWildRemovalReasonLine_TestReason_ExpectMessage', () => {
   assert.equal(RowAlertPresenter.buildWildRemovalReasonLine({}), '');
   assert.equal(
      RowAlertPresenter.buildWildRemovalReasonLine({ removalReason: 'Weather' }),
      Strings.itinerary.removedItems.notAvailableOnDate('Weather')
   );
});
