import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleCheckboxGridFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleCheckboxGridFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCheckboxGridField_TestOptions_ExpectGrid', () => {
   const gridId = 'daysGrid';
   const mondayId = 'mon';
   const mondayLabel = 'Monday';

   const fieldEl = ConsoleCheckboxGridFieldBuilder.createCheckboxGridField({
      label: 'Days',
      gridId,
      options: [{ id: mondayId, label: mondayLabel }],
   });

   const gridEl = fieldEl.children[Position.SECOND];
   assert.equal(gridEl.id, gridId);
   assert.equal(gridEl.className, 'console-operations-checkbox-grid');
   assert.equal(gridEl.children[Position.FIRST].children[Position.FIRST].id, mondayId);
   assert.match(gridEl.textContent, new RegExp(mondayLabel));
});
