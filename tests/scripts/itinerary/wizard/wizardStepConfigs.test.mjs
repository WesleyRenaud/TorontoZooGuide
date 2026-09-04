import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardStepConfigs } from '../../../../scripts/itinerary/wizard/wizardStepConfigs.js';

test('Test_ResolveWizardStartStep_TestUnknownValues_ExpectDateFallback', () => {
   assert.equal(
      WizardStepConfigs.resolveWizardStartStep('date'),
      WizardStepConfigs.WIZARD_DEFAULT_START_STEP
   );
   assert.equal(WizardStepConfigs.resolveWizardStartStep('animals'), 'animals');
   assert.equal(
      WizardStepConfigs.resolveWizardStartStep('unknown-step'),
      WizardStepConfigs.WIZARD_DEFAULT_START_STEP
   );
});

test('Test_BuildSelectionStepHandlers_TestNextAndFinish_ExpectUpdateThenOverride', () => {
   const updates = [];
   const finished = [];
   let advanced = 0;

   const handlers = WizardStepConfigs.buildSelectionStepHandlers({
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

test('Test_WizardSelectionStepDefinitionsByKey_TestConfiguredSteps_ExpectAllKeys', () => {
   assert.deepEqual(
      Object.keys(WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY).sort(),
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
      WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.regions.preserveOnInvalid,
      true
   );
   assert.equal(
      WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.wildEncounters.nextStepKey,
      'transportations'
   );
   assert.equal(
      WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY.transportations.prevStepKey,
      'wildEncounters'
   );
});
