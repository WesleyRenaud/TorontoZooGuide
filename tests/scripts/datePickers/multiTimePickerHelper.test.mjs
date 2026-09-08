import assert from 'node:assert/strict';
import test from 'node:test';

import { MultiTimePickerHelper } from '../../../scripts/datePickers/multiTimePickerHelper.js';
import { TimePickerEnterHandler } from '../../../scripts/datePickers/timePickerEnterHandler.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResetPickerSelection_TestInstance_ExpectCleared', () => {
   const calls = [];
   MultiTimePickerHelper.resetPickerSelection({
      setDate: (...args) => { calls.push(args); },
   });
   assert.deepEqual(calls, [[[], false]]);
   MultiTimePickerHelper.resetPickerSelection(null);
});

test('Test_CreateMultiTimeCommitController_TestCommitTime_ExpectCommitted', () => {
   const commits = [];
   const resets = [];
   const inputEl = document.createElement('input');
   inputEl.value = '11:00 AM';

   const controller = MultiTimePickerHelper.createMultiTimeCommitController({
      inputEl,
      onCommitTime: (time) => { commits.push(time); },
   });

   const instance = {
      setDate: (...args) => { resets.push(args); },
   };

   assert.equal(controller.commitTime('  ', instance), false);
   assert.equal(controller.commitTime('11:00 AM', instance), true);
   assert.deepEqual(commits, ['11:00 AM']);
   assert.equal(inputEl.value, '');
   assert.deepEqual(resets, [[[], false]]);
});

test('Test_CreateMultiTimeCommitController_TestCommitResolvedTime_ExpectUsesResolver', () => {
   const commits = [];
   const inputEl = document.createElement('input');
   const original = TimePickerEnterHandler.resolveOpenTimePickerValue;
   TimePickerEnterHandler.resolveOpenTimePickerValue = () => '2:00 PM';

   try {
      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime: (time) => { commits.push(time); },
      });
      assert.equal(controller.commitResolvedTime({ setDate() {} }), true);
      assert.deepEqual(commits, ['2:00 PM']);
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

test('Test_CreateMultiTimeCommitController_TestCommitAfterInputSettles_ExpectPendingCommit', async () => {
   const commits = [];
   const inputEl = document.createElement('input');
   const original = TimePickerEnterHandler.resolveOpenTimePickerValue;
   TimePickerEnterHandler.resolveOpenTimePickerValue = () => '6:00 PM';

   try {
      const controller = MultiTimePickerHelper.createMultiTimeCommitController({
         inputEl,
         onCommitTime: (time) => { commits.push(time); },
      });

      inputEl.value = '';
      controller.commitAfterInputSettles({ setDate() {} }, '3:00 PM');
      await new Promise((resolve) => setTimeout(resolve, 0));
      assert.deepEqual(commits, ['3:00 PM']);

      commits.length = 0;
      inputEl.value = 'typed';
      controller.commitAfterInputSettles({ setDate() {} }, '4:00 PM');
      await new Promise((resolve) => setTimeout(resolve, 0));
      assert.deepEqual(commits, ['6:00 PM']);
   } finally {
      TimePickerEnterHandler.resolveOpenTimePickerValue = original;
   }
});

test('Test_WireMultiTimeInputEvents_TestBlurOpenAndPending_ExpectGuards', async () => {
   const inputEl = document.createElement('input');
   const settles = [];
   const openPicker = { isOpen: true };
   const closedPicker = { isOpen: false };

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

   MultiTimePickerHelper.wireMultiTimeInputEvents(
      inputEl,
      closedPicker,
      {
         commitAfterInputSettles: (...args) => { settles.push(args); },
      }
   );

   inputEl.value = '5:00 PM';
   inputEl.listeners.blur();
   await new Promise((resolve) => setTimeout(resolve, 0));
   assert.equal(settles.length, 1);
   assert.equal(settles[0][1], '5:00 PM');
});
