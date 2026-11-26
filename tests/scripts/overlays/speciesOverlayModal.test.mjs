import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesOverlayModal } from '../../../scripts/overlays/speciesOverlayModal.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


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


function _buildPage() {
   const app = createDomNode('div', 'app');
   const main = createDomNode('main');
   const opener = _focusable('span', 'species-link');
   const pin = _focusable('div', 'marker');
   const nav = createDomNode('nav');
   const alreadyInert = createDomNode('div', 'already-inert');
   const script = createDomNode('script');
   const overlay = createDomNode('div', 'species-overlay');
   const card = _focusable('div', 'species-overlay-card');
   card.removeAttribute('tabindex');
   const closeButton = _focusable('button', 'species-close');
   const content = createDomNode('div', 'species-overlay-content');
   const navNext = _focusable('button', 'species-overlay-nav-next');
   const scroll = _focusable('div', 'species-overlay-scroll');
   scroll.removeAttribute('tabindex');
   const title = _focusable('h2', 'animal-species-name');
   title.removeAttribute('tabindex');
   title.textContent = 'African Lion';

   alreadyInert.setAttribute('inert', '');
   main.appendChild(pin);
   main.appendChild(opener);
   app.appendChild(main);
   app.appendChild(alreadyInert);
   app.appendChild(script);
   app.appendChild(overlay);
   app.appendChild(nav);
   overlay.appendChild(card);
   card.appendChild(closeButton);
   card.appendChild(content);
   content.appendChild(navNext);
   content.appendChild(scroll);

   scroll.appendChild(title);

   const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
      getOverlay: () => overlay,
      getDialog: () => card,
   });

   return { app, main, nav, alreadyInert, script, overlay, card, closeButton, navNext, scroll, title, opener, pin, modal };
}


function _key(key, extra = {}) {
   return {
      key,
      defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
      ...extra,
   };
}


test('Test_CreateSpeciesOverlayModal_TestActivate_ExpectModalDialogNamedBySpecies', () => {
   const page = _buildPage();
   page.opener.focus();

   page.modal.activate();

   assert.equal(page.card.getAttribute('role'), 'dialog');
   assert.equal(page.card.getAttribute('aria-modal'), 'true');
   assert.equal(page.card.getAttribute('aria-labelledby'), SpeciesOverlayModal.TITLE_ID);
   assert.equal(page.title.id, SpeciesOverlayModal.TITLE_ID);
   assert.equal(page.scroll.getAttribute('tabindex'), '0');
   assert.equal(page.scroll.getAttribute('role'), 'region');
   assert.equal(page.modal.isActive(), true);
});


test('Test_CreateSpeciesOverlayModal_TestKeyboardActivate_ExpectTitleFocusedWithRing', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.handleKeydown(_key('Enter'));

   page.modal.activate();

   assert.equal(document.activeElement, page.title);
   assert.equal(page.title.getAttribute('tabindex'), '-1');
   assert.deepEqual(page.title.focusCalls, [{ preventScroll: true }]);
   assert.equal(page.card.hasAttribute(SpeciesOverlayModal.POINTER_OPENED_ATTRIBUTE), false);
});


test('Test_CreateSpeciesOverlayModal_TestPointerActivate_ExpectFocusWithoutRing', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.handlePointerDown();

   page.modal.activate();

   assert.deepEqual(page.title.focusCalls, [{ preventScroll: true, focusVisible: false }]);
   assert.equal(page.card.hasAttribute(SpeciesOverlayModal.POINTER_OPENED_ATTRIBUTE), true);

   page.modal.handleKeydown(_key('ArrowDown'));
   assert.equal(page.card.hasAttribute(SpeciesOverlayModal.POINTER_OPENED_ATTRIBUTE), false);
});


