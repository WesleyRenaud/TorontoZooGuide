import assert from 'node:assert/strict';
import test from 'node:test';

import {
   isWizardDateStep,
   resolveDateStepDraftUpdate,
   shouldSyncSelectionStepDraft,
} from '../../scripts/itinerary/wizard/wizardStepDraftSync.js';

function makeNoonDate(year, monthIndex, day) {
   return new Date(year, monthIndex, day, 12, 0, 0, 0);
}

test('resolveDateStepDraftUpdate returns null for invalid or unchanged dates', () => {
   assert.equal(
      resolveDateStepDraftUpdate({
         currentDate: null,
         wizardDate: '2026-06-15',
      }),
      null
   );
   assert.equal(
      resolveDateStepDraftUpdate({
         currentDate: makeNoonDate(2026, 5, 15),
         wizardDate: '2026-06-15',
      }),
      null
   );
   assert.equal(
      resolveDateStepDraftUpdate({
         currentDate: makeNoonDate(2026, 5, 16),
         wizardDate: '2026-06-15',
      }),
      '2026-06-16'
   );
});

test('shouldSyncSelectionStepDraft requires a controller snapshot and allows sync by default', () => {
   assert.equal(
      shouldSyncSelectionStepDraft({
         stepConfig: null,
         stepController: { getSelectionSnapshot: async () => [] },
      }),
      false
   );
   assert.equal(
      shouldSyncSelectionStepDraft({
         stepConfig: { selectionKey: 'animals' },
         stepController: {
            getSelectionSnapshot: async () => [],
            shouldSkipClosingSelectionSync: () => true,
         },
      }),
      false
   );
   assert.equal(
      shouldSyncSelectionStepDraft({
         stepConfig: { selectionKey: 'animals' },
         stepController: {
            getSelectionSnapshot: async () => [],
            shouldSkipClosingSelectionSync: () => false,
         },
      }),
      true
   );
});

test('isWizardDateStep identifies the default wizard date step', () => {
   assert.equal(isWizardDateStep('date'), true);
   assert.equal(isWizardDateStep('animals'), false);
});
