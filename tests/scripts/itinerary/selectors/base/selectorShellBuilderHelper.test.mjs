import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorShellBuilderHelper } from '../../../../../scripts/itinerary/selectors/base/selectorShellBuilderHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateButton_TestConfig_ExpectButton', () => {
   const button = SelectorShellBuilderHelper.createButton({
      className: 'shell-btn',
      text: 'Done',
   });
   assert.equal(button.type, 'button');
   assert.equal(button.className, 'shell-btn');
   assert.equal(button.textContent, 'Done');
   assert.equal(button.getAttribute('aria-label'), null);
});
