import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelFragment } from '../../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { ItineraryPanelPopupBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelPopupBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks({
   before: () => {
      globalThis.requestAnimationFrame = (callback) => callback();
   },
   after: () => {
      delete globalThis.requestAnimationFrame;
   },
});

test('Test_GetItineraryOverlayMountEl_TestFlowThenMap_ExpectFallback', () => {
   const flow = document.getElementById('itineraryFlow');
   assert.equal(ItineraryPanelFragment.getItineraryOverlayMountEl(), flow);

   const originalGet = document.getElementById;
   document.getElementById = () => null;
   const map = document.createElement('div');
   map.className = 'map-container';
   const originalQuery = document.querySelector;
   document.querySelector = (selector) => (
      selector === '.map-container' ? map : originalQuery(selector)
   );

   try {
      assert.equal(ItineraryPanelFragment.getItineraryOverlayMountEl(), map);
   } finally {
      document.getElementById = originalGet;
      document.querySelector = originalQuery;
   }
});

test('Test_GetItineraryPanelMountEl_TestPanel_ExpectElement', () => {
   const panel = document.querySelector('.itinerary-panel');
   assert.equal(ItineraryPanelFragment.getItineraryPanelMountEl(), panel);
});

test('Test_CreateItineraryPopupLayout_TestMessageAndActions_ExpectStructure', () => {
   const layout = ItineraryPanelFragment.createItineraryPopupLayout({
      popupClassName: 'tzg-confirm',
      title: 'Heads up',
      message: 'Save changes?',
      actionButtons: [
         { key: 'cancel', label: 'Cancel' },
         { key: 'confirm', label: 'Save', className: 'tzg-popup-confirm' },
      ],
   });

   assert.ok(layout.root.classList.contains('tzg-popup'));
   assert.ok(layout.root.classList.contains('tzg-confirm'));
   assert.equal(layout.root.querySelector('.itin-top-title')?.textContent, 'Heads up');
   assert.equal(layout.root.querySelector('.tzg-popup-message')?.textContent, 'Save changes?');
   assert.equal(layout.closeButton, null);
   assert.ok(layout.buttonEls.cancel);
   assert.ok(layout.buttonEls.confirm);
});

test('Test_CreateItineraryPopupLayout_TestBodyContentAndClose_ExpectCloseButton', () => {
   const bodyContent = document.createElement('div');
   bodyContent.className = 'custom-body';
   bodyContent.textContent = 'Custom';

   const layout = ItineraryPanelFragment.createItineraryPopupLayout({
      title: 'Dialog',
      bodyContent,
      showCloseButton: true,
      closeAriaLabel: Strings.itinerary.aria.closeBuilder,
      actionButtons: [],
   });

   assert.ok(layout.closeButton);
   assert.equal(layout.closeButton.getAttribute('aria-label'), Strings.itinerary.aria.closeBuilder);
   assert.ok(layout.root.querySelector('.custom-body'));
   assert.equal(layout.root.querySelector('.tzg-popup-message'), null);
});

test('Test_MountDismissablePopup_TestMissingArgs_ExpectNoOpClosers', () => {
   const result = ItineraryPanelFragment.mountDismissablePopup({});
   result.close();
   result.dismiss();
});

test('Test_MountDismissablePopup_TestOverlayEscapeAndClose_ExpectDismiss', () => {
   const dismissals = [];
   const focusEl = document.createElement('button');
   const focusCalls = [];
   focusEl.focus = () => {
      focusCalls.push(true);
   };

   const root = document.createElement('div');
   const overlay = document.createElement('div');
   overlay.className = 'itin-overlay';
   root.appendChild(overlay);

   const { close, dismiss } = ItineraryPanelFragment.mountDismissablePopup({
      mountEl: document.body,
      root,
      overlay,
      initialFocusEl: focusEl,
      onDismiss: () => {
         dismissals.push(true);
      },
   });

   assert.equal(document.body.children.includes?.(root) || document.body.contains?.(root), true);
   assert.deepEqual(focusCalls, [true]);

   overlay.listeners.click({ target: overlay });
   assert.deepEqual(dismissals, [true]);
   assert.equal(Boolean(root.parentElement), false);

   const root2 = document.createElement('div');
   const overlay2 = document.createElement('div');
   const keydowns = [];
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;
   let keyHandler = null;

   document.addEventListener = (type, handler) => {
      if (type === 'keydown') {
         keyHandler = handler;
      }
      keydowns.push(type);
   };
   document.removeEventListener = () => {};

   try {
      const mounted = ItineraryPanelFragment.mountDismissablePopup({
         mountEl: document.body,
         root: root2,
         overlay: overlay2,
         onDismiss: () => {
            dismissals.push('escape');
         },
      });

      keyHandler?.({ key: 'Escape', preventDefault() {} });
      assert.ok(dismissals.includes('escape'));

      mounted.close();
      close();
      dismiss();
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
   }
});

test('Test_MountDismissablePopup_TestDismissFlagsOff_ExpectNoOverlayOrEscape', () => {
   const dismissals = [];
   const root = document.createElement('div');
   const overlay = document.createElement('div');
   let keyHandler = null;
   const originalAdd = document.addEventListener;

   document.addEventListener = (type, handler) => {
      if (type === 'keydown') {
         keyHandler = handler;
      }
   };

   try {
      ItineraryPanelFragment.mountDismissablePopup({
         mountEl: document.body,
         root,
         overlay,
         dismissOnOverlayClick: false,
         dismissOnEscape: false,
         onDismiss: () => {
            dismissals.push(true);
         },
      });

      assert.equal(overlay.listeners.click, undefined);
      keyHandler?.({ key: 'Escape', preventDefault() {} });
      assert.deepEqual(dismissals, []);
   } finally {
      document.addEventListener = originalAdd;
   }
});

test('Test_CreateItineraryPopupLayout_TestJoinClassNames_ExpectPopupBuilder', () => {
   const originalJoin = ItineraryPanelPopupBuilder.joinClassNames;
   const originalButton = ItineraryPanelPopupBuilder.createPopupButton;
   const joins = [];

   ItineraryPanelPopupBuilder.joinClassNames = (...args) => {
      joins.push(args);
      return args.filter(Boolean).join(' ');
   };
   ItineraryPanelPopupBuilder.createPopupButton = (config) => {
      const button = document.createElement('button');
      button.textContent = config.label;
      return button;
   };

   try {
      ItineraryPanelFragment.createItineraryPopupLayout({
         popupClassName: 'extra',
         actionsClassName: 'actions-extra',
         actionButtons: [{ key: 'ok', label: 'OK' }],
      });
      assert.ok(joins.some((args) => args.includes('tzg-popup')));
   } finally {
      ItineraryPanelPopupBuilder.joinClassNames = originalJoin;
      ItineraryPanelPopupBuilder.createPopupButton = originalButton;
   }
});
