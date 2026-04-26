import { normalizeAssetKey } from './normalizeAssetKey.js';

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
   const normalizedExhibit = normalizeAssetKey(exhibit);
   const normalizedAnimal = normalizeAssetKey(species);
   const normalizedVariant = normalizeIconVariantToken(variantToken);

   return `/images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${normalizedVariant}.png`;
}

function buildAttractionIconPath(attractionName, variantToken) {
   const normalizedAttraction = normalizeAssetKey(attractionName);

   if (isOpenIconVariant(variantToken)) {
      return `/images/attraction-icons/${normalizedAttraction}-open.png`;
   }

   const normalizedVariant = normalizeIconVariantToken(variantToken);
   return `/images/attraction-icons/${normalizedAttraction}/${normalizedAttraction}-${normalizedVariant}.png`;
}

function buildGenericIconPath(iconName, variantToken) {
   if (isOpenIconVariant(variantToken)) {
      return `/images/generic-icons/${iconName}-open.png`;
   }

   const normalizedVariant = normalizeIconVariantToken(variantToken);
   return `/images/generic-icons/${iconName}/${iconName}-${normalizedVariant}.png`;
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
      return buildCssUrl('/images/generic-icons/restroom/restroom-closed.png');
   }

   return buildCssUrl(
      buildGenericIconPath('restroom', backgroundColourForUrl)
   );
}
