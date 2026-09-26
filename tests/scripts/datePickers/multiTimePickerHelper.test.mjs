import assert from 'node:assert/strict';
import test from 'node:test';

import { MultiTimePickerHelper } from '../../../scripts/datePickers/multiTimePickerHelper.js';
import { TimePickerEnterHandler } from '../../../scripts/datePickers/timePickerEnterHandler.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResetPickerSelection_TestInstance_ExpectCleared', () => {
   const calls = [];

   MultiTimePickerHelper.resetPickerSelection({
      setDate: (...args) => { calls.push(args); },
   });

   assert.deepEqual(calls, [[[], false]]);
});


test('Test_ResetPickerSelection_TestNull_ExpectNoThrow', () => {
   const reset = () => MultiTimePickerHelper.resetPickerSelection(null);

   assert.doesNotThrow(reset);
});


test('Test_CreateMultiTimeCommitController_TestBlankTime_ExpectFalse', () => {
   const inputEl = document.createElement('input');
   const controller = MultiTimePickerHelper.createMultiTimeCommitController({
      inputEl,
      onCommitTime: () => {},
   });

   const committed = controller.commitTime('  ', { setDate() {} });

   assert.equal(committed, false);
});


test('Test_CreateMultiTimeCommitController_TestCommitTime_ExpectCommitted', () => {
   const commits = [];
   const resets = [];
   const time = '11:00 AM';
   const inputEl = document.createElement('input');
   inputEl.value = time;
   const controller = MultiTimePickerHelper.createMultiTimeCommitController({
      inputEl,
      onCommitTime: (nextTime) => { commits.push(nextTime); },
   });
   const instance = {
      setDate: (...args) => { resets.push(args); },
   };

   const committed = controller.commitTime(time, instance);

   assert.equal(committed, true);
   assert.deepEqual(commits, [time]);
   assert.equal(inputEl.value, '');
   assert.deepEqual(resets, [[[], false]]);
});


test('Test_CreateMultiTimeCommitController_TestCommitResolvedTime_ExpectUsesResolver', () => {
   const commits = [];
   const time = '2:00 PM';
   const inputEl = document.createElement('input');
   const original = TimePickerEnterHandler.resolveOpenTimePickerValue;
   TimePickerEnterHandler.resolveOpenTimePickerValue = () => time;

   try {
      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime: (nextTime) => { commits.push(nextTime); },
      });

      const committed = controller.commitResolvedTime({ setDate() {} });

      assert.equal(committed, true);
      assert.deepEqual(commits, [time]);
   } finally {
      TimePickerEnterHandler.resolveOpenTimePickerValue = original;
   }
});


test('Test_WireMultiTimeInputEvents_TestBackspace_ExpectRemoveLast', () => {
   const inputEl = document.createElement('input');
   inputEl.value = '';
   const closes = [];
   const removes = [];
   const prevented = [];

   MultiTimePickerHelper.wireMultiTimeInputEvents(
      inputEl,
      { close: () => { closes.push(true); } },
      { commitAfterInputSettles() {} },
      {
         onRemoveLastTime: () => {
            removes.push(true);
            return true;
         },
      }
   );
   inputEl.listeners.keydown({
      key: 'Backspace',
      preventDefault: () => { prevented.push('default'); },
      stopImmediatePropagation: () => { prevented.push('stop'); },
   });

   assert.deepEqual(removes, [true]);
   assert.deepEqual(closes, [true]);
   assert.deepEqual(prevented, ['default', 'stop']);
});


test('Test_CreateMultiTimeCommitController_TestCommitAfterInputSettlesEmpty_ExpectFallback', async () => {
   const commits = [];
   const fallback = '3:00 PM';
   const inputEl = document.createElement('input');
   const original = TimePickerEnterHandler.resolveOpenTimePickerValue;
   TimePickerEnterHandler.resolveOpenTimePickerValue = () => '6:00 PM';

   try {
      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime: (time) => { commits.push(time); },
      });
      inputEl.value = '';

      controller.commitAfterInputSettles({ setDate() {} }, fallback);
      await new Promise((resolve) => setTimeout(resolve, 0));

      assert.deepEqual(commits, [fallback]);
   } finally {
      TimePickerEnterHandler.resolveOpenTimePickerValue = original;
   }
});


test('Test_CreateMultiTimeCommitController_TestCommitAfterInputSettlesTyped_ExpectResolved', async () => {
   const commits = [];
   const resolved = '6:00 PM';
   const inputEl = document.createElement('input');
   const original = TimePickerEnterHandler.resolveOpenTimePickerValue;
   TimePickerEnterHandler.resolveOpenTimePickerValue = () => resolved;

   try {
      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime: (time) => { commits.push(time); },
      });
      inputEl.value = 'typed';

      controller.commitAfterInputSettles({ setDate() {} }, '4:00 PM');
      await new Promise((resolve) => setTimeout(resolve, 0));

      assert.deepEqual(commits, [resolved]);
   } finally {
      TimePickerEnterHandler.resolveOpenTimePickerValue = original;
   }
});


test('Test_WireMultiTimeInputEvents_TestBlurWhileOpen_ExpectNoSettle', async () => {
   const inputEl = document.createElement('input');
   const settles = [];
   const openPicker = { isOpen: true };

   MultiTimePickerHelper.wireMultiTimeInputEvents(
      inputEl,
      openPicker,
      {
         commitAfterInputSettles: (...args) => { settles.push(args); },
      }
   );
   inputEl.value = '4:00 PM';
   inputEl.listeners.blur();
   await new Promise((resolve) => setTimeout(resolve, 0));

   assert.deepEqual(settles, []);
});


test('Test_WireMultiTimeInputEvents_TestBlurWhileClosed_ExpectSettle', async () => {
   const inputEl = document.createElement('input');
   const settles = [];
   const time = '5:00 PM';
   const closedPicker = { isOpen: false };

   MultiTimePickerHelper.wireMultiTimeInputEvents(
      inputEl,
      closedPicker,
      {
         commitAfterInputSettles: (...args) => { settles.push(args); },
      }
   );
   inputEl.value = time;
   inputEl.listeners.blur();
   await new Promise((resolve) => setTimeout(resolve, 0));

   assert.equal(settles.length, Position.SECOND);
   assert.equal(settles.at(Position.FIRST).at(Position.SECOND), time);
});
