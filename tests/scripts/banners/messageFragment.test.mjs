import assert from 'node:assert/strict';
import test from 'node:test';

import { MessageFragment } from '../../../scripts/banners/messageFragment.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}


function _getIconClass(bannerEl) {
   const iconEl = bannerEl.querySelector('.off-display-closed-icon');
   return iconEl.children[0].getAttribute('class');
}

installDomTestHooks({ before: _installCreateElementNS });


test('Test_CreateSingleMessageBanner_TestEmpty_ExpectUnchanged', () => {
   const banner = MessageFragment.createSingleMessageBanner((item) => item?.closed_message);
   const beforeCount = document.body.children.length;

   banner.sync({});

   assert.equal(document.body.children.length, beforeCount);
});


test('Test_CreateSingleMessageBanner_TestMessage_ExpectShown', () => {
   const message = 'Closed today';
   const banner = MessageFragment.createSingleMessageBanner((item) => item?.closed_message);

   banner.sync({ closed_message: message });
   const el = document.body.children.at(Position.LAST);

   assert.equal(el.className, 'off-display-closed-banner');
   assert.equal(el.style.display, 'flex');
   assert.equal(el.style.getPropertyValue('--alert-banner-width'), '');
   assert.match(el.textContent, new RegExp(message));
});


test('Test_CreateSingleMessageBanner_TestUpdatedMessage_ExpectSameElement', () => {
   const firstMessage = 'Closed today';
   const nextMessage = 'Still closed';
   const banner = MessageFragment.createSingleMessageBanner((item) => item?.closed_message);
   banner.sync({ closed_message: firstMessage });
   const el = document.body.children.at(Position.LAST);

   banner.sync({ closed_message: nextMessage });

   assert.equal(document.body.children.at(Position.LAST), el);
   assert.match(el.textContent, new RegExp(nextMessage));
});


test('Test_CreateMessageBanner_TestOffDisplayForSeason_ExpectSeasonStyleAndSnowflake', () => {
   const banner = MessageFragment.createMessageBanner({
      getMessages: item => [item.message],
      isOffDisplayForSeason: item => item.isSeason,
   });

   banner.sync({ message: 'Off for the season', isSeason: true });
   const el = document.body.children.at(Position.LAST);

   assert.equal(el.classList.contains('off-display-closed-banner--season'), true);
   assert.equal(_getIconClass(el), 'off-display-snowflake-icon');
});


test('Test_CreateMessageBanner_TestSeasonThenRegular_ExpectWarningRestored', () => {
   const banner = MessageFragment.createMessageBanner({
      getMessages: item => [item.message],
      isOffDisplayForSeason: item => item.isSeason,
   });
   banner.sync({ message: 'Off for the season', isSeason: true });
   const el = document.body.children.at(Position.LAST);

   banner.sync({ message: 'Temporarily off display', isSeason: false });

   assert.equal(el.classList.contains('off-display-closed-banner--season'), false);
   assert.equal(_getIconClass(el), 'off-display-warning-icon');
});


test('Test_CreateSingleMessageBanner_TestCloseAndHide_ExpectHidden', () => {
   const banner = MessageFragment.createSingleMessageBanner((item) => item?.closed_message);
   banner.sync({ closed_message: 'Closed today' });
   const el = document.body.children.at(Position.LAST);
   const closeButton = el.querySelector('.off-display-closed-close');

   closeButton.listeners.click({
      stopPropagation() {},
   });
   banner.hide();

   assert.equal(el.style.display, 'none');
});


test('Test_CreateMessageBanner_TestFocusableElements_ExpectCloseButtonOnlyWhileShown', () => {
   const banner = MessageFragment.createSingleMessageBanner((item) => item.closed_message);

   assert.deepEqual(banner.getFocusableElements(), []);

   banner.sync({ closed_message: 'Closed today' });
   const closeButton = document.body.children.at(Position.LAST).querySelector('.off-display-closed-close');

   assert.deepEqual(banner.getFocusableElements(), [closeButton]);

   banner.hide();

   assert.deepEqual(banner.getFocusableElements(), []);
});


test('Test_CreateMessageBanner_TestClose_ExpectHiddenAndDismissHandlerCalled', () => {
   const banner = MessageFragment.createSingleMessageBanner((item) => item.closed_message);
   let dismissals = 0;
   banner.setOnDismiss(() => { dismissals += 1; });
   banner.sync({ closed_message: 'Closed today' });
   const el = document.body.children.at(Position.LAST);
   const closeButton = el.querySelector('.off-display-closed-close');

   closeButton.listeners.click({ stopPropagation() {} });

   assert.equal(el.style.display, 'none');
   assert.equal(dismissals, Position.SECOND);
});
