import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WizardPopup } from '../../../../scripts/itinerary/wizard/wizardPopup.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

test.describe('showItineraryWizardPopup', () => {
   installDomTestHooks({
      after: () => {
         document.querySelector('.tzg-popup')?.__tzgPopupCleanup?.();
         document.querySelector('.tzg-popup')?.remove();
      },
   });

   test('Test_ShowItineraryWizardPopup_TestMissingMount_ExpectNoOp', () => {
      WizardPopup.showItineraryWizardPopup({
         mountEl: null,
         title: 'Missing mount',
      });
   });

   test('Test_ShowItineraryWizardPopup_TestMount_ExpectDismissablePopup', () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      WizardPopup.showItineraryWizardPopup({
         mountEl,
         title: 'Empty itinerary',
         message: 'Select at least one item.',
         buttonText: 'Got it',
      });

      const popup = mountEl.querySelector('.tzg-popup');
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const okButton = popup?.querySelector('.tzg-popup-ok');

      assert.ok(popup);
      assert.equal(title?.textContent, 'Empty itinerary');
      assert.equal(message?.textContent, 'Select at least one item.');
      assert.equal(okButton?.textContent, 'Got it');

      okButton?.click();

      assert.equal(mountEl.querySelector('.tzg-popup'), null);
   });

   test('Test_ShowItineraryWizardPopup_TestExisting_ExpectReplaced', () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      WizardPopup.showItineraryWizardPopup({
         mountEl,
         title: 'First popup',
      });
      WizardPopup.showItineraryWizardPopup({
         mountEl,
         title: 'Second popup',
      });

      const popups = mountEl.querySelectorAll('.tzg-popup');

      assert.equal(popups.length, 1);
      assert.equal(
         popups[0]?.querySelector('.itin-top-title')?.textContent,
         'Second popup'
      );
   });
});
