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
   const closed = 'closed';
   const onCloseEvent = 'onClose';
   const onSaveEvent = 'onSave';
   const statuses = [];
   const mountEl = document.getElementById('itineraryFlow');
   const originalBuild = ItinerarySettingsView.buildItinerarySettingsView;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const closeButtonEl = document.createElement('button');
   const saveButtonEl = document.createElement('button');
   const root = document.createElement('div');
   const dismissOnOverlayClick = false;
   const dismissOnEscape = false;
   root.className = 'itin-overlay itin-settings-overlay';
   let builtArgs;
   let mountedArgs;
   let closedView;
   let savedView;
   ItinerarySettingsView.buildItinerarySettingsView = (args) => {
      builtArgs = args;
      return {
         root,
         closeButtonEl,
         saveButtonEl,
         checkboxEls: [],
      };
   };
   ItineraryPanelFragment.mountDismissablePopup = (args) => {
      mountedArgs = args;
      return {
         close: () => {
            closes.push(closed);
         },
         dismiss: () => {
            closes.push('dismissed');
         },
      };
   };

   try {
      const view = ItinerarySettingsFragment.showItinerarySettingsOverlay({
         mountEl,
         statuses,
         onClose: ({ close, view: overlayView }) => {
            closes.push(onCloseEvent);
            closedView = overlayView;
            close();
         },
         onSave: ({ close, view: overlayView }) => {
            saves.push(onSaveEvent);
            savedView = overlayView;
            close();
         },
      });
      closeButtonEl.listeners.click();
      saveButtonEl.listeners.click();

      assert.equal(builtArgs.statuses, statuses);
      assert.equal(mountedArgs.mountEl, mountEl);
      assert.equal(mountedArgs.root, root);
      assert.equal(mountedArgs.overlay, root);
      assert.equal(mountedArgs.initialFocusEl, saveButtonEl);
      assert.equal(mountedArgs.dismissOnOverlayClick, dismissOnOverlayClick);
      assert.equal(mountedArgs.dismissOnEscape, dismissOnEscape);
      assert.equal(view.closeButtonEl, closeButtonEl);
      assert.equal(closedView.closeButtonEl, closeButtonEl);
      assert.equal(savedView.saveButtonEl, saveButtonEl);
      assert.deepEqual(saves, [onSaveEvent]);
      assert.deepEqual(closes, [onCloseEvent, closed, closed]);
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
   const closed = 'closed';
   const closes = [];
   ItinerarySettingsView.buildItinerarySettingsView = () => ({
      root: document.createElement('div'),
      closeButtonEl,
      saveButtonEl,
      checkboxEls: [],
   });
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => {
         closes.push(closed);
      },
      dismiss: () => {},
   });

   try {
      const view = ItinerarySettingsFragment.showItinerarySettingsOverlay({
         mountEl,
      });
      closeButtonEl.listeners.click();
      saveButtonEl.listeners.click();

      assert.equal(view.closeButtonEl, closeButtonEl);
      assert.deepEqual(closes, [closed, closed]);
   } finally {
      ItinerarySettingsView.buildItinerarySettingsView = originalBuild;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});


test('Test_ShowItinerarySettingsOverlay_TestExistingOverlay_ExpectReplaced', () => {
   const mountEl = document.getElementById('itineraryFlow');
   const statuses = [];

   const first = ItinerarySettingsFragment.showItinerarySettingsOverlay({
      mountEl,
      statuses,
   });
   const second = ItinerarySettingsFragment.showItinerarySettingsOverlay({
      mountEl,
      statuses,
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
