import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { ItinerarySettingsFragment } from '../../../../scripts/itinerary/settings/itinerarySettingsFragment.js';
import { ItinerarySettingsView } from '../../../../scripts/itinerary/settings/itinerarySettingsView.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks({
   before: () => {
      globalThis.requestAnimationFrame = (callback) => callback();
   },
   after: () => {
      delete globalThis.requestAnimationFrame;
   },
});

test('Test_ShowItinerarySettingsOverlay_TestMount_ExpectSaveAndCloseCallbacks', () => {
   const closes = [];
   const saves = [];
   const mountEl = document.getElementById('itineraryFlow');
   const originalBuild = ItinerarySettingsView.buildItinerarySettingsView;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const closeButtonEl = document.createElement('button');
   const saveButtonEl = document.createElement('button');
   const root = document.createElement('div');
   root.className = 'itin-overlay itin-settings-overlay';
   let mountedArgs;

   ItinerarySettingsView.buildItinerarySettingsView = (args) => {
      assert.deepEqual(args.statuses, []);
      return {
         root,
         closeButtonEl,
         saveButtonEl,
         checkboxEls: [],
      };
   };
   ItineraryPanelFragment.mountDismissablePopup = (args) => {
      mountedArgs = args;
      assert.equal(args.mountEl, mountEl);
      assert.equal(args.root, root);
      assert.equal(args.overlay, root);
      assert.equal(args.initialFocusEl, saveButtonEl);
      assert.equal(args.dismissOnOverlayClick, false);
      assert.equal(args.dismissOnEscape, false);
      return {
         close: () => {
            closes.push('closed');
         },
         dismiss: () => {
            closes.push('dismissed');
         },
      };
   };

   try {
      const view = ItinerarySettingsFragment.showItinerarySettingsOverlay({
         mountEl,
         statuses: [],
         onClose: ({ close, view: overlayView }) => {
            closes.push('onClose');
            assert.equal(overlayView.closeButtonEl, closeButtonEl);
            close();
         },
         onSave: ({ close, view: overlayView }) => {
            saves.push('onSave');
            assert.equal(overlayView.saveButtonEl, saveButtonEl);
            close();
         },
      });

      assert.equal(view.closeButtonEl, closeButtonEl);
      closeButtonEl.listeners.click();
      assert.deepEqual(closes, ['onClose', 'closed']);

      saveButtonEl.listeners.click();
      assert.deepEqual(saves, ['onSave']);
      assert.deepEqual(closes, ['onClose', 'closed', 'closed']);
      assert.equal(mountedArgs.dismissOnOverlayClick, false);
   } finally {
      ItinerarySettingsView.buildItinerarySettingsView = originalBuild;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});

test('Test_ShowItinerarySettingsOverlay_TestWithoutCallbacks_ExpectCloses', () => {
   const mountEl = document.getElementById('itineraryFlow');
   const originalBuild = ItinerarySettingsView.buildItinerarySettingsView;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const closeButtonEl = document.createElement('button');
   const saveButtonEl = document.createElement('button');
   const closes = [];

   ItinerarySettingsView.buildItinerarySettingsView = () => ({
      root: document.createElement('div'),
      closeButtonEl,
      saveButtonEl,
      checkboxEls: [],
   });
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => {
         closes.push('closed');
      },
      dismiss: () => {},
   });

   try {
      ItinerarySettingsFragment.showItinerarySettingsOverlay({
         mountEl,
      });
      closeButtonEl.listeners.click();
      saveButtonEl.listeners.click();
      assert.deepEqual(closes, ['closed', 'closed']);
   } finally {
      ItinerarySettingsView.buildItinerarySettingsView = originalBuild;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});

test('Test_ShowItinerarySettingsOverlay_TestExistingOverlay_ExpectReplaced', () => {
   const mountEl = document.getElementById('itineraryFlow');
   const first = ItinerarySettingsFragment.showItinerarySettingsOverlay({
      mountEl,
      statuses: [],
   });
   const second = ItinerarySettingsFragment.showItinerarySettingsOverlay({
      mountEl,
      statuses: [],
   });

   assert.equal(
      mountEl.querySelectorAll(ItinerarySettingsFragment.SETTINGS_OVERLAY_SELECTOR).length,
      1
   );
   assert.notEqual(first.root, second.root);
   assert.equal(
      second.root.querySelector('.itin-top-title').textContent,
      Strings.itinerary.settings.title
   );
});
