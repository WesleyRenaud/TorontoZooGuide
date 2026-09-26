import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardControllerHelper } from '../../../../scripts/itinerary/wizard/wizardControllerHelper.js';
import { WizardSelectionStepFactory } from '../../../../scripts/itinerary/wizard/wizardSelectionStepFactory.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ClearWizard_TestMount_ExpectChildrenRemoved', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));

   WizardControllerHelper.clearWizard(mountEl);

   assert.equal(mountEl.children.length, 0);
});


test('Test_ClearWizard_TestMissingMount_ExpectNoOp', () => {
   const mountEl = null;

   assert.doesNotThrow(() => {
      WizardControllerHelper.clearWizard(mountEl);
   });
});


test('Test_CloseWizard_TestMissingMount_ExpectNoOp', () => {
   const mountEl = undefined;

   assert.doesNotThrow(() => {
      WizardControllerHelper.closeWizard(mountEl);
   });
});


test('Test_CloseWizard_TestMount_ExpectCleared', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));

   WizardControllerHelper.closeWizard(mountEl);

   assert.equal(mountEl.children.length, 0);
});


test('Test_LoadDefaultSelectionStepConfigs_TestDefaults_ExpectFactoryConfigs', async () => {
   const expected = WizardSelectionStepFactory.buildWizardSelectionStepConfigs();

   const configs = await WizardControllerHelper.loadDefaultSelectionStepConfigs();

   assert.equal(configs.length, expected.length);
   assert.deepEqual(
      configs.map((config) => config.stepKey),
      expected.map((config) => config.stepKey)
   );
   assert.equal(typeof configs[Position.FIRST].factory, 'function');
});
