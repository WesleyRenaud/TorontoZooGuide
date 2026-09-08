import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateActions_TestSubmit_ExpectPrimaryButton', () => {
   const actionsEl = ConsoleActionsBuilder.createActions({ submitId: 'save-btn' });
   const button = actionsEl.children[0];
   assert.equal(actionsEl.className, 'console-operations-actions');
   assert.equal(button.id, 'save-btn');
   assert.equal(button.textContent, Strings.actions.save);
});
