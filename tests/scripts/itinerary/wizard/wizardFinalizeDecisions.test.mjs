import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardFinalizeDecisions } from '../../../../scripts/itinerary/wizard/wizardFinalizeDecisions.js';

test('Test_ShouldBlockEmptyFinish_TestAllowEmpty_ExpectBlockedOrAllowed', () => {
   const isEmpty = (itinerary) => itinerary.empty;

   assert.equal(
      WizardFinalizeDecisions.shouldBlockEmptyFinish({ empty: true }, false, isEmpty),
      true
   );
   assert.equal(
      WizardFinalizeDecisions.shouldBlockEmptyFinish({ empty: true }, true, isEmpty),
      false
   );
   assert.equal(
      WizardFinalizeDecisions.shouldBlockEmptyFinish({ empty: false }, false, isEmpty),
      false
   );
});

test('Test_ShouldShowSaveIssuesPopup_TestSaveIssues_ExpectDetected', () => {
   assert.equal(WizardFinalizeDecisions.shouldShowSaveIssuesPopup({ saveIssues: [{ type: 'conflict' }] }), true);
   assert.equal(WizardFinalizeDecisions.shouldShowSaveIssuesPopup({ saveIssues: [] }), false);
   assert.equal(WizardFinalizeDecisions.shouldShowSaveIssuesPopup({}), false);
   assert.equal(WizardFinalizeDecisions.shouldShowSaveIssuesPopup(null), false);
});
