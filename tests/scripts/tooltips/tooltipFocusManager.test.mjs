import assert from 'node:assert/strict';
import test from 'node:test';

import { TooltipFocusManager } from '../../../scripts/tooltips/tooltipFocusManager.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _trackFocus(element) {
   element.focusCalls = [];
   element.focus = (options) => {
      element.focusCalls.push(options);
      document.activeElement = element;
   };
   return element;
}


function _createFocusable(tagName, className = '', { tabindex = '0' } = {}) {
   const element = _trackFocus(document.createElement(tagName));

   if (className) {
      element.className = className;
   }

   if (tabindex != null && tagName !== 'button') {
      element.setAttribute('tabindex', tabindex);
   }

   return element;
}


function _createTooltipTree() {
   const tooltipEl = _trackFocus(document.createElement('div'));
   const content = document.createElement('div');
   const firstCard = document.createElement('div');
   const secondCard = document.createElement('div');
   const firstLink = _createFocusable('span', 'species-link');
   const hiddenLink = _createFocusable('span', 'species-link');
   const prevArrow = _createFocusable('div', 'tooltip-arrow');
   const closeButton = _createFocusable('button', 'tooltip-close');

   secondCard.style.display = 'none';
   firstCard.appendChild(firstLink);
   secondCard.appendChild(hiddenLink);
   content.appendChild(firstCard);
   content.appendChild(secondCard);
   tooltipEl.appendChild(content);
   tooltipEl.appendChild(prevArrow);
   tooltipEl.appendChild(closeButton);

   return {
      tooltipEl,
      firstCard,
      secondCard,
      firstLink,
      hiddenLink,
      prevArrow,
      closeButton,
   };
}


function _createManager(tooltipEl, overrides = {}) {
   const opener = _createFocusable('div', 'marker');

   const manager = TooltipFocusManager.createTooltipFocusManager({
      tooltipEl,
      getOpener: () => opener,
      isOpen: () => true,
      onFocusLeave: () => {},
      ...overrides,
   });

   return { manager, opener };
}


function _tabEvent({ shiftKey = false } = {}) {
   return {
      key: 'Tab',
      shiftKey,
      defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; },
   };
}


function _createBannerManager(tooltipEl, overrides = {}) {
   const bannerCloseButton = _createFocusable('button', 'off-display-closed-close');
   const { manager, opener } = _createManager(tooltipEl, {
      getBannerFocusables: () => [bannerCloseButton],
      ...overrides,
   });

   return { manager, opener, bannerCloseButton };
}


test('Test_CollectFocusableElements_TestHiddenCard_ExpectVisibleControlsInOrder', () => {
   const tree = _createTooltipTree();

   const focusable = TooltipFocusManager.collectFocusableElements(tree.tooltipEl);

   assert.deepEqual(focusable, [tree.firstLink, tree.prevArrow, tree.closeButton]);
});


test('Test_IsFocusableElement_TestNegativeTabindex_ExpectFalse', () => {
   const element = _createFocusable('span', '', { tabindex: '-1' });

   assert.equal(TooltipFocusManager.isFocusableElement(element), false);
});


test('Test_IsFocusableElement_TestInputWithoutTabindex_ExpectTrue', () => {
   const input = _createFocusable('input', 'itin-date-input', { tabindex: null });
   const excluded = _createFocusable('input', 'hidden-input', { tabindex: '-1' });

   assert.equal(TooltipFocusManager.isFocusableElement(input), true);
   assert.equal(TooltipFocusManager.isFocusableElement(excluded), false);
});


test('Test_IsFocusableElement_TestAnchorWithHref_ExpectTrue', () => {
   const element = _createFocusable('a', 'tooltip-link', { tabindex: null });
   element.setAttribute('href', 'https://example.test');

   assert.equal(TooltipFocusManager.isFocusableElement(element), true);
});


test('Test_CreateTooltipFocusManager_TestInstall_ExpectNonModalDialog', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);

   manager.install();
   manager.install();

   assert.equal(tree.tooltipEl.getAttribute('role'), 'dialog');
   assert.equal(tree.tooltipEl.getAttribute('tabindex'), '-1');
   assert.equal(tree.tooltipEl.getAttribute('aria-modal'), null);
   assert.ok(tree.tooltipEl.listeners.keydown);
   assert.ok(tree.tooltipEl.listeners.focusout);
});


