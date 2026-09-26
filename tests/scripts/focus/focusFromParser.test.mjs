import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusFromParser } from '../../../scripts/focus/focusFromParser.js';
import { FocusFromQueryHelper } from '../../../scripts/focus/focusFromQueryHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_InitFocusFromQuery_TestMissingRequest_ExpectNoOp', () => {
   const original = FocusFromQueryHelper.getFocusRequestFromQuery;
   FocusFromQueryHelper.getFocusRequestFromQuery = () => null;
   const focuses = [];

   try {
      FocusFromParser.initFocusFromQuery({ onFocus: (request) => focuses.push(request) });

      assert.deepEqual(focuses, []);
   } finally {
      FocusFromQueryHelper.getFocusRequestFromQuery = original;
   }
});


test('Test_InitFocusFromQuery_TestRequest_ExpectFocusAndReplaceState', () => {
   const originalGet = FocusFromQueryHelper.getFocusRequestFromQuery;
   const replaces = [];
   const focuses = [];
   const request = { type: 'animal', id: 'lion' };
   const pathname = '/map';
   FocusFromQueryHelper.getFocusRequestFromQuery = () => request;
   globalThis.history = {
      replaceState: (...args) => { replaces.push(args); },
   };
   globalThis.window.location = { pathname };

   try {
      FocusFromParser.initFocusFromQuery({
         onFocus: (nextRequest) => focuses.push(nextRequest),
      });

      assert.deepEqual(focuses, [request]);
      assert.deepEqual(replaces, [[{}, '', pathname]]);
   } finally {
      FocusFromQueryHelper.getFocusRequestFromQuery = originalGet;
      delete globalThis.history;
   }
});
