import { normalizeAssetKey } from './normalizeAssetKey.js';

export function getAnimalIconUrl(exhibit, species, backgroundColourForUrl) {
   const normalizedExhibit = normalizeAssetKey(exhibit);
   const normalizedAnimal = normalizeAssetKey(species);

   return `url("/images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${backgroundColourForUrl}.png")`;
}

export function getAttractionIconUrl(attractionName, backgroundColourForUrl) {
   const normalizedAttraction = normalizeAssetKey(attractionName);

   if (!backgroundColourForUrl || backgroundColourForUrl == 'open') {
      return `url("/images/attraction-icons/${normalizedAttraction}-open.png")`;
   }

   return `url("/images/attraction-icons/${normalizedAttraction}/${normalizedAttraction}-${backgroundColourForUrl}.png")`;
}

export function getRestaurantIconUrl(backgroundColourForUrl) {
   if (!backgroundColourForUrl || backgroundColourForUrl == 'open') {
      return 'url("/images/generic-icons/restaurant-open.png")';
   }

   return `url("/images/generic-icons/restaurant/restaurant-${backgroundColourForUrl}.png")`;
}

export function getGiftShopIconUrl(backgroundColourForUrl) {
   if (!backgroundColourForUrl || backgroundColourForUrl == 'open') {
      return 'url("/images/generic-icons/gift-shop-open.png")';
   }

   return `url("/images/generic-icons/gift-shop/gift-shop-${backgroundColourForUrl}.png")`;
}
