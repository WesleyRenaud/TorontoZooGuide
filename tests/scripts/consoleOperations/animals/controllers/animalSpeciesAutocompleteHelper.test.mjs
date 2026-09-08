import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSpeciesAutocompleteHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalSpeciesAutocompleteHelper.js';

test('Test_Debounce_TestRapidCalls_ExpectSingleLateInvocation', async () => {
   let calls = 0;
   const debounced = AnimalSpeciesAutocompleteHelper.debounce(() => {
      calls += 1;
   }, 20);

   debounced();
   debounced();
   assert.equal(calls, 0);
   await new Promise((resolve) => setTimeout(resolve, 40));
   assert.equal(calls, 1);
});
