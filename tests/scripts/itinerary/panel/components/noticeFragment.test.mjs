import assert from 'node:assert/strict';
import test from 'node:test';

import { NoticeFragment } from '../../../../../scripts/itinerary/panel/components/noticeFragment.js';
import { ItineraryPanelFragment } from '../../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShowItineraryNoticePopup_TestConfirm_ExpectClose', async () => {
   const originalCreate = ItineraryPanelFragment.createItineraryPopupLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const closes = [];
   const confirms = [];
   const okButton = document.createElement('button');

   ItineraryPanelFragment.createItineraryPopupLayout = (args) => {
      assert.equal(args.popupClassName, 'tzg-notice');
      assert.equal(args.title, Strings.common.headsUp);
      return {
         root: document.createElement('div'),
         overlay: document.createElement('div'),
         buttonEls: { ok: okButton },
         closeButton: null,
      };
   };
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => { closes.push(true); },
   });

   try {
      NoticeFragment.showItineraryNoticePopup({
         message: 'Hello',
         onConfirm: async () => {
            confirms.push(true);
            return true;
         },
      });

      await okButton.listeners.click();
      assert.deepEqual(confirms, [true]);
      assert.deepEqual(closes, [true]);
   } finally {
      ItineraryPanelFragment.createItineraryPopupLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
   }
});
