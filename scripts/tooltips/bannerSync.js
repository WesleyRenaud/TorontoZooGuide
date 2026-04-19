export function createTooltipBannerSync({
   offDisplayBanner,
   restaurantClosedBanner,
   giftShopClosedBanner,
   attractionClosedBanner,
}) {
   function hideAll() {
      offDisplayBanner?.hide?.();
      restaurantClosedBanner?.hide?.();
      giftShopClosedBanner?.hide?.();
      attractionClosedBanner?.hide?.();
   }

   function sync(item) {
      const type = String(item?.type || '');

      if (type === 'animal') {
         offDisplayBanner?.sync?.(item);
         restaurantClosedBanner?.hide?.();
         giftShopClosedBanner?.hide?.();
         attractionClosedBanner?.hide?.();
         return;
      }

      if (type === 'restaurant') {
         restaurantClosedBanner?.sync?.(item);
         offDisplayBanner?.hide?.();
         giftShopClosedBanner?.hide?.();
         attractionClosedBanner?.hide?.();
         return;
      }

      if (type === 'giftShop') {
         giftShopClosedBanner?.sync?.(item);
         offDisplayBanner?.hide?.();
         restaurantClosedBanner?.hide?.();
         attractionClosedBanner?.hide?.();
         return;
      }

      if (type === 'attraction') {
         attractionClosedBanner?.sync?.(item);
         offDisplayBanner?.hide?.();
         restaurantClosedBanner?.hide?.();
         giftShopClosedBanner?.hide?.();
         return;
      }

      hideAll();
   }

   return {
      hideAll,
      sync,
   };
}
