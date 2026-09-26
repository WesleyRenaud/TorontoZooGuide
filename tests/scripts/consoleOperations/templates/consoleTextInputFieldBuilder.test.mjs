import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleTextInputFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleTextInputFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateTextInputField_TestConfig_ExpectInput', () => {
   const inputId = 'name';
   const placeholder = 'Enter name';
   const helpText = 'Required';

   const fieldEl = ConsoleTextInputFieldBuilder.createTextInputField({
      label: 'Name',
      inputId,
      placeholder,
      helpText,
   });

   const inputEl = fieldEl.children[Position.SECOND];
   assert.equal(inputEl.id, inputId);
   assert.equal(inputEl.placeholder, placeholder);
   assert.match(fieldEl.textContent, new RegExp(helpText));
});
