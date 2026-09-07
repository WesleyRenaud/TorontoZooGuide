import { AssetKeyNormalizer } from './assetKeyNormalizer.js';
import { IconUrlBuilder } from './iconUrlBuilder.js';

export class IconUrls {
   static getAnimalIconUrl(exhibit, species, backgroundColourForUrl) {
      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildAnimalIconPath(exhibit, species, backgroundColourForUrl)
      );
   }

   static getAttractionIconUrl(attractionName, backgroundColourForUrl) {
      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildAttractionIconPath(attractionName, backgroundColourForUrl)
      );
   }

   static getRestaurantIconUrl(backgroundColourForUrl) {
      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildGenericIconPath('restaurant', backgroundColourForUrl)
      );
   }

   static getGiftShopIconUrl(backgroundColourForUrl) {
      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildGenericIconPath('gift-shop', backgroundColourForUrl)
      );
   }

   static getRestroomIconUrl(backgroundColourForUrl) {
      const variantToken = IconUrlBuilder.normalizeIconVariantToken(backgroundColourForUrl);

      if (variantToken === 'closed') {
         return IconUrlBuilder.buildCssUrl('/images/icons/restroom/restroom-closed.png');
      }

      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildGenericIconPath('restroom', backgroundColourForUrl)
      );
   }

   static getDrinkingFountainIconUrl(backgroundColourForUrl) {
      const variantToken = IconUrlBuilder.normalizeIconVariantToken(backgroundColourForUrl);

      if (variantToken === 'closed') {
         return IconUrlBuilder.buildCssUrl('/images/icons/drinking-fountain/drinking-fountain-closed.png');
      }

      return IconUrlBuilder.buildCssUrl(
         IconUrlBuilder.buildGenericIconPath('drinking-fountain', backgroundColourForUrl)
      );
   }

   static getGuestServiceIconUrl(serviceType) {
      const normalizedServiceType = AssetKeyNormalizer.normalize(serviceType);

      return IconUrlBuilder.buildCssUrl(
         `/images/icons/guest-services/${normalizedServiceType}.png`
      );
   }

   static getEventSiteIconUrl(eventSiteName) {
      const normalizedEventSiteName = AssetKeyNormalizer.normalize(eventSiteName);

      return IconUrlBuilder.buildCssUrl(
         `/images/icons/event-center/${normalizedEventSiteName}.png`
      );
   }
}
