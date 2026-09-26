import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateDateField_TestConfig_ExpectDatetimeInput', () => {
   const inputId = 'date';

   const fieldEl = ConsoleDateFieldBuilder.createDateField({
      label: 'Date',
      inputId,
      placeholder: 'YYYY-MM-DD',
   });

   const inputEl = fieldEl.children[Position.SECOND];
   assert.equal(inputEl.id, inputId);
   assert.match(inputEl.className, /console-operations-datetime/);
});
