import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosedFragment } from '../../../scripts/banners/giftShopClosedFragment.js';
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


test('Test_CreateGiftShopClosedBanner_TestMessage_ExpectShown', () => {
   const message = 'Shop closed';
   const banner = GiftShopClosedFragment.createGiftShopClosedBanner();

   banner.sync({ closed_message: message });

   assert.match(document.body.children.at(Position.LAST).textContent, new RegExp(message));
});
