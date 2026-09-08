import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDiffSummaryHelper } from '../../../../../scripts/itinerary/wizard/diff/wizardDiffSummaryHelper.js';

test('Test_HasItems_TestArrays_ExpectBoolean', () => {
   assert.equal(WizardDiffSummaryHelper.hasItems(['a']), true);
   assert.equal(WizardDiffSummaryHelper.hasItems([]), false);
   assert.equal(WizardDiffSummaryHelper.hasItems(null), false);
});
