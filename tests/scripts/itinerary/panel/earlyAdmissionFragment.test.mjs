import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { EarlyAdmissionFragment } from '../../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ShowEarlyAdmissionConfirmation_TestDefaults_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMount = ItineraryPanelFragment.getItineraryPanelMountEl;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;
   const onConfirm = () => {};
   const onCancel = () => {};

   try {
      EarlyAdmissionFragment.showEarlyAdmissionConfirmation({ onConfirm, onCancel });

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(confirmation.title, Strings.itinerary.confirmation.earlyAdmissionTitle);
      assert.equal(confirmation.message, Strings.itinerary.confirmation.earlyAdmissionMessage);
      assert.equal(confirmation.onConfirm, onConfirm);
      assert.equal(confirmation.onCancel, onCancel);
      assert.equal(confirmation.mountEl, document.body);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryPanelFragment.getItineraryPanelMountEl = originalMount;
   }
});
