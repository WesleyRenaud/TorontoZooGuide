import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosedFragment } from '../../../scripts/banners/giftShopClosedFragment.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _installCreateElementNS() {
   document.createElementNS = (ns, tagName) => {
      const node = document.createElement(tagName);
      node.namespaceURI = ns;
      return node;
   };
}

installDomTestHooks({ before: _installCreateElementNS });

test('Test_CreateGiftShopClosedBanner_TestMessage_ExpectShown', () => {
   const banner = GiftShopClosedFragment.createGiftShopClosedBanner();
   banner.sync({ closed_message: 'Shop closed' });
   assert.match(document.body.children.at(-1).textContent, /Shop closed/);
});
