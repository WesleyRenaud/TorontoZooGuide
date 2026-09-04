import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardStepDraftSync } from '../../../../scripts/itinerary/wizard/wizardStepDraftSync.js';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

test('Test_ResolveDateStepDraftUpdate_TestInvalidOrUnchanged_ExpectNullOrDate', () => {
   assert.equal(
      WizardStepDraftSync.resolveDateStepDraftUpdate({
         currentDate: null,
         wizardDate: '2026-06-15',
      }),
      null
   );
   assert.equal(
      WizardStepDraftSync.resolveDateStepDraftUpdate({
         currentDate: makeNoonDate(2026, 5, 15),
         wizardDate: '2026-06-15',
      }),
      null
   );
   assert.equal(
      WizardStepDraftSync.resolveDateStepDraftUpdate({
         currentDate: makeNoonDate(2026, 5, 16),
         wizardDate: '2026-06-15',
      }),
      '2026-06-16'
   );
});

test('Test_ShouldSyncSelectionStepDraft_TestController_ExpectSyncRules', () => {
   assert.equal(
      WizardStepDraftSync.shouldSyncSelectionStepDraft({
         stepConfig: null,
         stepController: { getSelectionSnapshot: async () => [] },
      }),
      false
   );
   assert.equal(
      WizardStepDraftSync.shouldSyncSelectionStepDraft({
         stepConfig: { selectionKey: 'animals' },
         stepController: {
            getSelectionSnapshot: async () => [],
            shouldSkipClosingSelectionSync: () => true,
         },
      }),
      false
   );
   assert.equal(
      WizardStepDraftSync.shouldSyncSelectionStepDraft({
         stepConfig: { selectionKey: 'animals' },
         stepController: {
            getSelectionSnapshot: async () => [],
            shouldSkipClosingSelectionSync: () => false,
         },
      }),
      true
   );
});

test('Test_IsWizardDateStep_TestDefaultStep_ExpectIdentified', () => {
   assert.equal(WizardStepDraftSync.isWizardDateStep('date'), true);
   assert.equal(WizardStepDraftSync.isWizardDateStep('animals'), false);
});
