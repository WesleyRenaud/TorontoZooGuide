import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleActionsBuilder } from '../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateActions_TestSubmit_ExpectPrimaryButton', () => {
   const submitId = 'save-btn';

   const actionsEl = ConsoleActionsBuilder.createActions({ submitId });

   const button = actionsEl.children[Position.FIRST];
   assert.equal(actionsEl.className, 'console-operations-actions');
   assert.equal(button.id, submitId);
   assert.equal(button.textContent, Strings.actions.save);
});
