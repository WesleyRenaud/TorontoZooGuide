import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantTooltipRenderer } from '../../../../scripts/tooltips/renderers/restaurantTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateCard_TestRestaurant_ExpectNamedCard', () => {
   const card = RestaurantTooltipRenderer.createCard({
      name: 'Simba Safari Cafe',
      location: 'Africa',
      description: 'Meals',
      menu_link: 'https://example.test/menu',
   }, 0);
   assert.equal(RestaurantTooltipRenderer.key, 'restaurant');
   assert.match(card.textContent, /Simba Safari Cafe/);
   assert.match(card.textContent, /Africa/);
});
