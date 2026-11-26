import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryCardModal } from '../../../scripts/itinerary/itineraryCardModal.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

afterEach(() => {
   if (globalThis.document) {
      ItineraryCardModal.release();
   }

   ItineraryCardModal.modal = null;
   ItineraryCardModal.mountEl = null;
   ItineraryCardModal.onEscape = null;
   ItineraryCardModal.installedDocument = null;
});


function _focusable(tagName = 'button', className = '') {
   const element = createDomNode(tagName, className);
   element.focusCalls = [];
   element.focus = (options) => {
      element.focusCalls.push(options);
      document.activeElement = element;
   };

   if (tagName !== 'button') {
      element.setAttribute('tabindex', '0');
   }

   return element;
}


function _key(key, extra = {}) {
   return {
      key,
      defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
      stopPropagation() { this.propagationStopped = true; },
      ...extra,
   };
}


function _buildPage() {
   const page = createDomNode('div', 'itinerary-layout');
   const panel = document.querySelector('.itinerary-panel');
   const mountEl = document.getElementById('itineraryFlow');
   const buildButton = _focusable('button', 'itin-panel-build-btn');
   const overlay = createDomNode('div', 'itin-overlay');
   const card = createDomNode('section', 'itin-card');
   const title = _focusable('h1', 'itin-h1');
   const closeButton = _focusable('button', 'itin-close');
   const nextButton = _focusable('button', 'itin-next');

   title.removeAttribute('tabindex');
   title.textContent = 'Set Visit Date';
   card.append(title, closeButton, nextButton);
   overlay.appendChild(card);
   mountEl.replaceChildren(overlay);
   panel.replaceChildren(buildButton);
   page.append(panel, mountEl);

   return {
      page,
      panel,
      mountEl,
      overlay,
      card,
      title,
      closeButton,
      nextButton,
      buildButton,
   };
}


test('Test_SyncOpenCard_TestMissingMount_ExpectNoThrow', () => {
   assert.doesNotThrow(() => {
      ItineraryCardModal.syncOpenCard(null);
      ItineraryCardModal.release();
   });
});


test('Test_SyncOpenCard_TestWizardCard_ExpectHeadingFocusedAndBackgroundInert', () => {
   const page = _buildPage();
   const escapes = [];

   ItineraryCardModal.syncOpenCard(page.mountEl, {
      returnFocusFallback: page.buildButton,
      onEscape: () => {
         escapes.push('escape');
      },
   });

   assert.equal(page.card.getAttribute('role'), 'dialog');
   assert.equal(page.card.getAttribute('aria-labelledby'), ItineraryCardModal.TITLE_ID);
   assert.equal(page.title.id, ItineraryCardModal.TITLE_ID);
   assert.equal(page.title.getAttribute('tabindex'), '-1');
   assert.equal(document.activeElement, page.title);
   assert.equal(page.panel.hasAttribute('inert'), true);
   assert.equal(page.mountEl.hasAttribute('inert'), false);
   assert.equal(ItineraryCardModal.getTopCard(), page.card);
   assert.equal(ItineraryCardModal.getTitle(page.card), page.title);
   assert.equal(ItineraryCardModal.getBuildItineraryButton(), page.buildButton);
   assert.deepEqual(escapes, []);
});


test('Test_SyncOpenCard_TestStepChange_ExpectFocusMovesToNewHeading', () => {
   const page = _buildPage();
   ItineraryCardModal.syncOpenCard(page.mountEl, {
      returnFocusFallback: page.buildButton,
   });

   const nextTitle = _focusable('h1', 'itin-h1');
   nextTitle.removeAttribute('tabindex');
   nextTitle.textContent = 'Select Regions';
   page.card.replaceChildren(nextTitle, page.closeButton, page.nextButton);

   ItineraryCardModal.syncOpenCard(page.mountEl, {
      returnFocusFallback: page.buildButton,
   });

   assert.equal(document.activeElement, nextTitle);
   assert.equal(nextTitle.id, ItineraryCardModal.TITLE_ID);
   assert.equal(page.panel.hasAttribute('inert'), true);
});


test('Test_HandleTab_TestWrapsInsideCard', () => {
   const page = _buildPage();
   ItineraryCardModal.syncOpenCard(page.mountEl);
   page.closeButton.focus();

   const shiftTab = _key('Tab', { shiftKey: true });
   ItineraryCardModal.modal.handleKeydown(shiftTab);

   assert.equal(shiftTab.defaultPrevented, true);
   assert.equal(document.activeElement, page.nextButton);

   const tab = _key('Tab');
   ItineraryCardModal.modal.handleKeydown(tab);

   assert.equal(tab.defaultPrevented, true);
   assert.equal(document.activeElement, page.closeButton);
});


