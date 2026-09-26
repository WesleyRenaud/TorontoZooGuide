import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardFragment } from '../../../../scripts/itinerary/wizard/wizardFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      document.querySelector('.tzg-popup')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-popup')?.remove();
   },
});


test('Test_ShowItineraryWizardPopup_TestMissingMount_ExpectNoOp', () => {
   const title = 'Missing mount';

   assert.doesNotThrow(() => {
      WizardFragment.showItineraryWizardPopup({
         mountEl: null,
         title,
      });
   });
});


test('Test_ShowItineraryWizardPopup_TestMount_ExpectDismissablePopup', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const titleText = 'Empty itinerary';
   const messageText = 'Select at least one item.';
   const buttonText = 'Got it';

   WizardFragment.showItineraryWizardPopup({
      mountEl,
      title: titleText,
      message: messageText,
      buttonText,
   });

   const popup = mountEl.querySelector('.tzg-popup');
   const title = popup?.querySelector('.itin-top-title');
   const message = popup?.querySelector('.tzg-popup-message');
   const okButton = popup?.querySelector('.tzg-popup-ok');

   assert.ok(popup);
   assert.equal(title?.textContent, titleText);
   assert.equal(message?.textContent, messageText);
   assert.equal(okButton?.textContent, buttonText);

   okButton?.click();

   assert.equal(mountEl.querySelector('.tzg-popup'), null);
});


test('Test_ShowItineraryWizardPopup_TestExisting_ExpectReplaced', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const firstTitle = 'First popup';
   const secondTitle = 'Second popup';

   WizardFragment.showItineraryWizardPopup({
      mountEl,
      title: firstTitle,
   });
   WizardFragment.showItineraryWizardPopup({
      mountEl,
      title: secondTitle,
   });

   const popups = mountEl.querySelectorAll('.tzg-popup');

   assert.equal(popups.length, 1);
   assert.equal(
      popups[Position.FIRST]?.querySelector('.itin-top-title')?.textContent,
      secondTitle
   );
});
