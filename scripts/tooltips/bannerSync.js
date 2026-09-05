export class BannerSync {
   static createTooltipBannerSync({
      offDisplayBanner,
      restaurantClosedBanner,
      restroomMessageBanner,
      giftShopClosedBanner,
      attractionClosedBanner,
      drinkingFountainClosedBanner,
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

      function hideAll() {
         allBanners.forEach((banner) => {
            banner?.hide?.();
         });
      }

      function sync(item) {
         const type = String(item?.type || '');
         const activeBanner = bannersByType[type] ?? null;

         hideAll();
         activeBanner?.sync?.(item);
      }

      return {
         hideAll,
         sync,
      };
   }
}
