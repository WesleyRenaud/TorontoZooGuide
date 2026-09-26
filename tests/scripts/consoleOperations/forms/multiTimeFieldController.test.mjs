import assert from 'node:assert/strict';
import test from 'node:test';

import { MultiTimeFieldController } from '../../../../scripts/consoleOperations/forms/multiTimeFieldController.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
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
   const afternoon = '1:00 PM';
   const later = '2:30 PM';
   const times = [afternoon, later];
   const { fieldEl, listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);
   controller.addTime(later);

   assert.equal(listEl.children.length, times.length);
   assert.equal(
      fieldEl.classList.contains('console-operations-multi-time-field--has-times'),
      true
   );
   assert.deepEqual(controller.getTimes(), times);
});


test('Test_CreateMultiTimeFieldController_TestTwelveHour_ExpectChipLabel', () => {
   const afternoon = '1:00 PM';
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);

   assert.equal(
      listEl.children[Position.FIRST].querySelector('.console-operations-time-chip-label').textContent,
      afternoon
   );
});


test('Test_CreateMultiTimeFieldController_TestDuplicateFormats_ExpectSingle', () => {
   const afternoon = '3:30 PM';
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);
   controller.addTime('15:30');

   assert.deepEqual(controller.getTimes(), [afternoon]);
   assert.equal(listEl.children.length, 1);
});


test('Test_CreateMultiTimeFieldController_TestCommitPending_ExpectInputCleared', () => {
   const afternoon = '3:00 PM';
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   inputEl.value = afternoon;
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.commitPendingInput();

   assert.deepEqual(controller.getTimes(), [afternoon]);
   assert.equal(inputEl.value, '');
});


test('Test_CreateMultiTimeFieldController_TestDuplicateTime_ExpectIgnored', () => {
   const afternoon = '1:00 PM';
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);
   controller.addTime(afternoon);

   assert.deepEqual(controller.getTimes(), [afternoon]);
   assert.equal(listEl.children.length, 1);
});


test('Test_CreateMultiTimeFieldController_TestRemoveTime_ExpectRemoved', () => {
   const afternoon = '1:00 PM';
   const later = '2:30 PM';
   const listEl = createDomNode('div');
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);
   controller.addTime(later);
   controller.removeTime(afternoon);

   assert.deepEqual(controller.getTimes(), [later]);
   assert.equal(listEl.children.length, 1);
});


test('Test_CreateMultiTimeFieldController_TestRemoveLast_ExpectRemoved', () => {
   const afternoon = '1:00 PM';
   const later = '2:30 PM';
   const { listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });

   controller.addTime(afternoon);
   controller.addTime(later);
   controller.removeLastTime();

   assert.deepEqual(controller.getTimes(), [afternoon]);
   assert.equal(listEl.children.length, 1);
});


test('Test_CreateMultiTimeFieldController_TestMissingList_ExpectTimesTracked', () => {
   const afternoon = '1:00 PM';
   const inputEl = createDomNode('input');
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      inputEl,
   });

   const added = controller.addTime(afternoon);
   const times = controller.getTimes();
   const removed = controller.removeLastTime();
   const removedAgain = controller.removeLastTime();

   assert.equal(added, true);
   assert.deepEqual(times, [afternoon]);
   assert.equal(removed, true);
   assert.equal(removedAgain, false);
});


test('Test_CreateMultiTimeFieldController_TestChipRemove_ExpectCleared', () => {
   const afternoon = '4:00 PM';
   const { listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });
   controller.addTime(afternoon);
   const removeButton = listEl.children[Position.FIRST].querySelector('.console-operations-time-chip-remove');
   const prevented = [];

   removeButton.listeners.mousedown({
      preventDefault: () => {
         prevented.push(true);
      },
   });
   removeButton.listeners.click();

   assert.deepEqual(prevented, [true]);
   assert.deepEqual(controller.getTimes(), []);
});


test('Test_CreateMultiTimeFieldController_TestCommitExistingOrBlank_ExpectFalse', () => {
   const afternoon = '5:00 PM';
   const { listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });
   inputEl.value = afternoon;
   controller.addTime(afternoon);

   const existing = controller.commitPendingInput();
   inputEl.value = '';
   const blank = controller.commitPendingInput();

   assert.equal(existing, false);
   assert.equal(blank, false);
});


test('Test_CreateMultiTimeFieldController_TestReset_ExpectCleared', () => {
   const afternoon = '6:00 PM';
   const { listEl, inputEl } = _createMultiTimeFieldDom();
   const controller = MultiTimeFieldController.createMultiTimeFieldController({
      listEl,
      inputEl,
   });
   controller.addTime(afternoon);
   inputEl.value = 'pending';

   controller.reset();

   assert.deepEqual(controller.getTimes(), []);
   assert.equal(inputEl.value, '');
});
