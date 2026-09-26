import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmPopupHelper } from '../../../../../scripts/itinerary/panel/components/confirmPopupHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateConfirmPopupBody_TestMessageOnly_ExpectBody', () => {
   const message = 'Clear this itinerary?';

   const body = ConfirmPopupHelper.createConfirmPopupBody(message);

   assert.equal(body.className, 'tzg-popup-confirm-body');
   assert.equal(body.children.at(Position.FIRST).textContent, message);
});


test('Test_CreateConfirmPopupBody_TestDoNotShowAgain_ExpectCheckbox', () => {
   const message = 'Clear this itinerary?';
   const doNotShowAgainLabel = 'Do not show again';

   const result = ConfirmPopupHelper.createConfirmPopupBody(message, doNotShowAgainLabel);

   assert.equal(result.body.className, 'tzg-popup-confirm-body');
   assert.equal(result.checkbox.type, 'checkbox');
});
