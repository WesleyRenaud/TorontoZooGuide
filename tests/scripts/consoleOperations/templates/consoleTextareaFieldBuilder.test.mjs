import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTextareaField_TestConfig_ExpectField', () => {
   const fieldEl = ConsoleTextareaFieldBuilder.createTextareaField({
      label: 'Notes',
      inputId: 'notes',
      placeholder: 'Enter notes',
   });
   const textareaEl = fieldEl.children[1];
   assert.equal(fieldEl.className, 'console-operations-field');
   assert.equal(textareaEl.id, 'notes');
   assert.equal(textareaEl.placeholder, 'Enter notes');
});
