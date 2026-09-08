import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardControllerHelper } from '../../../../scripts/itinerary/wizard/wizardControllerHelper.js';
import { WizardSelectionStepFactory } from '../../../../scripts/itinerary/wizard/wizardSelectionStepFactory.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ClearWizard_TestMount_ExpectChildrenRemoved', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));
   WizardControllerHelper.clearWizard(mountEl);
   assert.equal(mountEl.children.length, 0);
});

test('Test_ClearWizard_TestMissingMount_ExpectNoOp', () => {
   assert.doesNotThrow(() => {
      WizardControllerHelper.clearWizard(null);
      WizardControllerHelper.closeWizard(undefined);
   });
});

test('Test_CloseWizard_TestMount_ExpectCleared', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));
   WizardControllerHelper.closeWizard(mountEl);
   assert.equal(mountEl.children.length, 0);
});

test('Test_LoadDefaultSelectionStepConfigs_TestDefaults_ExpectFactoryConfigs', async () => {
   const configs = await WizardControllerHelper.loadDefaultSelectionStepConfigs();
   const expected = WizardSelectionStepFactory.buildWizardSelectionStepConfigs();

   assert.equal(configs.length, expected.length);
   assert.deepEqual(
      configs.map((config) => config.stepKey),
      expected.map((config) => config.stepKey)
   );
   assert.equal(typeof configs[0].factory, 'function');
});