test('Test_CreateSpeciesOverlayModal_TestActivate_ExpectBackgroundInertAndRestored', () => {
   const page = _buildPage();
   page.opener.focus();

   page.modal.activate();

   assert.equal(page.main.hasAttribute('inert'), true);
   assert.equal(page.nav.hasAttribute('inert'), true);
   assert.equal(page.script.hasAttribute('inert'), false);
   assert.equal(page.overlay.hasAttribute('inert'), false);

   page.modal.deactivate();

   assert.equal(page.main.hasAttribute('inert'), false);
   assert.equal(page.nav.hasAttribute('inert'), false);
   assert.equal(page.alreadyInert.hasAttribute('inert'), true);
});


test('Test_CreateSpeciesOverlayModal_TestDeactivate_ExpectFocusReturnedToOpener', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();

   page.modal.deactivate();
   page.modal.deactivate();

   assert.equal(document.activeElement, page.opener);
   assert.equal(page.modal.isActive(), false);
});


test('Test_CreateSpeciesOverlayModal_TestOpenerGone_ExpectFocusReturnedToFallback', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate({ returnFocusFallback: page.pin });
   page.opener.isConnected = false;

   page.modal.deactivate();

   assert.equal(document.activeElement, page.pin);
});


test('Test_CreateSpeciesOverlayModal_TestOpenerInsideInert_ExpectFallbackUsed', () => {
   const page = _buildPage();
   const inertWrapper = createDomNode('div');
   const hiddenOpener = _focusable('span');
   inertWrapper.setAttribute('inert', '');
   inertWrapper.appendChild(hiddenOpener);
   hiddenOpener.focus();
   page.modal.activate({ returnFocusFallback: page.pin });

   page.modal.deactivate();

   assert.equal(document.activeElement, page.pin);
});


test('Test_CreateSpeciesOverlayModal_TestFocusMovedOutsideBeforeClose_ExpectUnchanged', () => {
   const page = _buildPage();
   const elsewhere = _focusable('button');
   page.opener.focus();
   page.modal.activate();
   elsewhere.focus();

   page.modal.deactivate();

   assert.equal(document.activeElement, elsewhere);
});


test('Test_CreateSpeciesOverlayModal_TestNoOpenerOrFallback_ExpectNoFocusCall', () => {
   const page = _buildPage();
   document.activeElement = document.body;
   page.modal.activate();

   page.modal.deactivate();

   assert.equal(page.opener.focusCalls.length, 0);
});


test('Test_CreateSpeciesOverlayModal_TestTabFromTitle_ExpectFirstControl', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();
   const event = _key('Tab');

   page.modal.handleKeydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, page.closeButton);
});


test('Test_CreateSpeciesOverlayModal_TestTabFromLast_ExpectFirstControl', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();
   page.scroll.focus();
   const event = _key('Tab');

   page.modal.handleKeydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, page.closeButton);
});


test('Test_CreateSpeciesOverlayModal_TestShiftTabFromFirst_ExpectLastControl', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();
   page.closeButton.focus();
   const event = _key('Tab', { shiftKey: true });

   page.modal.handleKeydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, page.scroll);
});


test('Test_CreateSpeciesOverlayModal_TestTabInMiddle_ExpectBrowserDefault', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();
   page.navNext.focus();
   const tabEvent = _key('Tab');
   const shiftTabEvent = _key('Tab', { shiftKey: true });

   page.modal.handleKeydown(tabEvent);
   page.modal.handleKeydown(shiftTabEvent);

   assert.equal(tabEvent.defaultPrevented, false);
   assert.equal(shiftTabEvent.defaultPrevented, false);
   assert.equal(document.activeElement, page.navNext);
});


test('Test_CreateSpeciesOverlayModal_TestShiftTabFromTitle_ExpectLastControl', () => {
   const page = _buildPage();
   page.opener.focus();
   page.modal.activate();

   page.modal.handleKeydown(_key('Tab', { shiftKey: true }));

   assert.equal(document.activeElement, page.scroll);
});


