import assert from 'node:assert/strict';
import test from 'node:test';

import { DateSelectorViewHelper } from '../../../../scripts/itinerary/selectors/dateSelectorViewHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateButton_TestConfig_ExpectButton', () => {
   const className = 'date-nav';
   const text = 'Next';
   const ariaLabel = 'Next day';

   const button = DateSelectorViewHelper.createButton({
      className,
      text,
      ariaLabel,
   });

   assert.equal(button.type, 'button');
   assert.equal(button.className, className);
   assert.equal(button.textContent, text);
   assert.equal(button.getAttribute('aria-label'), ariaLabel);
});
