import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardFinalizePresenter } from '../../../../scripts/itinerary/wizard/wizardFinalizePresenter.js';

test('Test_ShouldShowSaveIssuesPopup_TestSaveIssues_ExpectDetected', () => {
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({ saveIssues: [{ type: 'conflict' }] }), true);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({ saveIssues: [] }), false);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup({}), false);
   assert.equal(WizardFinalizePresenter.shouldShowSaveIssuesPopup(null), false);
});
