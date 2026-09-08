import assert from 'node:assert/strict';
import test from 'node:test';

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

test('Test_CreateTooltipBannerSync_TestTypes_ExpectActiveBannerSynced', () => {
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
   assert.equal(restaurant.syncs.length, 1);
   assert.deepEqual(restaurant.syncs[0], { type: 'restaurant', name: 'Peaks' });
   assert.equal(animal.hides, 1);
   assert.equal(giftShop.hides, 1);

   syncer.hideAll();
   assert.equal(restaurant.hides, 2);

   syncer.sync({ type: 'unknown' });
   assert.equal(attraction.syncs.length, 0);
});
