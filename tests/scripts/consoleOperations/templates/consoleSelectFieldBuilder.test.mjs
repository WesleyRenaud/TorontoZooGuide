import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateSelectField_TestOptions_ExpectSelect', () => {
   const fieldEl = ConsoleSelectFieldBuilder.createSelectField({
      label: 'Exhibit',
      inputId: 'exhibit',
      emptyOptionLabel: 'Select',
      options: [{ value: 'a', label: 'Africa' }],
   });
   const selectEl = fieldEl.children[1];
   assert.equal(selectEl.id, 'exhibit');
   assert.equal(selectEl.children.length, 2);
   assert.equal(selectEl.children[0].value, '');
   assert.equal(selectEl.children[1].textContent, 'Africa');
});
