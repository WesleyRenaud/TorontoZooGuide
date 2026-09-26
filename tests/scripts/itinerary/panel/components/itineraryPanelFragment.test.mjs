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


test('Test_GetItineraryOverlayMountEl_TestFlow_ExpectFlow', () => {
   const flow = document.getElementById('itineraryFlow');

   const mount = ItineraryPanelFragment.getItineraryOverlayMountEl();

   assert.equal(mount, flow);
});


test('Test_GetItineraryOverlayMountEl_TestMissingFlow_ExpectMap', () => {
   const originalGet = document.getElementById;
   const originalQuery = document.querySelector;
   const map = document.createElement('div');
   map.className = 'map-container';

   document.getElementById = () => null;
   document.querySelector = (selector) => (
      selector === `.${map.className}` ? map : originalQuery(selector)
   );

   try {
      const mount = ItineraryPanelFragment.getItineraryOverlayMountEl();

      assert.equal(mount, map);
   } finally {
      document.getElementById = originalGet;
      document.querySelector = originalQuery;
   }
});


test('Test_GetItineraryPanelMountEl_TestPanel_ExpectElement', () => {
   const panel = document.querySelector('.itinerary-panel');

   const mount = ItineraryPanelFragment.getItineraryPanelMountEl();

   assert.equal(mount, panel);
});


test('Test_CreateItineraryPopupLayout_TestMessageAndActions_ExpectStructure', () => {
   const popupClassName = 'tzg-confirm';
   const title = 'Heads up';
   const message = 'Save changes?';

   const layout = ItineraryPanelFragment.createItineraryPopupLayout({
      popupClassName,
      title,
      message,
      actionButtons: [
         { key: 'cancel', label: 'Cancel' },
         { key: 'confirm', label: 'Save', className: 'tzg-popup-confirm' },
      ],
   });

   assert.ok(layout.root.classList.contains('tzg-popup'));
   assert.ok(layout.root.classList.contains(popupClassName));
   assert.equal(layout.root.querySelector('.itin-top-title')?.textContent, title);
   assert.equal(layout.root.querySelector('.tzg-popup-message')?.textContent, message);
   assert.equal(layout.closeButton, null);
   assert.ok(layout.buttonEls.cancel);
   assert.ok(layout.buttonEls.confirm);
});


test('Test_CreateItineraryPopupLayout_TestBodyContentAndClose_ExpectCloseButton', () => {
   const bodyClassName = 'custom-body';
   const bodyContent = document.createElement('div');
   bodyContent.className = bodyClassName;
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
   assert.ok(layout.root.querySelector(`.${bodyClassName}`));
   assert.equal(layout.root.querySelector('.tzg-popup-message'), null);
});


test('Test_MountDismissablePopup_TestMissingArgs_ExpectNoOpClosers', () => {
   const result = ItineraryPanelFragment.mountDismissablePopup({});

   result.close();
   result.dismiss();
});


test('Test_MountDismissablePopup_TestOverlayClick_ExpectDismiss', () => {
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

   const mounted = ItineraryPanelFragment.mountDismissablePopup({
      mountEl: document.body,
      root,
      overlay,
      initialFocusEl: focusEl,
      onDismiss: () => {
         dismissals.push(true);
      },
   });
   overlay.listeners.click({ target: root });
   overlay.listeners.click({ target: overlay });
   mounted.close();
   mounted.dismiss();

   assert.equal(document.body.children.includes?.(root) || document.body.contains?.(root), true);
   assert.deepEqual(focusCalls, [true]);
   assert.deepEqual(dismissals, [true]);
   assert.equal(Boolean(root.parentElement), false);
});


test('Test_MountDismissablePopup_TestEscape_ExpectDismiss', () => {
   const dismissals = [];
   const root = document.createElement('div');
   const overlay = document.createElement('div');
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;
   let keyHandler = null;

   document.addEventListener = (type, handler) => {
      if (type === 'keydown') {
         keyHandler = handler;
      }
   };
   document.removeEventListener = () => {};

   try {
      const mounted = ItineraryPanelFragment.mountDismissablePopup({
         mountEl: document.body,
         root,
         overlay,
         onDismiss: () => {
            dismissals.push('escape');
         },
      });
      keyHandler?.({ key: 'Escape', preventDefault() {} });
      mounted.close();

      assert.ok(dismissals.includes('escape'));
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
   }
});


test('Test_MountDismissablePopup_TestDismissFlagsOff_ExpectNoOverlayOrEscape', () => {
   const dismissals = [];
   const root = document.createElement('div');
   const overlay = document.createElement('div');
   const originalAdd = document.addEventListener;
   let keyHandler = null;

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
      keyHandler?.({ key: 'Escape', preventDefault() {} });

      assert.equal(overlay.listeners.click, undefined);
      assert.deepEqual(dismissals, []);
   } finally {
      document.addEventListener = originalAdd;
   }
});


test('Test_CreateItineraryPopupLayout_TestJoinClassNames_ExpectPopupBuilder', () => {
   const originalJoin = ItineraryPanelPopupBuilder.joinClassNames;
   const originalButton = ItineraryPanelPopupBuilder.createPopupButton;
   const joins = [];
   const popupClassName = 'extra';

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
         popupClassName,
         actionsClassName: 'actions-extra',
         actionButtons: [{ key: 'ok', label: 'OK' }],
      });

      assert.ok(joins.some((args) => args.includes('tzg-popup')));
   } finally {
      ItineraryPanelPopupBuilder.joinClassNames = originalJoin;
      ItineraryPanelPopupBuilder.createPopupButton = originalButton;
   }
});
