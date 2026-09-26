import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_SetStatus_TestSuccessKind_ExpectUpdatedElement', () => {
   const message = 'Saved';
   const kind = 'is-success';
   const el = document.createElement('div');

   ConsoleStatusPresenter.setStatus(el, message, kind);

   assert.equal(el.textContent, message);
   assert.equal(el.classList.contains(kind), true);
});


test('Test_SetStatus_TestErrorKind_ExpectUpdatedElement', () => {
   const message = 'Failed';
   const kind = 'is-error';
   const el = document.createElement('div');

   ConsoleStatusPresenter.setStatus(el, message, kind);

   assert.equal(el.textContent, message);
   assert.equal(el.classList.contains(kind), true);
});


test('Test_SetStatus_TestMissingElement_ExpectNoThrow', () => {
   const el = null;

   assert.doesNotThrow(() => ConsoleStatusPresenter.setStatus(el, 'Saved', 'is-success'));
});
