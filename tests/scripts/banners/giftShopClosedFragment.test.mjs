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


test('Test_CreateGiftShopClosedBanner_TestClosedForSeason_ExpectSeasonStyle', () => {
   const banner = GiftShopClosedFragment.createGiftShopClosedBanner();

   banner.sync({
      closed_message: 'The Zootique is closed for the season.',
      is_closed_for_season: true,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.classList.contains('off-display-closed-banner--season'), true);
   assert.equal(
      bannerEl.querySelector('.off-display-closed-icon')?.children[0]?.getAttribute('class'),
      'off-display-snowflake-icon'
   );
});


test('Test_CreateGiftShopClosedBanner_TestTemporarilyClosed_ExpectWarningStyle', () => {
   const banner = GiftShopClosedFragment.createGiftShopClosedBanner();

   banner.sync({
      closed_message: 'The Zootique is temporarily closed.',
      is_closed_for_season: false,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.classList.contains('off-display-closed-banner--season'), false);
   assert.equal(
      bannerEl.querySelector('.off-display-closed-icon')?.children[0]?.getAttribute('class'),
      'off-display-warning-icon'
   );
});
