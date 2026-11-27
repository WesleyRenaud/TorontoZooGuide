import assert from 'node:assert/strict';
import test from 'node:test';

import { OverlayModal } from '../../../scripts/overlays/overlayModal.js';
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


function _key(key, extra = {}) {
   return {
      key,
      defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
      ...extra,
   };
}


function _buildDialog({ titleText = 'Set Visit Date', titleId = 'overlayTitle' } = {}) {
   const page = createDomNode('div', 'page');
   const sidebar = createDomNode('aside', 'sidebar');
   const mountEl = createDomNode('div', 'itinerary-flow');
   const overlay = createDomNode('div', 'itin-overlay');
   const card = createDomNode('section', 'itin-card');
   const title = _focusable('h2', 'itin-h1');
   const closeButton = _focusable('button', 'itin-close');
   const nextButton = _focusable('button', 'itin-next');

   title.removeAttribute('tabindex');
   title.textContent = titleText;
   card.append(title, closeButton, nextButton);
   overlay.appendChild(card);
   mountEl.appendChild(overlay);
   page.append(sidebar, mountEl);

   const modal = OverlayModal.createOverlayModal({
      getOverlay: () => mountEl,
      getDialog: () => card,
      getTitle: (dialog) => dialog.querySelector('.itin-h1'),
      titleId,
   });

   return { page, sidebar, mountEl, overlay, card, title, closeButton, nextButton, modal };
}


test('Test_CreateOverlayModal_TestActivate_ExpectHeadingLabelsDialog', () => {
   const page = _buildDialog();

   page.modal.activate();

   assert.equal(page.card.getAttribute('role'), 'dialog');
   assert.equal(page.card.getAttribute('aria-modal'), 'true');
   assert.equal(page.card.getAttribute('aria-labelledby'), 'overlayTitle');
   assert.equal(page.title.id, 'overlayTitle');
   assert.equal(page.title.getAttribute('tabindex'), '-1');
   assert.equal(document.activeElement, page.title);
   assert.equal(page.sidebar.hasAttribute('inert'), true);
});


test('Test_CreateOverlayModal_TestDefaultTitle_ExpectFirstControlFocused', () => {
   const card = createDomNode('section', 'itin-card');
   const closeButton = _focusable('button', 'itin-close');
   const overlay = createDomNode('div', 'itin-overlay');
   card.appendChild(closeButton);
   overlay.appendChild(card);

   const modal = OverlayModal.createOverlayModal({
      getOverlay: () => overlay,
      getDialog: () => card,
   });

   modal.activate();

   assert.equal(document.activeElement, closeButton);
   assert.equal(card.getAttribute('aria-labelledby'), null);
   assert.equal(OverlayModal.getDefaultTitle(), null);
});


test('Test_CreateOverlayModal_TestTitleWithoutId_ExpectTabbableHeadingUnlabelled', () => {
   const page = _buildDialog({ titleId: null });

   page.modal.activate();

   assert.equal(page.title.getAttribute('tabindex'), '-1');
   assert.equal(page.card.getAttribute('aria-labelledby'), null);
   assert.ok(!page.title.id);
});


test('Test_CreateOverlayModal_TestRefresh_ExpectFocusMovesToNewHeading', () => {
   const page = _buildDialog();
   page.modal.activate();
   const nextTitle = _focusable('h2', 'itin-h1');
   nextTitle.removeAttribute('tabindex');
   nextTitle.textContent = 'Select Regions';
   page.card.replaceChildren(nextTitle, page.closeButton, page.nextButton);

   page.modal.refresh();

   assert.equal(document.activeElement, nextTitle);
   assert.equal(nextTitle.id, 'overlayTitle');
   assert.equal(page.card.getAttribute('aria-labelledby'), 'overlayTitle');
});


test('Test_CreateOverlayModal_TestRefreshWhileInactive_ExpectNoFocusChange', () => {
   const page = _buildDialog();

   page.modal.refresh();

   assert.equal(page.modal.isActive(), false);
   assert.equal(page.title.focusCalls.length, 0);
});


test('Test_CreateOverlayModal_TestDecorateNothing_ExpectNoThrow', () => {
   const dialog = createDomNode('section', 'itin-card');

   assert.doesNotThrow(() => {
      OverlayModal.decorateNothing(dialog, null);
   });
});


test('Test_CreateOverlayModal_TestDatePicker_ExpectUsableOutsideCard', () => {
   const page = _buildDialog();
   const calendar = _focusable('div', 'flatpickr-calendar');
   calendar.classList.add('open');
   page.page.appendChild(calendar);

   page.modal.activate();
   calendar.focus();
   page.modal.handleFocusIn({ target: calendar });
   const tabEvent = _key('Tab');
   page.modal.handleKeydown(tabEvent);

   assert.equal(calendar.hasAttribute('inert'), false);
   assert.equal(document.activeElement, calendar);
   assert.equal(tabEvent.defaultPrevented, false);
});


test('Test_CreateOverlayModal_TestTabAfterFocusLoss_ExpectNextControl', async () => {
   const page = _buildDialog();
   page.modal.activate();
   page.closeButton.focus();
   const event = _key('Tab');

   page.modal.handleKeydown(event);
   document.activeElement = document.body;
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, page.nextButton);
});


test('Test_CreateOverlayModal_TestTabRepairWithoutTimeout_ExpectStaysOnControl', () => {
   const page = _buildDialog();
   page.modal.activate();
   page.closeButton.focus();
   const originalSetTimeout = globalThis.setTimeout;
   globalThis.setTimeout = undefined;

   try {
      page.modal.handleKeydown(_key('Tab'));
      assert.equal(document.activeElement, page.closeButton);
   } finally {
      globalThis.setTimeout = originalSetTimeout;
   }
});


test('Test_CreateOverlayModal_TestShiftTabAfterFocusLoss_ExpectPreviousControl', async () => {
   const page = _buildDialog();
   page.modal.activate();
   page.nextButton.focus();
   const event = _key('Tab', { shiftKey: true });

   page.modal.handleKeydown(event);
   document.activeElement = document.body;
   await new Promise((resolve) => setTimeout(resolve, 0));

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, page.closeButton);
});


test('Test_CreateOverlayModal_TestTabAfterFocusLoss_ExpectHeadingWhenControlsRemoved', async () => {
   const page = _buildDialog();
   page.modal.activate();
   page.closeButton.focus();
   page.modal.handleKeydown(_key('Tab'));
   page.closeButton.remove();
   page.nextButton.remove();
   document.activeElement = document.body;
   await new Promise((resolve) => setTimeout(resolve, 0));

   assert.equal(document.activeElement, page.title);
});
