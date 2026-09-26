import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleRadioGroupFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleRadioGroupFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateRadioGroupField_TestOptions_ExpectGroup', () => {
   const name = 'scope';
   const checked = true;
   const options = [{ id: 'all', value: 'all', label: 'All', checked }];

   const fieldEl = ConsoleRadioGroupFieldBuilder.createRadioGroupField({
      label: 'Scope',
      name,
      options,
   });

   const inputEl = fieldEl.children[Position.SECOND]
      .children[Position.FIRST]
      .children[Position.FIRST];
   assert.equal(inputEl.type, 'radio');
   assert.equal(inputEl.name, name);
   assert.equal(inputEl.checked, checked);
});
