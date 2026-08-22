import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildSelectionStepHandlers,
   resolveWizardStartStep,
   WIZARD_DEFAULT_START_STEP,
   WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY,
} from '../../scripts/itinerary/wizard/wizardStepConfigs.js';

test('resolveWizardStartStep falls back to the date step for unknown values', () => {
   assert.equal(resolveWizardStartStep('date'), WIZARD_DEFAULT_START_STEP);
   assert.equal(resolveWizardStartStep('animals'), 'animals');
   assert.equal(resolveWizardStartStep('unknown-step'), WIZARD_DEFAULT_START_STEP);
});

test('buildSelectionStepHandlers updates selections on next but finishes via override only', () => {
   const updates = [];
   const finished = [];
   let advanced = 0;

   const handlers = buildSelectionStepHandlers({
      selectionKey: 'animals',
      updateSelection: (selectionKey, value, options) => {
         updates.push({ selectionKey, value, options });
      },
      showNextStep: () => {
         advanced += 1;
      },
      finish: (override) => {
         finished.push(override);
      },
   });

   handlers.onNext?.([{ id: 'lion' }]);
   handlers.onFinish?.([{ id: 'tiger' }]);

   assert.deepEqual(updates, [
      {
         selectionKey: 'animals',
         value: [{ id: 'lion' }],
         options: { preserveOnInvalid: false },
      },
   ]);
   assert.equal(advanced, 1);
   assert.deepEqual(finished, [{ animals: [{ id: 'tiger' }] }]);
});

test('WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY exposes every configured step', () => {
   assert.deepEqual(
      Object.keys(WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY).sort(),
      [
         'animals',
         'attractions',
         'guardiansTalks',
         'regions',
         'transportations',
         'wildEncounters',
      ]
   );
   assert.equal(
      WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.regions.preserveOnInvalid,
      true
   );
   assert.equal(
      WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.wildEncounters.nextStepKey,
      'transportations'
   );
   assert.equal(
      WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.transportations.prevStepKey,
      'wildEncounters'
   );
});
