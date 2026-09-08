import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { AttractionOutsideOperatingHoursFragment } from '../../../../scripts/itinerary/panel/attractionOutsideOperatingHoursFragment.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShowAttractionOutsideOperatingHoursConfirmation_TestDefaults_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMount = ItineraryPanelFragment.getItineraryPanelMountEl;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;

   try {
      AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation({});
      assert.equal(calls.length, 1);
      assert.equal(
         calls[0].title,
         Strings.itinerary.confirmation.attractionOutsideOperatingHoursTitle
      );
      assert.equal(calls[0].confirmText, Strings.itinerary.actions.adjust);
      assert.equal(calls[0].mountEl, document.body);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryPanelFragment.getItineraryPanelMountEl = originalMount;
   }
});
