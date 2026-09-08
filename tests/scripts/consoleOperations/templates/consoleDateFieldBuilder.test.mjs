import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateDateField_TestConfig_ExpectDatetimeInput', () => {
   const fieldEl = ConsoleDateFieldBuilder.createDateField({
      label: 'Date',
      inputId: 'date',
      placeholder: 'YYYY-MM-DD',
   });
   const inputEl = fieldEl.children[1];
   assert.equal(inputEl.id, 'date');
   assert.match(inputEl.className, /console-operations-datetime/);
});
