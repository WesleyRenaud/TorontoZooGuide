import assert from 'node:assert/strict';
import test from 'node:test';

import { RowAlertsBuilder } from '../../../../scripts/itinerary/panel/rowAlertsBuilder.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_GetLikelihoodPair_TestValues_ExpectPercents', () => {
   assert.deepEqual(RowAlertsBuilder.getLikelihoodPair({
      likelihoodBefore: 40,
      likelihoodAfter: 70,
   }), { before: 40, after: 70 });
});

test('Test_BuildAnimalRemovalReasonLine_TestReason_ExpectUnavailable', () => {
   assert.equal(RowAlertsBuilder.buildAnimalRemovalReasonLine({}), '');
   assert.equal(
      RowAlertsBuilder.buildAnimalRemovalReasonLine({ removalReason: 'Closed exhibit' }),
      Strings.itinerary.removedItems.unavailableReason('Closed exhibit')
   );
});

test('Test_BuildAnimalVisibilityChange_TestDecrease_ExpectDefaultTone', () => {
   assert.deepEqual(RowAlertsBuilder.buildAnimalVisibilityChange({
      likelihoodBefore: 80,
      likelihoodAfter: 20,
   }), {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(80, 20),
      tone: 'default',
   });
});

test('Test_BuildAnimalVisibilityChange_TestIncrease_ExpectPositiveTone', () => {
   assert.deepEqual(RowAlertsBuilder.buildAnimalVisibilityChange({
      likelihoodBefore: 20,
      likelihoodAfter: 80,
   }), {
      line: Strings.itinerary.removedItems.projectedVisibilityChanged(20, 80),
      tone: 'positive',
   });
});

test('Test_BuildAnimalVisibilityChange_TestUnchanged_ExpectEmpty', () => {
   assert.deepEqual(RowAlertsBuilder.buildAnimalVisibilityChange({
      likelihoodBefore: 50,
      likelihoodAfter: 50,
   }), { line: '', tone: 'default' });
});
