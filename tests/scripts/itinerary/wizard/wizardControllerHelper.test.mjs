import assert from 'node:assert/strict';
import test from 'node:test';

import { WizardControllerHelper } from '../../../../scripts/itinerary/wizard/wizardControllerHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ClearWizard_TestMount_ExpectChildrenRemoved', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));
   WizardControllerHelper.clearWizard(mountEl);
   assert.equal(mountEl.children.length, 0);
});

test('Test_CloseWizard_TestMount_ExpectCleared', () => {
   const mountEl = document.createElement('div');
   mountEl.appendChild(document.createElement('span'));
   WizardControllerHelper.closeWizard(mountEl);
   assert.equal(mountEl.children.length, 0);
});