test('Test_CreateTooltipFocusManager_TestFocusInitial_ExpectFirstCardLink', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);

   manager.focusInitial();

   assert.equal(document.activeElement, tree.firstLink);
   assert.deepEqual(tree.firstLink.focusCalls, [{ preventScroll: true }]);
});


test('Test_CreateTooltipFocusManager_TestFocusInitialWithoutLinks_ExpectTooltip', () => {
   const tooltipEl = _trackFocus(document.createElement('div'));
   const { manager } = _createManager(tooltipEl);

   manager.focusInitial();

   assert.equal(document.activeElement, tooltipEl);
});


test('Test_CreateTooltipFocusManager_TestFocusInitialOnlyControls_ExpectFirstControl', () => {
   const tooltipEl = _trackFocus(document.createElement('div'));
   const closeButton = _createFocusable('button', 'tooltip-close');
   tooltipEl.appendChild(closeButton);
   const { manager } = _createManager(tooltipEl);

   manager.focusInitial();

   assert.equal(document.activeElement, closeButton);
});


test('Test_CreateTooltipFocusManager_TestRecoverFocusFromHiddenCard_ExpectVisibleLink', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   document.activeElement = tree.hiddenLink;

   manager.recoverFocus();

   assert.equal(document.activeElement, tree.firstLink);
});


test('Test_CreateTooltipFocusManager_TestRecoverFocusOnVisibleControl_ExpectUnchanged', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   document.activeElement = tree.prevArrow;

   manager.recoverFocus();

   assert.equal(document.activeElement, tree.prevArrow);
   assert.deepEqual(tree.firstLink.focusCalls, []);
});


test('Test_CreateTooltipFocusManager_TestRecoverFocusOutside_ExpectUnchanged', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   const outside = _createFocusable('button');
   document.activeElement = outside;

   manager.recoverFocus();

   assert.equal(document.activeElement, outside);
});


test('Test_CreateTooltipFocusManager_TestContainsFocus_ExpectTooltipDescendantsOnly', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createManager(tree.tooltipEl);

   document.activeElement = tree.firstLink;
   assert.equal(manager.containsFocus(), true);

   document.activeElement = opener;
   assert.equal(manager.containsFocus(), false);
});


test('Test_CreateTooltipFocusManager_TestShiftTabOnFirst_ExpectOpenerFocused', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;
   const event = _tabEvent({ shiftKey: true });

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, opener);
});


test('Test_CreateTooltipFocusManager_TestTabOnLast_ExpectOpenerThenNativeTab', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createManager(tree.tooltipEl);
   document.activeElement = tree.closeButton;
   const event = _tabEvent();

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, opener);
});


test('Test_CreateTooltipFocusManager_TestTabInMiddle_ExpectNativeTab', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;
   const event = _tabEvent();

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, tree.firstLink);
});


test('Test_CreateTooltipFocusManager_TestRestoreFocus_ExpectOpenerFocused', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;

   manager.restoreFocusToOpener();

   assert.equal(document.activeElement, opener);
   assert.deepEqual(opener.focusCalls, [{ preventScroll: true }]);
});


test('Test_CreateTooltipFocusManager_TestRestoreFocusAfterPointerOpen_ExpectOpenerFocusedWithoutRing', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createManager(tree.tooltipEl);
   manager.focusInitial({ pointer: true });

   manager.restoreFocusToOpener();

   assert.equal(document.activeElement, opener);
   assert.deepEqual(opener.focusCalls, [{ preventScroll: true, focusVisible: false }]);
});


test('Test_CreateTooltipFocusManager_TestFocusMovesElsewhere_ExpectFocusLeave', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   const { manager } = _createManager(tree.tooltipEl, { onFocusLeave: () => { leaves += 1; } });
   const outside = _createFocusable('button');

   document.activeElement = outside;
   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 1);
});


test('Test_CreateTooltipFocusManager_TestFocusMovesToOpenerOrInside_ExpectStaysOpen', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   const { manager, opener } = _createManager(tree.tooltipEl, { onFocusLeave: () => { leaves += 1; } });

   document.activeElement = opener;
   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));
   document.activeElement = tree.closeButton;
   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));
   document.activeElement = document.body;
   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 0);
});


test('Test_IsFocusableElement_TestDisabledOrMissing_ExpectFalse', () => {
   const button = _createFocusable('button');
   button.disabled = true;

   assert.equal(TooltipFocusManager.isFocusableElement(button), false);
   assert.equal(TooltipFocusManager.isFocusableElement(null), false);
});


