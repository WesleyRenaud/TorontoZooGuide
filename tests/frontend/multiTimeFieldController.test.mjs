import assert from 'node:assert/strict';
import test from 'node:test';

import { createMultiTimeFieldController } from '../../scripts/consoleOperations/forms/multiTimeFieldController.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

function createMultiTimeFieldDom() {
   const fieldEl = createDomNode('div', 'console-operations-multi-time-field');
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');

   fieldEl.appendChild(listEl);
   fieldEl.appendChild(inputEl);

   return { fieldEl, listEl, inputEl };
}

test('createMultiTimeFieldController renders saved times as chips', () => {
   const { fieldEl, listEl, inputEl } = createMultiTimeFieldDom();
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('2:30 PM');

   assert.equal(listEl.children.length, 2);
   assert.equal(
      fieldEl.classList.contains('console-operations-multi-time-field--has-times'),
      true
   );
   assert.deepEqual(controller.getTimes(), [ '1:00 PM', '2:30 PM' ]);
});

test('createMultiTimeFieldController displays chips in 12-hour format', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');

   assert.equal(
      listEl.children[0].querySelector('.console-operations-time-chip-label').textContent,
      '1:00 PM'
   );
});

test('createMultiTimeFieldController treats equivalent 12-hour and 24-hour times as duplicates', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('3:30 PM');
   controller.addTime('15:30');

   assert.deepEqual(controller.getTimes(), [ '3:30 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('createMultiTimeFieldController clears the input after committing a pending time', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   inputEl.value = '3:00 PM';

   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.commitPendingInput();

   assert.deepEqual(controller.getTimes(), [ '3:00 PM' ]);
   assert.equal(inputEl.value, '');
});

test('createMultiTimeFieldController ignores duplicate times', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('1:00 PM');

   assert.deepEqual(controller.getTimes(), [ '1:00 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('createMultiTimeFieldController removes a saved time', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('2:30 PM');
   controller.removeTime('1:00 PM');

   assert.deepEqual(controller.getTimes(), [ '2:30 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('createMultiTimeFieldController removes the last saved time', () => {
   const { listEl, inputEl } = createMultiTimeFieldDom();
   const controller = createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('2:30 PM');
   controller.removeLastTime();

   assert.deepEqual(controller.getTimes(), [ '1:00 PM' ]);
   assert.equal(listEl.children.length, 1);
});
