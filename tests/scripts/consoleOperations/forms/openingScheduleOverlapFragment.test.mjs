import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleOverlapDialogBuilder } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapDialogBuilder.js';
import { OpeningScheduleOverlapFragment } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { OpeningScheduleOverlapResolution } from '../../../../scripts/shared/enums/openingScheduleOverlapResolution.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _installDialogStubs() {
   const originalCreate = OpeningScheduleOverlapDialogBuilder.createDialogLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const buttons = {
      cancel: document.createElement('button'),
      replace: document.createElement('button'),
      trim: document.createElement('button'),
   };

   OpeningScheduleOverlapDialogBuilder.createDialogLayout = () => ({
      root: document.createElement('div'),
      overlay: document.createElement('div'),
      buttons,
   });
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => {},
      dismiss: () => {},
   });

   return {
      buttons,
      restore() {
         OpeningScheduleOverlapDialogBuilder.createDialogLayout = originalCreate;
         ItineraryPanelFragment.mountDismissablePopup = originalMount;
      },
   };
}


test('Test_ShowOpeningScheduleOverlapDialog_TestReplace_ExpectReplaceResolution', async () => {
   const stubs = _installDialogStubs();

   try {
      const replacePromise = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();
      stubs.buttons.replace.listeners.click();

      const resolution = await replacePromise;

      assert.equal(resolution, OpeningScheduleOverlapResolution.REPLACE);
   } finally {
      stubs.restore();
   }
});


test('Test_ShowOpeningScheduleOverlapDialog_TestTrim_ExpectTrimResolution', async () => {
   const stubs = _installDialogStubs();

   try {
      const trimPromise = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();
      stubs.buttons.trim.listeners.click();

      const resolution = await trimPromise;

      assert.equal(resolution, OpeningScheduleOverlapResolution.TRIM);
   } finally {
      stubs.restore();
   }
});


test('Test_ShowOpeningScheduleOverlapDialog_TestDismiss_ExpectNull', async () => {
   const originalCreate = OpeningScheduleOverlapDialogBuilder.createDialogLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   let onDismiss;

   OpeningScheduleOverlapDialogBuilder.createDialogLayout = () => ({
      root: document.createElement('div'),
      overlay: document.createElement('div'),
      buttons: {
         cancel: document.createElement('button'),
         replace: document.createElement('button'),
         trim: document.createElement('button'),
      },
   });
   ItineraryPanelFragment.mountDismissablePopup = (args) => {
      onDismiss = args.onDismiss;
      return {
         close: () => {},
         dismiss: () => args.onDismiss(),
      };
   };

   try {
      const promise = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();
      onDismiss();

      const resolution = await promise;

      assert.equal(resolution, null);
   } finally {
      OpeningScheduleOverlapDialogBuilder.createDialogLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});
