import assert from 'node:assert/strict';
import test from 'node:test';

import { MultiTimeFieldController } from '../../../../scripts/consoleOperations/forms/multiTimeFieldController.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createMultiTimeFieldDom() {
   const fieldEl = createDomNode('div', 'console-operations-multi-time-field');
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');

   fieldEl.appendChild(listEl);
   fieldEl.appendChild(inputEl);

   return { fieldEl, listEl, inputEl };
}

test('Test_CreateMultiTimeFieldController_TestSavedTimes_ExpectChips', () => {
   const { fieldEl, listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
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

test('Test_CreateMultiTimeFieldController_TestTwelveHour_ExpectChipLabel', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');

   assert.equal(
      listEl.children[0].querySelector('.console-operations-time-chip-label').textContent,
      '1:00 PM'
   );
});

test('Test_CreateMultiTimeFieldController_TestDuplicateFormats_ExpectSingle', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('3:30 PM');
   controller.addTime('15:30');

   assert.deepEqual(controller.getTimes(), [ '3:30 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('Test_CreateMultiTimeFieldController_TestCommitPending_ExpectInputCleared', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   inputEl.value = '3:00 PM';

   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.commitPendingInput();

   assert.deepEqual(controller.getTimes(), [ '3:00 PM' ]);
   assert.equal(inputEl.value, '');
});

test('Test_CreateMultiTimeFieldController_TestDuplicateTime_ExpectIgnored', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('1:00 PM');

   assert.deepEqual(controller.getTimes(), [ '1:00 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('Test_CreateMultiTimeFieldController_TestRemoveTime_ExpectRemoved', () => {
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('2:30 PM');
   controller.removeTime('1:00 PM');

   assert.deepEqual(controller.getTimes(), [ '2:30 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('Test_CreateMultiTimeFieldController_TestRemoveLast_ExpectRemoved', () => {
   const { listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime('1:00 PM');
   controller.addTime('2:30 PM');
   controller.removeLastTime();

   assert.deepEqual(controller.getTimes(), [ '1:00 PM' ]);
   assert.equal(listEl.children.length, 1);
});

test('Test_CreateMultiTimeFieldController_TestMissingListChipEventsAndReset_ExpectHandled', () => {
   const inputEl = createDomNode('input');
   const withoutList = MultiTimeFieldController.createMultiTimeFieldController({
      inputEl,
   });

   assert.equal(withoutList.addTime('1:00 PM'), true);
   assert.deepEqual(withoutList.getTimes(), [ '1:00 PM' ]);
   assert.equal(withoutList.removeLastTime(), true);
   assert.equal(withoutList.removeLastTime(), false);

   const { listEl, inputEl: chipInputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl: chipInputEl,
   });

   controller.addTime('4:00 PM');
   const removeButton = listEl.children[0].querySelector('.console-operations-time-chip-remove');
   const prevented = [];
   removeButton.listeners.mousedown({
      preventDefault: () => { prevented.push(true); },
   });
   assert.deepEqual(prevented, [true]);

   removeButton.listeners.click();
   assert.deepEqual(controller.getTimes(), []);

   chipInputEl.value = '5:00 PM';
   controller.addTime('5:00 PM');
   assert.equal(controller.commitPendingInput(), false);

   chipInputEl.value = '';
   assert.equal(controller.commitPendingInput(), false);

   controller.addTime('6:00 PM');
   chipInputEl.value = 'pending';
   controller.reset();
   assert.deepEqual(controller.getTimes(), []);
   assert.equal(chipInputEl.value, '');
});
