export function createTooltipBannerSync({
   offDisplayBanner,
   restaurantClosedBanner,
   restroomMessageBanner,
   giftShopClosedBanner,
   attractionClosedBanner,
}) {
   const bannersByType = {
      animal: offDisplayBanner,
      restaurant: restaurantClosedBanner,
      restroom: restroomMessageBanner,
      giftShop: giftShopClosedBanner,
      attraction: attractionClosedBanner,
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
