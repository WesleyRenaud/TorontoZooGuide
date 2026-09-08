import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardFinalizePresenter } from '../../../../scripts/itinerary/wizard/wizardFinalizePresenter.js';

test('Test_ShouldBlockEmptyFinish_TestAllowEmpty_ExpectBlockedOrAllowed', () => {
   const isEmpty = (itinerary) => itinerary.empty;

   assert.equal(
      WizardFinalizePresenter.shouldBlockEmptyFinish({ empty: true }, false, isEmpty),
      true
   );
   assert.equal(
      WizardFinalizePresenter.shouldBlockEmptyFinish({ empty: true }, true, isEmpty),
      false
   );
   assert.equal(
      WizardFinalizePresenter.shouldBlockEmptyFinish({ empty: false }, false, isEmpty),
      false
   );
});

test('Test_ShouldShowSaveIssuesPopup_TestSaveIssues_ExpectDetected', () => {
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({ saveIssues: [{ type: 'conflict' }] }), true);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({ saveIssues: [] }), false);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({}), false);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup(null), false);
});
