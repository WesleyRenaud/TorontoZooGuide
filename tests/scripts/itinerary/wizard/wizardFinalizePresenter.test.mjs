import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardFinalizePresenter } from '../../../../scripts/itinerary/wizard/wizardFinalizePresenter.js';


test('Test_ShouldShowSaveIssuesPopup_TestSaveIssues_ExpectTrue', () => {
   const saveIssues = [{ type: 'conflict' }];
   const result = { saveIssues };

   const shouldShow = WizardFinalizePresenter.shouldShowSaveIssuesPopup(result);

   assert.equal(shouldShow, true);
});


test('Test_ShouldShowSaveIssuesPopup_TestEmptyIssues_ExpectFalse', () => {
   const result = { saveIssues: [] };

   const shouldShow = WizardFinalizePresenter.shouldShowSaveIssuesPopup(result);

   assert.equal(shouldShow, false);
});


test('Test_ShouldShowSaveIssuesPopup_TestMissingIssues_ExpectFalse', () => {
   const result = {};

   const shouldShow = WizardFinalizePresenter.shouldShowSaveIssuesPopup(result);

   assert.equal(shouldShow, false);
});


test('Test_ShouldShowSaveIssuesPopup_TestNull_ExpectFalse', () => {
   const result = null;

   const shouldShow = WizardFinalizePresenter.shouldShowSaveIssuesPopup(result);

   assert.equal(shouldShow, false);
});
