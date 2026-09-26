import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleFieldPrimitiveBuilder } from '../../../../scripts/consoleOperations/templates/consoleFieldPrimitiveBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateFieldWrapper_TestBasics_ExpectFieldClass', () => {
   const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();

   assert.equal(fieldEl.className, 'console-operations-field');
});


test('Test_CreateLabel_TestTextAndFor_ExpectLabel', () => {
   const text = 'Name';
   const htmlFor = 'name';

   const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({ text, htmlFor });

   assert.equal(labelEl.textContent, text);
   assert.equal(labelEl.htmlFor, htmlFor);
});


test('Test_AppendChildren_TestNested_ExpectAppended', () => {
   const parent = document.createElement('div');
   const child = document.createElement('span');
   const nested = document.createElement('em');
   const children = [child, null, [nested]];

   const parentEl = ConsoleFieldPrimitiveBuilder.appendChildren(parent, children);

   assert.equal(parentEl.children.length, [child, nested].length);
});
