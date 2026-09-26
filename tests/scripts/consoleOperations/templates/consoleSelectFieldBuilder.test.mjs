import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleSelectFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSelectField_TestOptions_ExpectSelect', () => {
   const inputId = 'exhibit';
   const emptyOptionLabel = 'Select';
   const region = 'Africa';
   const options = [{ value: 'a', label: region }];

   const fieldEl = ConsoleSelectFieldBuilder.createSelectField({
      label: 'Exhibit',
      inputId,
      emptyOptionLabel,
      options,
   });

   const selectEl = fieldEl.children[Position.SECOND];
   assert.equal(selectEl.id, inputId);
   assert.equal(selectEl.children.length, options.length + 1);
   assert.equal(selectEl.children[Position.FIRST].value, '');
   assert.equal(selectEl.children[Position.SECOND].textContent, region);
});
