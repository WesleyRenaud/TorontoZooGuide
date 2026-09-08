import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleOverlapFragment } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleOverlapDialogBuilder } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapDialogBuilder.js';
import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShowOpeningScheduleOverlapDialog_TestReplaceAndTrim_ExpectResolutions', async () => {
   const originalCreate = OpeningScheduleOverlapDialogBuilder.createDialogLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   let buttons;

   OpeningScheduleOverlapDialogBuilder.createDialogLayout = () => {
      buttons = {
         cancel: document.createElement('button'),
         replace: document.createElement('button'),
         trim: document.createElement('button'),
      };
      return {
         root: document.createElement('div'),
         overlay: document.createElement('div'),
         buttons,
      };
   };
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => {},
      dismiss: () => {},
   });

   try {
      const replacePromise = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();
      buttons.replace.listeners.click();
      assert.equal(
         await replacePromise,
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );

      const trimPromise = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();
      buttons.trim.listeners.click();
      assert.equal(
         await trimPromise,
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
      );
   } finally {
      OpeningScheduleOverlapDialogBuilder.createDialogLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
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
      assert.equal(await promise, null);
   } finally {
      OpeningScheduleOverlapDialogBuilder.createDialogLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});
