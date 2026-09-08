import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleStatusBuilder } from '../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateStatus_TestId_ExpectStatusElement', () => {
   const statusEl = ConsoleStatusBuilder.createStatus({ statusId: 'animals-status' });

   assert.equal(statusEl.tagName.toUpperCase(), 'DIV');
   assert.equal(statusEl.id, 'animals-status');
   assert.equal(statusEl.className, 'console-operations-status');
   assert.equal(statusEl.getAttribute('aria-live'), 'polite');
});
