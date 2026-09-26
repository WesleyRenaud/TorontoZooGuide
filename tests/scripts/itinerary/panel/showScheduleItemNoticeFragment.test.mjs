import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ShowScheduleItemNoticeFragment } from '../../../../scripts/itinerary/panel/showScheduleItemNoticeFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      document.querySelector('.tzg-notice')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-notice')?.remove();
   },
});


test('Test_ShowScheduleItemNotice_TestPanelMount_ExpectNoticePopup', () => {
   const message = 'Could not schedule item.';

   ShowScheduleItemNoticeFragment.showScheduleItemNotice(message);

   const popup = document.querySelector('.tzg-notice');
   const title = popup?.querySelector('.itin-top-title');
   const noticeMessage = popup?.querySelector('.tzg-popup-message');
   const button = popup?.querySelector('.tzg-popup-confirm');

   assert.ok(popup);
   assert.equal(title?.textContent, Strings.itinerary.scheduleItem.errorTitle);
   assert.equal(noticeMessage?.textContent, message);
   assert.equal(button?.textContent, Strings.itinerary.actions.ok);
});


test('Test_ShowScheduleItemNotice_TestNoMount_ExpectDocumentBody', () => {
   const message = 'Missing mount.';
   const noticeCalls = [];

   ShowScheduleItemNoticeFragment.showScheduleItemNotice(message, {
      getMountEl: () => null,
      showNoticePopup: (config) => {
         noticeCalls.push(config);
      },
   });

   const notice = noticeCalls.at(Position.FIRST);

   assert.equal(noticeCalls.length, 1);
   assert.equal(notice.mountEl, document.body);
   assert.equal(notice.message, message);
});
