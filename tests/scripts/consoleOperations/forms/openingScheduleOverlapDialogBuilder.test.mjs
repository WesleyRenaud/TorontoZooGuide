import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleOverlapDialogBuilder } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapDialogBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks({
   before: () => {
      document.createElementNS = (_ns, tagName) => {
         const attrs = {};
         const node = {
            tagName,
            attrs,
            children: [],
            setAttribute(key, value) { attrs[key] = value; },
            append(...nodes) { this.children.push(...nodes); },
         };
         return node;
      };
   },
});

test('Test_CreateDialogButton_TestText_ExpectButton', () => {
   const button = OpeningScheduleOverlapDialogBuilder.createDialogButton('btn', 'Cancel');
   assert.equal(button.type, 'button');
   assert.equal(button.className, 'btn');
   assert.equal(button.textContent, 'Cancel');
});

test('Test_CreateDialogLayout_TestDefaults_ExpectDialogParts', () => {
   const layout = OpeningScheduleOverlapDialogBuilder.createDialogLayout();
   assert.equal(layout.root.className, 'console-overlap-dialog-root');
   assert.equal(layout.buttons.cancel.textContent, Strings.itinerary.actions.cancel);
   assert.equal(layout.buttons.replace.textContent, Strings.confirm.deleteOldSchedules);
   assert.equal(layout.buttons.trim.textContent, Strings.confirm.trimOldSchedules);
   assert.match(layout.root.textContent, new RegExp(Strings.confirm.openingScheduleOverlapTitle));
});
