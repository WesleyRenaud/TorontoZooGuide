import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDropdownOptionBuilder } from '../../../../scripts/consoleOperations/options/consoleDropdownOptionBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreatePlaceholderOption_TestLabel_ExpectEmptyValue', () => {
   const option = ConsoleDropdownOptionBuilder.createPlaceholderOption('Select');
   assert.equal(option.value, '');
   assert.equal(option.textContent, 'Select');
});

test('Test_CreateNamedOption_TestName_ExpectValueAndLabel', () => {
   const option = ConsoleDropdownOptionBuilder.createNamedOption('Carousel');
   assert.equal(option.value, 'Carousel');
   assert.equal(option.textContent, 'Carousel');
});
