import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleFieldPrimitiveBuilder } from '../../../../scripts/consoleOperations/templates/consoleFieldPrimitiveBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateFieldWrapperAndLabel_TestBasics_ExpectElements', () => {
   const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
   const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({ text: 'Name', htmlFor: 'name' });
   assert.equal(fieldEl.className, 'console-operations-field');
   assert.equal(labelEl.textContent, 'Name');
   assert.equal(labelEl.htmlFor, 'name');
});

test('Test_AppendChildren_TestNested_ExpectAppended', () => {
   const parent = document.createElement('div');
   const child = document.createElement('span');
   ConsoleFieldPrimitiveBuilder.appendChildren(parent, [child, null, [document.createElement('em')]]);
   assert.equal(parent.children.length, 2);
});
