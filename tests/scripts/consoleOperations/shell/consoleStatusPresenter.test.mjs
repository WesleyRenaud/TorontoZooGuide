import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleStatusPresenter } from '../../../../scripts/consoleOperations/shell/consoleStatusPresenter.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_SetStatus_TestMessageAndKind_ExpectUpdatedElement', () => {
   const el = document.createElement('div');

   ConsoleStatusPresenter.setStatus(el, 'Saved', 'is-success');

   assert.equal(el.textContent, 'Saved');
   assert.equal(el.classList.contains('is-success'), true);

   ConsoleStatusPresenter.setStatus(el, 'Failed', 'is-error');

   assert.equal(el.textContent, 'Failed');
   assert.equal(el.classList.contains('is-error'), true);
});

test('Test_SetStatus_TestMissingElement_ExpectNoThrow', () => {
   assert.doesNotThrow(() => ConsoleStatusPresenter.setStatus(null, 'Saved', 'is-success'));
});
