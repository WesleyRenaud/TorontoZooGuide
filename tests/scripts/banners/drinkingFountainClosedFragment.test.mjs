import assert from 'node:assert/strict';
import test from 'node:test';

import { DrinkingFountainClosedFragment } from '../../../scripts/banners/drinkingFountainClosedFragment.js';
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


test('Test_CreateDrinkingFountainClosedBanner_TestMessage_ExpectShown', () => {
   const message = 'Fountain closed';
   const banner = DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner();

   banner.sync({ closed_message: message });

   assert.match(document.body.children.at(Position.LAST).textContent, new RegExp(message));
});


test('Test_CreateDrinkingFountainClosedBanner_TestClosedForSeason_ExpectSeasonStyle', () => {
   const banner = DrinkingFountainClosedFragment.createDrinkingFountainClosedBanner();

   banner.sync({
      closed_message: 'The drinking fountains are closed for the season.',
      is_closed_for_season: true,
   });
   const bannerEl = document.body.children.at(Position.LAST);

   assert.equal(bannerEl.classList.contains('off-display-closed-banner--season'), true);
   assert.equal(
      bannerEl.querySelector('.off-display-closed-icon')?.children[0]?.getAttribute('class'),
      'off-display-snowflake-icon'
   );
});
