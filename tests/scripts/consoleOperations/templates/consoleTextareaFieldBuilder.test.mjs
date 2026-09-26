import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleTextareaFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextareaFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateTextareaField_TestConfig_ExpectField', () => {
   const inputId = 'notes';
   const placeholder = 'Enter notes';

   const fieldEl = ConsoleTextareaFieldBuilder.createTextareaField({
      label: 'Notes',
      inputId,
      placeholder,
   });

   const textareaEl = fieldEl.children[Position.SECOND];
   assert.equal(fieldEl.className, 'console-operations-field');
   assert.equal(textareaEl.id, inputId);
   assert.equal(textareaEl.placeholder, placeholder);
});
