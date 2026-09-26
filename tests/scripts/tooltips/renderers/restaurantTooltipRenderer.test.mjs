import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { RestaurantTooltipRenderer } from '../../../../scripts/tooltips/renderers/restaurantTooltipRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateCard_TestRestaurant_ExpectNamedCard', () => {
   const name = 'Simba Safari Cafe';
   const location = 'Africa';

   const card = RestaurantTooltipRenderer.createCard({
      name,
      location,
      description: 'Meals',
      menu_link: 'https://example.test/menu',
   }, Position.FIRST);

   assert.equal(RestaurantTooltipRenderer.key, 'restaurant');
   assert.match(card.textContent, new RegExp(name));
   assert.match(card.textContent, new RegExp(location));
});
