import { AssetKeyNormalizer } from './assetKeyNormalizer.js';

function buildCssUrl(path) {
   return `url("${path}")`;
}

function normalizeIconVariantToken(token = '') {
   return typeof token === 'string'
      ? token.trim().toLowerCase()
      : '';
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

export function getAnimalIconUrl(exhibit, species, backgroundColourForUrl) {
   return buildCssUrl(
      buildAnimalIconPath(exhibit, species, backgroundColourForUrl)
   );
}

export function getAttractionIconUrl(attractionName, backgroundColourForUrl) {
   return buildCssUrl(
      buildAttractionIconPath(attractionName, backgroundColourForUrl)
   );
}

export function getRestaurantIconUrl(backgroundColourForUrl) {
   return buildCssUrl(
      buildGenericIconPath('restaurant', backgroundColourForUrl)
   );
}

export function getGiftShopIconUrl(backgroundColourForUrl) {
   return buildCssUrl(
      buildGenericIconPath('gift-shop', backgroundColourForUrl)
   );
}

export function getRestroomIconUrl(backgroundColourForUrl) {
   const variantToken = normalizeIconVariantToken(backgroundColourForUrl);

   if (variantToken === 'closed') {
      return buildCssUrl('/images/icons/restroom/restroom-closed.png');
   }

   return buildCssUrl(
      buildGenericIconPath('restroom', backgroundColourForUrl)
   );
}

export function getDrinkingFountainIconUrl(backgroundColourForUrl) {
   const variantToken = normalizeIconVariantToken(backgroundColourForUrl);

   if (variantToken === 'closed') {
      return buildCssUrl('/images/icons/drinking-fountain/drinking-fountain-closed.png');
   }

   return buildCssUrl(
      buildGenericIconPath('drinking-fountain', backgroundColourForUrl)
   );
}

export function getGuestServiceIconUrl(serviceType) {
   const normalizedServiceType = AssetKeyNormalizer.normalize(serviceType);

   return buildCssUrl(
      `/images/icons/guest-services/${normalizedServiceType}.png`
   );
}

export function getEventSiteIconUrl(eventSiteName) {
   const normalizedEventSiteName = AssetKeyNormalizer.normalize(eventSiteName);

   return buildCssUrl(
      `/images/icons/event-center/${normalizedEventSiteName}.png`
   );
}
