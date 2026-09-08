import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleTextInputFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextInputFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTextInputField_TestConfig_ExpectInput', () => {
   const fieldEl = ConsoleTextInputFieldBuilder.createTextInputField({
      label: 'Name',
      inputId: 'name',
      placeholder: 'Enter name',
      helpText: 'Required',
   });
   assert.equal(fieldEl.children[1].id, 'name');
   assert.equal(fieldEl.children[1].placeholder, 'Enter name');
   assert.match(fieldEl.textContent, /Required/);
});
