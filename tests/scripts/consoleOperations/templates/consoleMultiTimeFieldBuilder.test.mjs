import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleMultiTimeFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleMultiTimeFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateMultiTimeField_TestIds_ExpectCompositeField', () => {
   const fieldEl = ConsoleMultiTimeFieldBuilder.createMultiTimeField({
      label: 'Times',
      listId: 'time-list',
      inputId: 'time-input',
      placeholder: 'Add time',
      helpText: 'Enter times',
   });

   assert.match(fieldEl.textContent, /Times/);
   assert.match(fieldEl.textContent, /Enter times/);

   const compositeEl = fieldEl.children[1];
   assert.equal(compositeEl.className, 'console-operations-multi-time-field');
   assert.equal(compositeEl.children[0].id, 'time-list');
   assert.equal(compositeEl.children[1].id, 'time-input');
   assert.equal(compositeEl.children[1].placeholder, 'Add time');
});
