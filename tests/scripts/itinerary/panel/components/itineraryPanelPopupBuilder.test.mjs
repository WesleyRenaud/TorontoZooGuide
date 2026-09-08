import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelPopupBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelPopupBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_JoinClassNames_TestValues_ExpectJoined', () => {
   assert.equal(ItineraryPanelPopupBuilder.joinClassNames('a', '', 'b', null), 'a b');
});

test('Test_CreatePopupButton_TestConfig_ExpectButton', () => {
   const button = ItineraryPanelPopupBuilder.createPopupButton({
      className: 'tzg-popup-confirm',
      text: 'OK',
   });
   assert.equal(button.type, 'button');
   assert.equal(button.className, 'tzg-popup-confirm');
   assert.equal(button.textContent, 'OK');
});
