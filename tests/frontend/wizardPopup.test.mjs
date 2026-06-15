import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { showItineraryWizardPopup } from '../../scripts/itinerary/wizard/wizardPopup.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test.describe('showItineraryWizardPopup', () => {
   beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      document.querySelector('.tzg-popup')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-popup')?.remove();
      teardownDocument();
      delete globalThis.window;
   });

   test('no-ops when mountEl is missing', () => {
      showItineraryWizardPopup({
         mountEl: null,
         title: 'Missing mount',
      });
   });

   test('renders a dismissable popup on the mount element', () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      showItineraryWizardPopup({
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

   test('replaces an existing popup before mounting a new one', () => {
      const mountEl = createDomNode('div', 'wizard-mount');

      showItineraryWizardPopup({
         mountEl,
         title: 'First popup',
      });
      showItineraryWizardPopup({
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
