import assert from 'node:assert/strict';
import test from 'node:test';

import { ShowScheduleItemModuleHelper } from '../../../../../scripts/itinerary/panel/components/showScheduleItemModuleHelper.js';

test('Test_Debounce_TestRapidCalls_ExpectSingleLateInvocation', async () => {
   let calls = 0;
   let lastArg = null;
   const debounced = ShowScheduleItemModuleHelper.debounce((value) => {
      calls += 1;
      lastArg = value;
   }, 20);

   debounced('a');
   debounced('b');
   debounced('c');
   assert.equal(calls, 0);
   await new Promise((resolve) => setTimeout(resolve, 40));
   assert.equal(calls, 1);
   assert.equal(lastArg, 'c');
});
