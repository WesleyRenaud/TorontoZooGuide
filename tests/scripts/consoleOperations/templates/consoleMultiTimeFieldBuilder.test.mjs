import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleMultiTimeFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleMultiTimeFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateMultiTimeField_TestIds_ExpectCompositeField', () => {
   const label = 'Times';
   const listId = 'time-list';
   const inputId = 'time-input';
   const placeholder = 'Add time';
   const helpText = 'Enter times';

   const fieldEl = ConsoleMultiTimeFieldBuilder.createMultiTimeField({
      label,
      listId,
      inputId,
      placeholder,
      helpText,
   });

   const compositeEl = fieldEl.children[Position.SECOND];
   const listEl = compositeEl.children[Position.FIRST];
   const inputEl = compositeEl.children[Position.SECOND];
   assert.match(fieldEl.textContent, new RegExp(label));
   assert.match(fieldEl.textContent, new RegExp(helpText));
   assert.equal(compositeEl.className, 'console-operations-multi-time-field');
   assert.equal(listEl.id, listId);
   assert.equal(inputEl.id, inputId);
   assert.equal(inputEl.placeholder, placeholder);
});
