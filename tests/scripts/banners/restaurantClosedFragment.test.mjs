import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantClosedFragment } from '../../../scripts/banners/restaurantClosedFragment.js';
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


test('Test_CreateRestaurantClosedBanner_TestMessage_ExpectShown', () => {
   const message = 'Restaurant closed';
   const banner = RestaurantClosedFragment.createRestaurantClosedBanner();

   banner.sync({ closed_message: message });

   assert.match(document.body.children.at(Position.LAST).textContent, new RegExp(message));
});


test('Test_CreateRestaurantClosedBanner_TestClosedForSeason_ExpectSeasonStyle', () => {
   const banner = RestaurantClosedFragment.createRestaurantClosedBanner();

   banner.sync({
      closed_message: 'The Africa Restaurant is closed for the season.',
      is_closed_for_season: true,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.classList.contains('off-display-closed-banner--season'), true);
   assert.equal(
      bannerEl.querySelector('.off-display-closed-icon')?.children[0]?.getAttribute('class'),
      'off-display-snowflake-icon'
   );
});


test('Test_CreateRestaurantClosedBanner_TestTemporarilyClosed_ExpectWarningStyle', () => {
   const banner = RestaurantClosedFragment.createRestaurantClosedBanner();

   banner.sync({
      closed_message: 'The Africa Restaurant is temporarily closed.',
      is_closed_for_season: false,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.classList.contains('off-display-closed-banner--season'), false);
   assert.equal(
      bannerEl.querySelector('.off-display-closed-icon')?.children[0]?.getAttribute('class'),
      'off-display-warning-icon'
   );
});
