import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkDropdownResetHelper } from '../../../../../scripts/consoleOperations/guardiansTalks/helpers/guardiansTalkDropdownResetHelper.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResetTalkDropdown_TestFilterControllerClear_ExpectDelegates', () => {
   const calls = [];
   const talkNameEl = document.createElement('select');
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;

   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = () => {
      calls.push('populate');
   };

   try {
      GuardiansTalkDropdownResetHelper.resetTalkDropdown({
         talkNameEl,
         talkLocationFilterController: {
            clear: () => {
               calls.push('clear');
            },
         },
      });

      assert.deepEqual(calls, ['clear']);
   } finally {
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
   }
});

test('Test_ResetTalkDropdown_TestSelectWithoutFilter_ExpectEmptyPopulate', () => {
   const talkNameEl = document.createElement('select');
   const originalPopulate = ConsoleDropdownPopulator.populateGuardiansTalkDropdown;
   let captured;

   ConsoleDropdownPopulator.populateGuardiansTalkDropdown = (el, talks) => {
      captured = { el, talks };
   };

   try {
      GuardiansTalkDropdownResetHelper.resetTalkDropdown({ talkNameEl });
      assert.deepEqual(captured, { el: talkNameEl, talks: [] });
   } finally {
      ConsoleDropdownPopulator.populateGuardiansTalkDropdown = originalPopulate;
   }
});

test('Test_ResetTalkDropdown_TestInputWithoutFilter_ExpectClearsValue', () => {
   const talkNameEl = document.createElement('input');
   talkNameEl.value = 'Keeper Talk';

   GuardiansTalkDropdownResetHelper.resetTalkDropdown({ talkNameEl });
   assert.equal(talkNameEl.value, '');
});