test('Test_HandleEscape_TestOpenCard_ExpectOnEscape', () => {
   const page = _buildPage();
   const escapes = [];
   ItineraryCardModal.syncOpenCard(page.mountEl, {
      onEscape: () => {
         escapes.push('escape');
      },
   });

   const event = _key('Escape');
   ItineraryCardModal.handleDocumentKeydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(event.propagationStopped, true);
   assert.deepEqual(escapes, ['escape']);
});


test('Test_HandleEscape_TestIgnoredCases_ExpectNoClose', () => {
   const page = _buildPage();
   const escapes = [];
   ItineraryCardModal.handleDocumentKeydown(_key('Escape'));

   ItineraryCardModal.syncOpenCard(page.mountEl, {
      onEscape: () => {
         escapes.push('escape');
      },
   });

   const prevented = _key('Escape');
   prevented.defaultPrevented = true;
   ItineraryCardModal.handleEscape(prevented);

   const picker = createDomNode('div', 'flatpickr-calendar');
   picker.classList.add('open');
   document.body.appendChild(picker);
   ItineraryCardModal.handleEscape(_key('Escape'));
   picker.classList.remove('open');

   const nested = createDomNode('div', 'tzg-popup');
   nested.appendChild(createDomNode('section', 'itin-card'));
   page.mountEl.appendChild(nested);
   ItineraryCardModal.handleEscape(_key('Escape'));
   nested.remove();

   ItineraryCardModal.onEscape = null;
   ItineraryCardModal.handleEscape(_key('Escape'));
   ItineraryCardModal.handleEscape(_key('Tab'));

   ItineraryCardModal.release();
   ItineraryCardModal.handleEscape(_key('Escape'));

   assert.deepEqual(escapes, []);
});


test('Test_GetTopCard_TestNestedPopup_ExpectTopmostCard', () => {
   const page = _buildPage();
   const popup = createDomNode('div', 'tzg-popup');
   const confirmCard = createDomNode('section', 'itin-card');
   popup.appendChild(confirmCard);
   page.mountEl.appendChild(popup);

   assert.equal(ItineraryCardModal.getTopCard(page.mountEl), confirmCard);
   assert.equal(ItineraryCardModal.getTopCard(null), null);
   assert.equal(ItineraryCardModal.getTitle(null), null);
});


test('Test_Release_TestOpenCard_ExpectFocusReturnedToBuildButton', () => {
   const page = _buildPage();
   page.buildButton.focus();
   ItineraryCardModal.syncOpenCard(page.mountEl, {
      returnFocusFallback: page.buildButton,
   });

   ItineraryCardModal.release();
   ItineraryCardModal.release();

   assert.equal(document.activeElement, page.buildButton);
   assert.equal(page.panel.hasAttribute('inert'), false);
   assert.equal(ItineraryCardModal.mountEl, null);
});


test('Test_GetGearButton_TestPresent_ExpectGear', () => {
   const gear = _focusable('button', 'itinerary-settings-gear');
   const originalGetElementById = document.getElementById;
   document.getElementById = (id) => {
      if (id === ItineraryCardModal.GEAR_BUTTON_ID) {
         return gear;
      }

      return originalGetElementById(id);
   };

   try {
      assert.equal(ItineraryCardModal.getGearButton(), gear);
   } finally {
      document.getElementById = originalGetElementById;
   }
});


test('Test_EnsureModal_TestSameDocument_ExpectReusedInstance', () => {
   const page = _buildPage();
   ItineraryCardModal.syncOpenCard(page.mountEl);
   const first = ItineraryCardModal.modal;

   const again = ItineraryCardModal.ensureModal();

   assert.equal(again, first);
});


test('Test_EnsureModal_TestNewDocument_ExpectInactiveModalReinstalled', () => {
   const page = _buildPage();
   ItineraryCardModal.syncOpenCard(page.mountEl);
   ItineraryCardModal.installedDocument = {};

   const modal = ItineraryCardModal.ensureModal();

   assert.equal(modal.isActive(), false);
   assert.equal(ItineraryCardModal.installedDocument, document);
});


test('Test_GetGearButton_TestMissing_ExpectNull', () => {
   assert.equal(ItineraryCardModal.getGearButton(), null);
});
