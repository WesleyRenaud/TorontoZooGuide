export class BannerSynchronizer {
   static hasMethod(banner, methodName) {
      if (!banner) {
         return false;
      }

      return typeof banner[methodName] === 'function';
   }

   static createTooltipBannerSync({
      offDisplayBanner,
      restaurantClosedBanner,
      restroomMessageBanner,
      giftShopClosedBanner,
      attractionClosedBanner,
      drinkingFountainClosedBanner,
      onDismiss,
   }) {
      const bannersByType = {
         animal: offDisplayBanner,
         restaurant: restaurantClosedBanner,
         restroom: restroomMessageBanner,
         giftShop: giftShopClosedBanner,
         attraction: attractionClosedBanner,
         drinkingFountain: drinkingFountainClosedBanner,
      };

      const allBanners = Object.values(bannersByType);
      let shownBanner = null;

      allBanners.forEach((banner) => {
         if (!BannerSynchronizer.hasMethod(banner, 'setOnDismiss')) {
            return;
         }

         banner.setOnDismiss(onDismiss);
      });

      function hideAll() {
         shownBanner = null;

         allBanners.forEach((banner) => {
            banner?.hide?.();
         });
      }

      function getFocusableElements() {
         if (!BannerSynchronizer.hasMethod(shownBanner, 'getFocusableElements')) {
            return [];
         }

         return shownBanner.getFocusableElements();
      }

      function findBanner(type) {
         const banner = bannersByType[type];

         if (!banner) {
            return null;
         }

         return banner;
      }

      function sync(item) {
         const type = String(item?.type || '');

         hideAll();
         shownBanner = findBanner(type);

         if (!BannerSynchronizer.hasMethod(shownBanner, 'sync')) {
            return;
         }

         shownBanner.sync(item);
      }

      return {
         hideAll,
         getFocusableElements,
         sync,
      };
   }
}
