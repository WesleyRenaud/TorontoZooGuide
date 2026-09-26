import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardDiffSummaryHelper } from '../../../../../scripts/itinerary/wizard/diff/wizardDiffSummaryHelper.js';


test('Test_HasItems_TestNonEmpty_ExpectTrue', () => {
   const items = ['African Lion'];

   const hasItems = WizardDiffSummaryHelper.hasItems(items);

   assert.equal(hasItems, true);
});


test('Test_HasItems_TestEmpty_ExpectFalse', () => {
   const items = [];

   const hasItems = WizardDiffSummaryHelper.hasItems(items);

   assert.equal(hasItems, false);
});


test('Test_HasItems_TestNull_ExpectFalse', () => {
   const items = null;

   const hasItems = WizardDiffSummaryHelper.hasItems(items);

   assert.equal(hasItems, false);
});
