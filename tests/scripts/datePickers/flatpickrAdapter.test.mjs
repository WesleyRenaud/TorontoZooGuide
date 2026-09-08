import assert from 'node:assert/strict';
import test from 'node:test';

import { FlatpickrAdapter } from '../../../scripts/datePickers/flatpickrAdapter.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_InitFlatpickr_TestMissingInput_ExpectNull', () => {
   assert.equal(FlatpickrAdapter.initFlatpickr(null), null);
});

test('Test_InitFlatpickr_TestMissingLibrary_ExpectNull', () => {
   delete window.flatpickr;
   assert.equal(FlatpickrAdapter.initFlatpickr(document.createElement('input')), null);
});

test('Test_InitFlatpickr_TestAvailableLibrary_ExpectInstance', () => {
   const calls = [];
   window.flatpickr = (inputEl, options) => {
      calls.push({ inputEl, options });
      return { inputEl, options };
   };

   const inputEl = document.createElement('input');
   const instance = FlatpickrAdapter.initFlatpickr(inputEl, { dateFormat: 'Y-m-d' });

   assert.equal(instance.inputEl, inputEl);
   assert.equal(calls[0].options.allowInput, true);
   assert.equal(calls[0].options.dateFormat, 'Y-m-d');
});
