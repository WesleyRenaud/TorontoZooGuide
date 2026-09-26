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