test('Test_CreateTooltipFocusManager_TestNonTabOrModifiedKey_ExpectIgnored', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;
   const enterEvent = { ..._tabEvent({ shiftKey: true }), key: 'Enter' };
   const ctrlTabEvent = { ..._tabEvent({ shiftKey: true }), ctrlKey: true };

   manager.handleTab(enterEvent);
   manager.handleTab(ctrlTabEvent);

   assert.equal(enterEvent.defaultPrevented, false);
   assert.equal(ctrlTabEvent.defaultPrevented, false);
   assert.equal(document.activeElement, tree.firstLink);
});


test('Test_CreateTooltipFocusManager_TestTabWithoutOpener_ExpectIgnored', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl, { getOpener: () => null });
   document.activeElement = tree.firstLink;
   const event = _tabEvent({ shiftKey: true });

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, false);
});


test('Test_CreateTooltipFocusManager_TestFocusOutWhenClosedOrWindowBlurred_ExpectNoFocusLeave', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   let open = false;
   const { manager } = _createManager(tree.tooltipEl, {
      isOpen: () => open,
      onFocusLeave: () => { leaves += 1; },
   });
   document.activeElement = _createFocusable('button');

   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));
   open = true;
   document.hasFocus = () => false;
   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 0);
});


test('Test_CreateTooltipFocusManager_TestPointerFocusInitial_ExpectNoFocusRing', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);

   manager.focusInitial({ pointer: true });

   assert.equal(document.activeElement, tree.firstLink);
   assert.deepEqual(tree.firstLink.focusCalls, [{ preventScroll: true, focusVisible: false }]);
   assert.equal(tree.tooltipEl.hasAttribute(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE), true);
});


test('Test_CreateTooltipFocusManager_TestKeyboardFocusAfterPointer_ExpectRingRestored', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);

   manager.focusInitial({ pointer: true });
   manager.focusInitial();

   assert.equal(tree.tooltipEl.hasAttribute(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE), false);
   assert.deepEqual(tree.firstLink.focusCalls[1], { preventScroll: true });
});


test('Test_CreateTooltipFocusManager_TestKeydownInTooltip_ExpectPointerModeCleared', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   manager.install();
   manager.focusInitial({ pointer: true });

   tree.tooltipEl.dispatchEvent({ type: 'keydown', key: 'ArrowRight' });

   assert.equal(tree.tooltipEl.hasAttribute(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE), false);
});


test('Test_CreateTooltipFocusManager_TestClearPointerOpened_ExpectAttributeRemoved', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   manager.focusInitial({ pointer: true });

   manager.clearPointerOpened();

   assert.equal(tree.tooltipEl.hasAttribute(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE), false);
});


test('Test_CreateTooltipFocusManager_TestShiftTabOnFirstWithBanner_ExpectOpenerFocused', () => {
   const tree = _createTooltipTree();
   const { manager, opener } = _createBannerManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;
   const event = _tabEvent({ shiftKey: true });

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, opener);
});


test('Test_CreateTooltipFocusManager_TestTabOnLastWithBanner_ExpectBannerFocused', () => {
   const tree = _createTooltipTree();
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl);
   document.activeElement = tree.closeButton;
   const event = _tabEvent();

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, bannerCloseButton);
});


test('Test_CreateTooltipFocusManager_TestTabInMiddleWithBanner_ExpectNativeTab', () => {
   const tree = _createTooltipTree();
   const { manager } = _createBannerManager(tree.tooltipEl);
   document.activeElement = tree.firstLink;
   const event = _tabEvent();

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, tree.firstLink);
});
test('Test_CreateTooltipFocusManager_TestTabOnBanner_ExpectOpenerThenNativeTab', () => {
   const tree = _createTooltipTree();
   const { manager, opener, bannerCloseButton } = _createBannerManager(tree.tooltipEl);
   document.activeElement = bannerCloseButton;
   const event = _tabEvent();

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, opener);
});
test('Test_CreateTooltipFocusManager_TestShiftTabOnBannerWithEmptyTooltip_ExpectTooltipFocused', () => {
   const tooltipEl = _trackFocus(document.createElement('div'));
   const { manager, bannerCloseButton } = _createBannerManager(tooltipEl);
   document.activeElement = bannerCloseButton;

   manager.handleTab(_tabEvent({ shiftKey: true }));

   assert.equal(document.activeElement, tooltipEl);
});
test('Test_CreateTooltipFocusManager_TestShiftTabOnBanner_ExpectLastTooltipControlFocused', () => {
   const tree = _createTooltipTree();
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl);
   document.activeElement = bannerCloseButton;
   const event = _tabEvent({ shiftKey: true });

   manager.handleTab(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, tree.closeButton);
});
test('Test_CreateTooltipFocusManager_TestBannerFocused_ExpectCountedAsInsideTooltip', () => {
   const tree = _createTooltipTree();
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl);
   document.activeElement = bannerCloseButton;

   manager.recoverFocus();

   assert.equal(manager.containsFocus(), true);
   assert.equal(document.activeElement, bannerCloseButton);
   assert.deepEqual(tree.firstLink.focusCalls, []);
});


