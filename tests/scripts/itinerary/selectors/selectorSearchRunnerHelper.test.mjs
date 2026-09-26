import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorSearchRunnerHelper } from '../../../../scripts/itinerary/selectors/selectorSearchRunnerHelper.js';


test('Test_Debounce_TestRapidCalls_ExpectSingleLateInvocation', async () => {
   let calls = 0;
   let lastArg = null;
   const first = 'a';
   const second = 'b';
   const third = 'c';
   const debounced = SelectorSearchRunnerHelper.debounce((value) => {
      calls += 1;
      lastArg = value;
   }, 20);

   debounced(first);
   debounced(second);
   debounced(third);

   assert.equal(calls, 0);
   await new Promise((resolve) => setTimeout(resolve, 40));
   assert.equal(calls, 1);
   assert.equal(lastArg, third);
});
