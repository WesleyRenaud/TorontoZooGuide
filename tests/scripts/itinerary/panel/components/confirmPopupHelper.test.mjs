import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmPopupHelper } from '../../../../../scripts/itinerary/panel/components/confirmPopupHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateConfirmPopupBody_TestMessageOnly_ExpectBody', () => {
   const body = ConfirmPopupHelper.createConfirmPopupBody('Are you sure?');
   assert.equal(body.className, 'tzg-popup-confirm-body');
   assert.equal(body.children[0].textContent, 'Are you sure?');
});

test('Test_CreateConfirmPopupBody_TestDoNotShowAgain_ExpectCheckbox', () => {
   const result = ConfirmPopupHelper.createConfirmPopupBody('Are you sure?', 'Do not show again');
   assert.equal(result.body.className, 'tzg-popup-confirm-body');
   assert.equal(result.checkbox.type, 'checkbox');
});
