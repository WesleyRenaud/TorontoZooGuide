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
