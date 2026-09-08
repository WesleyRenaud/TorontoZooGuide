import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleRadioGroupFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleRadioGroupFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateRadioGroupField_TestOptions_ExpectGroup', () => {
   const fieldEl = ConsoleRadioGroupFieldBuilder.createRadioGroupField({
      label: 'Scope',
      name: 'scope',
      options: [{ id: 'all', value: 'all', label: 'All', checked: true }],
   });
   const inputEl = fieldEl.children[1].children[0].children[0];
   assert.equal(inputEl.type, 'radio');
   assert.equal(inputEl.name, 'scope');
   assert.equal(inputEl.checked, true);
});
