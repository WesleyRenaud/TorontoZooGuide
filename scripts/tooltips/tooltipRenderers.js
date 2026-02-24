import { animalRenderer } from './renderers/animals.js';
import { pavilionRenderer } from './renderers/pavilions.js';
import { restaurantRenderer } from './renderers/restaurants.js';
import { giftShopRenderer } from './renderers/giftShops.js';
import { attractionRenderer } from './renderers/attractions.js';

export const TYPE_REGISTRY = {
   animal: animalRenderer,
   pavilion: pavilionRenderer,
   restaurant: restaurantRenderer,
   // ✅ do NOT include restroom here at all
   giftShop: giftShopRenderer,
   attraction: attractionRenderer,
};

export function getRendererForItem(item) {
   const key = String(item?.type || '');
   return TYPE_REGISTRY[key] || null;
}