test('Test_CreateSpeciesOverlayModal_TestTabWithoutControls_ExpectInitialTarget', () => {
   const card = _focusable('div', 'species-overlay-card');
   card.removeAttribute('tabindex');
   const overlay = createDomNode('div');
   overlay.appendChild(card);
   const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
      getOverlay: () => overlay,
      getDialog: () => card,
   });
   modal.activate();
   const event = _key('Tab');

   modal.handleKeydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, card);
   assert.equal(card.getAttribute('aria-labelledby'), null);
});


test('Test_CreateSpeciesOverlayModal_TestInactiveOrModifiedKeys_ExpectIgnored', () => {
   const page = _buildPage();
   const inactive = _key('Tab');
   page.modal.handleKeydown(inactive);
   page.opener.focus();
   page.modal.activate();
   const ctrlTab = _key('Tab', { ctrlKey: true });
   page.modal.handleKeydown(ctrlTab);

   assert.equal(inactive.defaultPrevented, false);
   assert.equal(ctrlTab.defaultPrevented, false);
   assert.equal(document.activeElement, page.title);
});


test('Test_CreateSpeciesOverlayModal_TestFocusInOutside_ExpectPulledBack', () => {
   const page = _buildPage();
   page.modal.handleFocusIn({ target: page.pin });
   page.opener.focus();
   page.modal.activate();
   page.pin.focus();

   page.modal.handleFocusIn({ target: page.pin });
   assert.equal(document.activeElement, page.title);

   page.closeButton.focus();
   page.modal.handleFocusIn({ target: page.closeButton });
   assert.equal(document.activeElement, page.closeButton);
});


test('Test_CreateSpeciesOverlayModal_TestFocusIfLost_ExpectPreferredElement', () => {
   const page = _buildPage();
   page.modal.focusIfLost(page.navNext);
   assert.equal(page.navNext.focusCalls.length, 0);

   page.opener.focus();
   page.modal.activate();
   document.activeElement = document.body;
   page.modal.focusIfLost(page.navNext);
   assert.equal(document.activeElement, page.navNext);

   page.modal.activate();
   assert.equal(document.activeElement, page.navNext);
});


test('Test_CreateSpeciesOverlayModal_TestInstall_ExpectCaptureListeners', () => {
   const registered = [];
   document.addEventListener = (type, handler, capture) => registered.push([type, capture]);
   const page = _buildPage();

   page.modal.install();

   assert.deepEqual(registered, [['pointerdown', true], ['focusin', true]]);
});


test('Test_CreateSpeciesOverlayModal_TestTitleWithoutScroll_ExpectNamedDialog', () => {
   const overlay = createDomNode('div');
   const card = createDomNode('div', 'species-overlay-card');
   const title = _focusable('h2', 'animal-species-name');
   title.removeAttribute('tabindex');
   title.textContent = 'African Lion';
   overlay.appendChild(card);
   card.appendChild(title);
   const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
      getOverlay: () => overlay,
      getDialog: () => card,
   });

   modal.activate();

   assert.equal(card.getAttribute('aria-labelledby'), title.id);
   assert.equal(document.activeElement, title);
   assert.equal(card.querySelector('.species-overlay-scroll'), null);
});


test('Test_CreateSpeciesOverlayModal_TestNoTitleWithControl_ExpectFirstControlFocused', () => {
   const overlay = createDomNode('div');
   const card = createDomNode('div', 'species-overlay-card');
   const closeButton = _focusable('button', 'species-close');
   overlay.appendChild(card);
   card.appendChild(closeButton);
   const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
      getOverlay: () => overlay,
      getDialog: () => card,
   });

   modal.activate();

   assert.equal(card.getAttribute('aria-labelledby'), null);
   assert.equal(document.activeElement, closeButton);
});


test('Test_CreateSpeciesOverlayModal_TestMissingDialog_ExpectNoThrow', () => {
   const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
      getOverlay: () => null,
      getDialog: () => null,
   });

   modal.activate();
   modal.handleFocusIn({ target: null });
   modal.deactivate();

   assert.equal(modal.isActive(), false);
});
