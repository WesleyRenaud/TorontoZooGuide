import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardSelectionStepFactory } from '../../../../scripts/itinerary/wizard/wizardSelectionStepFactory.js';

test('Test_BuildWizardSelectionStepConfigs_TestDefinitions_ExpectFactoriesAttached', () => {
   const factoryA = () => 'a';
   const factoryB = () => 'b';
   const configs = WizardSelectionStepFactory.buildWizardSelectionStepConfigs(
      [
         { stepKey: 'animals', title: 'Animals' },
         { stepKey: 'regions', title: 'Regions' },
      ],
      {
         animals: factoryA,
         regions: factoryB,
      }
   );

   assert.equal(configs.length, 2);
   assert.equal(configs[0].factory, factoryA);
   assert.equal(configs[1].factory, factoryB);
   assert.equal(configs[0].title, 'Animals');
});

test('Test_WizardSelectionStepFactories_TestKeys_ExpectFrozenMap', () => {
   assert.ok(WizardSelectionStepFactory.WIZARD_SELECTION_STEP_FACTORIES.animals);
   assert.ok(WizardSelectionStepFactory.WIZARD_SELECTION_STEP_FACTORIES.regions);
   assert.ok(WizardSelectionStepFactory.WIZARD_SELECTION_STEP_FACTORIES.transportations);
});
