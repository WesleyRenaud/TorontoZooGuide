import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleRecurringScheduleRowsFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleRecurringScheduleRowsFieldBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateRecurringScheduleRowsField_TestIds_ExpectRowsAndAddButton', () => {
   const fieldEl = ConsoleRecurringScheduleRowsFieldBuilder.createRecurringScheduleRowsField({
      rowsId: 'rows',
      addRowButtonId: 'add-row',
   });

   assert.match(fieldEl.textContent, new RegExp(Strings.labels.encounterTimes));
   assert.match(fieldEl.textContent, new RegExp(Strings.actions.addEncounterScheduleRow));
   assert.match(fieldEl.textContent, new RegExp(Strings.help.encounterScheduleRows));

   const rowsEl = [...fieldEl.children].find((child) => child.id === 'rows');
   const addButtonEl = [...fieldEl.children].find((child) => child.id === 'add-row');

   assert.equal(rowsEl.className, 'console-operations-schedule-rows');
   assert.equal(addButtonEl.type, 'button');
   assert.equal(addButtonEl.className, 'console-operations-secondary-btn console-operations-schedule-rows-add');
});
