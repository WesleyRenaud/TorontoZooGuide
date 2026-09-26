import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardStepConfigs } from '../../../../scripts/itinerary/wizard/wizardStepConfigs.js';


test('Test_ResolveWizardStartStep_TestDate_ExpectDefault', () => {
   const step = 'date';

   const resolved = WizardStepConfigs.resolveWizardStartStep(step);

   assert.equal(resolved, WizardStepConfigs.WIZARD_DEFAULT_START_STEP);
});


test('Test_ResolveWizardStartStep_TestAnimals_ExpectAnimals', () => {
   const step = 'animals';

   const resolved = WizardStepConfigs.resolveWizardStartStep(step);

   assert.equal(resolved, step);
});


test('Test_ResolveWizardStartStep_TestUnknown_ExpectDefault', () => {
   const step = 'unknown-step';

   const resolved = WizardStepConfigs.resolveWizardStartStep(step);

   assert.equal(resolved, WizardStepConfigs.WIZARD_DEFAULT_START_STEP);
});


test('Test_BuildSelectionStepHandlers_TestNextAndFinish_ExpectUpdateThenOverride', () => {
   const updates = [];
   const finished = [];
   let advanced = 0;
   const selectionKey = 'animals';
   const nextSelection = [{ id: 'lion' }];
   const finishSelection = [{ id: 'tiger' }];

   const handlers = WizardStepConfigs.buildSelectionStepHandlers({
      selectionKey,
      updateSelection: (nextKey, value, options) => {
         updates.push({ selectionKey: nextKey, value, options });
      },
      showNextStep: () => {
         advanced += 1;
      },
      finish: (override) => {
         finished.push(override);
      },
   });

   handlers.onNext?.(nextSelection);
   handlers.onFinish?.(finishSelection);

   assert.deepEqual(updates, [
      {
         selectionKey,
         value: nextSelection,
         options: { preserveOnInvalid: false },
      },
   ]);
   assert.equal(advanced, 1);
   assert.deepEqual(finished, [{ [selectionKey]: finishSelection }]);
});


test('Test_WizardSelectionStepDefinitionsByKey_TestConfiguredSteps_ExpectAllKeys', () => {
   const definitions = WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY;

   assert.ok(definitions.animals);
   assert.ok(definitions.attractions);
   assert.ok(definitions.guardiansTalks);
   assert.ok(definitions.regions);
   assert.ok(definitions.transportations);
   assert.ok(definitions.wildEncounters);
   assert.equal(definitions.regions.preserveOnInvalid, true);
   assert.equal(definitions.wildEncounters.nextStepKey, 'transportations');
   assert.equal(definitions.transportations.prevStepKey, 'wildEncounters');
});
