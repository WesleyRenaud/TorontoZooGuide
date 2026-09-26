import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDropdownOptionBuilder } from '../../../../scripts/consoleOperations/options/consoleDropdownOptionBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreatePlaceholderOption_TestLabel_ExpectEmptyValue', () => {
   const label = 'Select';

   const option = ConsoleDropdownOptionBuilder.createPlaceholderOption(label);

   assert.equal(option.value, '');
   assert.equal(option.textContent, label);
});


test('Test_CreateNamedOption_TestName_ExpectValueAndLabel', () => {
   const name = 'Carousel';

   const option = ConsoleDropdownOptionBuilder.createNamedOption(name);

   assert.equal(option.value, name);
   assert.equal(option.textContent, name);
});
