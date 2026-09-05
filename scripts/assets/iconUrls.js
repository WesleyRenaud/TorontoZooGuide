import { ValueNormalizer } from '../api/valueNormalizer.js';
import { AssetKeyNormalizer } from './assetKeyNormalizer.js';

function buildCssUrl(path) {
   return `url("${path}")`;
}

function normalizeIconVariantToken(token = '') {
   return ValueNormalizer.asTrimmedString(token).toLowerCase();
}

function isOpenIconVariant(token) {
   const variantToken = normalizeIconVariantToken(token);
   return !variantToken || variantToken === 'open';
}

function buildAnimalIconPath(exhibit, species, variantToken) {
   const normalizedExhibit = AssetKeyNormalizer.normalize(exhibit);
   const normalizedAnimal = AssetKeyNormalizer.normalize(species);
   const normalizedVariant = normalizeIconVariantToken(variantToken);

   return `/images/icons/animals/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${normalizedVariant}.png`;
}

function buildAttractionIconPath(attractionName, variantToken) {
   const normalizedAttraction = AssetKeyNormalizer.normalize(attractionName);

   if (isOpenIconVariant(variantToken)) {
      return `/images/icons/attractions/${normalizedAttraction}-open.png`;
   }

   const normalizedVariant = normalizeIconVariantToken(variantToken);
   return `/images/icons/attractions/${normalizedAttraction}/${normalizedAttraction}-${normalizedVariant}.png`;
}

function buildGenericIconPath(iconName, variantToken) {
   const normalizedVariant = isOpenIconVariant(variantToken)
      ? 'open'
      : normalizeIconVariantToken(variantToken);

   return `/images/icons/${iconName}/${iconName}-${normalizedVariant}.png`;
}

export class IconUrls {
   static getAnimalIconUrl(exhibit, species, backgroundColourForUrl) {
      return buildCssUrl(
         buildAnimalIconPath(exhibit, species, backgroundColourForUrl)
      );
   }

   static getAttractionIconUrl(attractionName, backgroundColourForUrl) {
      return buildCssUrl(
         buildAttractionIconPath(attractionName, backgroundColourForUrl)
      );
   }

   static getRestaurantIconUrl(backgroundColourForUrl) {
      return buildCssUrl(
         buildGenericIconPath('restaurant', backgroundColourForUrl)
      );
   }

   static getGiftShopIconUrl(backgroundColourForUrl) {
      return buildCssUrl(
         buildGenericIconPath('gift-shop', backgroundColourForUrl)
      );
   }

   static getRestroomIconUrl(backgroundColourForUrl) {
      const variantToken = normalizeIconVariantToken(backgroundColourForUrl);

      if (variantToken === 'closed') {
         return buildCssUrl('/images/icons/restroom/restroom-closed.png');
      }

      return buildCssUrl(
         buildGenericIconPath('restroom', backgroundColourForUrl)
      );
   }

   static getDrinkingFountainIconUrl(backgroundColourForUrl) {
      const variantToken = normalizeIconVariantToken(backgroundColourForUrl);

      if (variantToken === 'closed') {
         return buildCssUrl('/images/icons/drinking-fountain/drinking-fountain-closed.png');
      }

      return buildCssUrl(
         buildGenericIconPath('drinking-fountain', backgroundColourForUrl)
      );
   }

   static getGuestServiceIconUrl(serviceType) {
      const normalizedServiceType = AssetKeyNormalizer.normalize(serviceType);

      return buildCssUrl(
         `/images/icons/guest-services/${normalizedServiceType}.png`
      );
   }

   static getEventSiteIconUrl(eventSiteName) {
      const normalizedEventSiteName = AssetKeyNormalizer.normalize(eventSiteName);

      return buildCssUrl(
         `/images/icons/event-center/${normalizedEventSiteName}.png`
      );
   }
}
