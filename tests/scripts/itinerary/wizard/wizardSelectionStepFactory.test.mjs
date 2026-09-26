import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardSelectionStepFactory } from '../../../../scripts/itinerary/wizard/wizardSelectionStepFactory.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_BuildWizardSelectionStepConfigs_TestDefinitions_ExpectFactoriesAttached', () => {
   const factoryA = () => 'a';
   const factoryB = () => 'b';
   const animalsTitle = 'Animals';
   const regionsTitle = 'Regions';
   const animalsKey = 'animals';
   const regionsKey = 'regions';
   const definitions = [
      { stepKey: animalsKey, title: animalsTitle },
      { stepKey: regionsKey, title: regionsTitle },
   ];
   const factories = {
      [animalsKey]: factoryA,
      [regionsKey]: factoryB,
   };

   const configs = WizardSelectionStepFactory.buildWizardSelectionStepConfigs(
      definitions,
      factories
   );

   assert.equal(configs.length, definitions.length);
   assert.equal(configs[Position.FIRST].factory, factoryA);
   assert.equal(configs.at(Position.LAST).factory, factoryB);
   assert.equal(configs[Position.FIRST].title, animalsTitle);
});


test('Test_WizardSelectionStepFactories_TestKeys_ExpectFrozenMap', () => {
   const factories = WizardSelectionStepFactory.WIZARD_SELECTION_STEP_FACTORIES;

   assert.ok(factories.animals);
   assert.ok(factories.regions);
   assert.ok(factories.transportations);
});
