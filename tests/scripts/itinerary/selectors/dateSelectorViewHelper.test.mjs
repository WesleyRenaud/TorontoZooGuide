import assert from 'node:assert/strict';
import test from 'node:test';

import { DateSelectorViewHelper } from '../../../../scripts/itinerary/selectors/dateSelectorViewHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateButton_TestConfig_ExpectButton', () => {
   const button = DateSelectorViewHelper.createButton({
      className: 'date-nav',
      text: 'Next',
      ariaLabel: 'Next day',
   });
   assert.equal(button.type, 'button');
   assert.equal(button.className, 'date-nav');
   assert.equal(button.textContent, 'Next');
   assert.equal(button.getAttribute('aria-label'), 'Next day');
});