test('Test_CreateTooltipFocusManager_TestFocusMovesToBanner_ExpectNoFocusLeave', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl, {
      onFocusLeave: () => { leaves += 1; },
   });
   document.activeElement = bannerCloseButton;

   manager.handleFocusOut();
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 0);
});


test('Test_CreateTooltipFocusManager_TestKeydownOnBanner_ExpectTabHandledAndPointerModeCleared', () => {
   const tree = _createTooltipTree();
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl);
   const documentListeners = {};
   document.addEventListener = (name, handler) => { documentListeners[name] = handler; };
   manager.install();
   manager.focusInitial({ pointer: true });
   document.activeElement = bannerCloseButton;
   const event = { ..._tabEvent({ shiftKey: true }), target: bannerCloseButton };

   documentListeners.keydown(event);

   assert.equal(event.defaultPrevented, true);
   assert.equal(document.activeElement, tree.closeButton);
   assert.equal(tree.tooltipEl.hasAttribute(TooltipFocusManager.POINTER_OPENED_ATTRIBUTE), false);
});


test('Test_CreateTooltipFocusManager_TestKeydownElsewhere_ExpectIgnored', () => {
   const tree = _createTooltipTree();
   const { manager } = _createBannerManager(tree.tooltipEl);
   const documentListeners = {};
   document.addEventListener = (name, handler) => { documentListeners[name] = handler; };
   manager.install();
   document.activeElement = tree.firstLink;
   const event = { ..._tabEvent(), target: tree.firstLink };

   documentListeners.keydown(event);

   assert.equal(event.defaultPrevented, false);
   assert.equal(document.activeElement, tree.firstLink);
});


test('Test_CreateTooltipFocusManager_TestTooltipWithoutContains_ExpectNoFocusInside', () => {
   const { manager } = _createManager({});
   document.activeElement = _createFocusable('button');

   assert.equal(manager.containsFocus(), false);
});


test('Test_CreateTooltipFocusManager_TestRecoverFocusOnTooltipItself_ExpectUnchanged', () => {
   const tree = _createTooltipTree();
   const { manager } = _createManager(tree.tooltipEl);
   document.activeElement = tree.tooltipEl;

   manager.recoverFocus();

   assert.equal(document.activeElement, tree.tooltipEl);
   assert.deepEqual(tree.firstLink.focusCalls, []);
});


test('Test_CreateTooltipFocusManager_TestFocusLeavesBanner_ExpectFocusLeave', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   const { manager, bannerCloseButton } = _createBannerManager(tree.tooltipEl, {
      onFocusLeave: () => { leaves += 1; },
   });
   const documentListeners = {};
   document.addEventListener = (name, handler) => { documentListeners[name] = handler; };
   manager.install();
   document.activeElement = _createFocusable('button');

   documentListeners.focusout({ target: bannerCloseButton });
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 1);
});


test('Test_CreateTooltipFocusManager_TestFocusOutElsewhere_ExpectIgnored', async () => {
   const tree = _createTooltipTree();
   let leaves = 0;
   const { manager } = _createBannerManager(tree.tooltipEl, {
      onFocusLeave: () => { leaves += 1; },
   });
   const documentListeners = {};
   document.addEventListener = (name, handler) => { documentListeners[name] = handler; };
   manager.install();
   document.activeElement = _createFocusable('button');

   documentListeners.focusout({ target: tree.firstLink });
   await new Promise((resolve) => setTimeout(resolve, 5));

   assert.equal(leaves, 0);
});
