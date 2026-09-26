import assert from 'node:assert/strict';
import test from 'node:test';

import { FlatpickrAdapter } from '../../../scripts/datePickers/flatpickrAdapter.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_InitFlatpickr_TestMissingInput_ExpectNull', () => {
   const inputEl = null;

   const instance = FlatpickrAdapter.initFlatpickr(inputEl);

   assert.equal(instance, null);
});


test('Test_InitFlatpickr_TestMissingLibrary_ExpectNull', () => {
   delete window.flatpickr;
   const inputEl = document.createElement('input');

   const instance = FlatpickrAdapter.initFlatpickr(inputEl);

   assert.equal(instance, null);
});


test('Test_InitFlatpickr_TestAvailableLibrary_ExpectInstance', () => {
   const calls = [];
   const dateFormat = 'Y-m-d';
   window.flatpickr = (inputEl, options) => {
      calls.push({ inputEl, options });
      return { inputEl, options };
   };
   const inputEl = document.createElement('input');

   const instance = FlatpickrAdapter.initFlatpickr(inputEl, { dateFormat });

   assert.equal(instance.inputEl, inputEl);
   assert.equal(calls.at(Position.FIRST).options.allowInput, true);
   assert.equal(calls.at(Position.FIRST).options.dateFormat, dateFormat);
});


test('Test_InitFlatpickr_TestLibraryThrows_ExpectNull', () => {
   const originalError = console.error;
   const errors = [];
   console.error = (...args) => { errors.push(args); };
   window.flatpickr = () => {
      throw new Error('flatpickr boom');
   };

   try {
      const instance = FlatpickrAdapter.initFlatpickr(document.createElement('input'));

      assert.equal(instance, null);
      assert.equal(errors.length, Position.SECOND);
      assert.match(String(errors.at(Position.FIRST).at(Position.FIRST)), /flatpickr/);
   } finally {
      console.error = originalError;
   }
});
