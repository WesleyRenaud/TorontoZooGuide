import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleCheckboxGridFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleCheckboxGridFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCheckboxGridField_TestOptions_ExpectGrid', () => {
   const fieldEl = ConsoleCheckboxGridFieldBuilder.createCheckboxGridField({
      label: 'Days',
      options: [{ id: 'mon', label: 'Monday' }],
   });
   const gridEl = fieldEl.children[1];
   assert.equal(gridEl.className, 'console-operations-checkbox-grid');
   assert.equal(gridEl.children[0].children[0].id, 'mon');
   assert.match(gridEl.textContent, /Monday/);
});
