import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSpeciesAutocompleteHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesAutocompleteHelper.js';


test('Test_Debounce_TestRapidCalls_ExpectSingleLateInvocation', async () => {
   let calls = 0;
   const waitMs = 20;
   const debounced = AnimalSpeciesAutocompleteHelper.debounce(() => {
      calls += 1;
   }, waitMs);

   debounced();
   debounced();
   const callsBeforeWait = calls;
   await new Promise((resolve) => setTimeout(resolve, waitMs * 2));

   assert.equal(callsBeforeWait, 0);
   assert.equal(calls, 1);
});
