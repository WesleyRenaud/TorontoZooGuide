import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorShellBuilderHelper } from '../../../../../scripts/itinerary/selectors/base/selectorShellBuilderHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateButton_TestConfig_ExpectButton', () => {
   const className = 'shell-btn';
   const text = 'Done';

   const button = SelectorShellBuilderHelper.createButton({
      className,
      text,
   });

   assert.equal(button.type, 'button');
   assert.equal(button.className, className);
   assert.equal(button.textContent, text);
   assert.equal(button.getAttribute('aria-label'), null);
});
