import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { EarlyAdmissionFragment } from '../../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShowEarlyAdmissionConfirmation_TestDefaults_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMount = ItineraryPanelFragment.getItineraryPanelMountEl;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;

   try {
      const onConfirm = () => {};
      const onCancel = () => {};
      EarlyAdmissionFragment.showEarlyAdmissionConfirmation({ onConfirm, onCancel });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.earlyAdmissionTitle);
      assert.equal(calls[0].message, Strings.itinerary.confirmation.earlyAdmissionMessage);
      assert.equal(calls[0].onConfirm, onConfirm);
      assert.equal(calls[0].onCancel, onCancel);
      assert.equal(calls[0].mountEl, document.body);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryPanelFragment.getItineraryPanelMountEl = originalMount;
   }
});
