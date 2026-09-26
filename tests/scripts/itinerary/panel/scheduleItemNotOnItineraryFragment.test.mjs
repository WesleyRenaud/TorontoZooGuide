import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { ScheduleItemNotOnItineraryFragment } from '../../../../scripts/itinerary/panel/scheduleItemNotOnItineraryFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ShowScheduleItemNotOnItineraryConfirmation_TestDefaults_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMount = ItineraryPanelFragment.getItineraryPanelMountEl;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;

   try {
      ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation({});

      const confirmation = calls.at(Position.FIRST);

      assert.equal(calls.length, 1);
      assert.equal(
         confirmation.title,
         Strings.itinerary.confirmation.scheduleItemNotOnItineraryTitle
      );
      assert.equal(
         confirmation.confirmText,
         Strings.itinerary.confirmation.scheduleItemNotOnItineraryConfirm
      );
      assert.equal(confirmation.mountEl, document.body);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      ItineraryPanelFragment.getItineraryPanelMountEl = originalMount;
   }
});
