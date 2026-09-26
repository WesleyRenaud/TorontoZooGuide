import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelPopupBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelPopupBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_JoinClassNames_TestValues_ExpectJoined', () => {
   const firstClass = 'tzg-popup';
   const emptyClass = '';
   const secondClass = 'tzg-popup-open';
   const missingClass = null;

   const classNames = ItineraryPanelPopupBuilder.joinClassNames(
      firstClass,
      emptyClass,
      secondClass,
      missingClass
   );

   assert.equal(classNames, `${firstClass} ${secondClass}`);
});


test('Test_CreatePopupButton_TestConfig_ExpectButton', () => {
   const className = 'tzg-popup-confirm';
   const text = 'OK';

   const button = ItineraryPanelPopupBuilder.createPopupButton({
      className,
      text,
   });

   assert.equal(button.type, 'button');
   assert.equal(button.className, className);
   assert.equal(button.textContent, text);
});
