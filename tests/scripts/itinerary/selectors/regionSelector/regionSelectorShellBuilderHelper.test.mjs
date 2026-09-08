import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorShellBuilderHelper } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorShellBuilderHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateButton_TestConfig_ExpectButton', () => {
   const button = RegionSelectorShellBuilderHelper.createButton({
      className: 'region-btn',
      text: 'Africa',
      ariaLabel: 'Select Africa',
   });
   assert.equal(button.className, 'region-btn');
   assert.equal(button.textContent, 'Africa');
   assert.equal(button.getAttribute('aria-label'), 'Select Africa');
});
