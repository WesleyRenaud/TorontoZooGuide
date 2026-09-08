import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { ConfirmPopupHelper } from '../../../../../scripts/itinerary/panel/components/confirmPopupHelper.js';
import { ItineraryPanelFragment } from '../../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ShowItineraryConfirmPopup_TestConfirm_ExpectDoNotShowAgain', () => {
   const originalCreate = ItineraryPanelFragment.createItineraryPopupLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const originalBody = ConfirmPopupHelper.createConfirmPopupBody;
   const confirms = [];
   const closes = [];
   const confirmButton = document.createElement('button');

   ConfirmPopupHelper.createConfirmPopupBody = () => ({
      body: document.createElement('div'),
      checkbox: { checked: true },
   });
   ItineraryPanelFragment.createItineraryPopupLayout = (args) => {
      assert.equal(args.popupClassName, 'tzg-confirm');
      assert.equal(args.title, Strings.common.headsUp);
      return {
         root: document.createElement('div'),
         overlay: document.createElement('div'),
         buttonEls: {
            cancel: document.createElement('button'),
            confirm: confirmButton,
         },
      };
   };
   ItineraryPanelFragment.mountDismissablePopup = () => ({
      close: () => { closes.push(true); },
      dismiss: () => {},
   });

   try {
      ConfirmFragment.showItineraryConfirmPopup({
         message: 'Confirm?',
         onConfirm: (args) => { confirms.push(args); },
      });

      confirmButton.listeners.click();
      assert.deepEqual(confirms, [{ doNotShowAgain: true }]);
      assert.deepEqual(closes, [true]);
   } finally {
      ItineraryPanelFragment.createItineraryPopupLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
      ConfirmPopupHelper.createConfirmPopupBody = originalBody;
   }
});

test('Test_ShowItineraryConfirmPopup_TestCancel_ExpectOnCancel', () => {
   const originalCreate = ItineraryPanelFragment.createItineraryPopupLayout;
   const originalMount = ItineraryPanelFragment.mountDismissablePopup;
   const originalBody = ConfirmPopupHelper.createConfirmPopupBody;
   const cancels = [];
   const cancelButton = document.createElement('button');

   ConfirmPopupHelper.createConfirmPopupBody = () => document.createElement('div');
   ItineraryPanelFragment.createItineraryPopupLayout = () => ({
      root: document.createElement('div'),
      overlay: document.createElement('div'),
      buttonEls: {
         cancel: cancelButton,
         confirm: document.createElement('button'),
      },
   });
   ItineraryPanelFragment.mountDismissablePopup = ({ onDismiss }) => ({
      close: () => {},
      dismiss: () => onDismiss?.(),
   });

   try {
      ConfirmFragment.showItineraryConfirmPopup({
         message: 'Cancel?',
         onCancel: () => { cancels.push(true); },
      });
      cancelButton.listeners.click();
      assert.deepEqual(cancels, [true]);
   } finally {
      ItineraryPanelFragment.createItineraryPopupLayout = originalCreate;
      ItineraryPanelFragment.mountDismissablePopup = originalMount;
      ConfirmPopupHelper.createConfirmPopupBody = originalBody;
   }
});
