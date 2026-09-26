import assert from 'node:assert/strict';
import test from 'node:test';

import { ShowScheduleItemModuleHelper } from '../../../../../scripts/itinerary/panel/components/showScheduleItemModuleHelper.js';


test('Test_Debounce_TestRapidCalls_ExpectSingleLateInvocation', async () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const gorilla = 'Western Lowland Gorilla';
   const delayMs = 20;
   let calls = 0;
   let lastArg = null;
   const debounced = ShowScheduleItemModuleHelper.debounce((value) => {
      calls += 1;
      lastArg = value;
   }, delayMs);

   debounced(lion);
   debounced(tiger);
   debounced(gorilla);
   const callsBeforeWait = calls;
   await new Promise((resolve) => setTimeout(resolve, delayMs * 2));

   assert.equal(callsBeforeWait, 0);
   assert.equal(calls, 1);
   assert.equal(lastArg, gorilla);
});
