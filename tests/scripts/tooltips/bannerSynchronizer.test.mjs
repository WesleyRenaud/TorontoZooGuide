import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../scripts/shared/enums/position.js';
import { BannerSynchronizer } from '../../../scripts/tooltips/bannerSynchronizer.js';


function _createBanner() {
   return {
      hides: 0,
      syncs: [],
      hide() {
         this.hides += 1;
      },
      sync(item) {
         this.syncs.push(item);
      },
   };
}


test('Test_CreateTooltipBannerSync_TestRestaurant_ExpectActiveBannerSynced', () => {
   const animal = _createBanner();
   const restaurant = _createBanner();
   const restroom = _createBanner();
   const giftShop = _createBanner();
   const attraction = _createBanner();
   const drinkingFountain = _createBanner();
   const item = { type: 'restaurant', name: 'Peaks' };
   const syncer = BannerSynchronizer.createTooltipBannerSync({
      offDisplayBanner: animal,
      restaurantClosedBanner: restaurant,
      restroomMessageBanner: restroom,
      giftShopClosedBanner: giftShop,
      attractionClosedBanner: attraction,
      drinkingFountainClosedBanner: drinkingFountain,
   });

   syncer.sync(item);

   assert.equal(restaurant.syncs.length, Position.SECOND);
   assert.deepEqual(restaurant.syncs.at(Position.FIRST), item);
   assert.equal(animal.hides, Position.SECOND);
   assert.equal(giftShop.hides, Position.SECOND);
});


test('Test_CreateTooltipBannerSync_TestHideAll_ExpectHidden', () => {
   const animal = _createBanner();
   const restaurant = _createBanner();
   const restroom = _createBanner();
   const giftShop = _createBanner();
   const attraction = _createBanner();
   const drinkingFountain = _createBanner();
   const syncer = BannerSynchronizer.createTooltipBannerSync({
      offDisplayBanner: animal,
      restaurantClosedBanner: restaurant,
      restroomMessageBanner: restroom,
      giftShopClosedBanner: giftShop,
      attractionClosedBanner: attraction,
      drinkingFountainClosedBanner: drinkingFountain,
   });
   syncer.sync({ type: 'restaurant', name: 'Peaks' });

   syncer.hideAll();

   assert.equal(restaurant.hides, 2);
});


test('Test_CreateTooltipBannerSync_TestUnknown_ExpectNoAttractionSync', () => {
   const animal = _createBanner();
   const restaurant = _createBanner();
   const restroom = _createBanner();
   const giftShop = _createBanner();
   const attraction = _createBanner();
   const drinkingFountain = _createBanner();
   const syncer = BannerSynchronizer.createTooltipBannerSync({
      offDisplayBanner: animal,
      restaurantClosedBanner: restaurant,
      restroomMessageBanner: restroom,
      giftShopClosedBanner: giftShop,
      attractionClosedBanner: attraction,
      drinkingFountainClosedBanner: drinkingFountain,
   });

   syncer.sync({ type: 'unknown' });

   assert.equal(attraction.syncs.length, 0);
});
