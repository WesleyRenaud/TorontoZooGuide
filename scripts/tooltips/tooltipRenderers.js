import { animalRenderer } from './renderers/animals.js';
import { pavilionRenderer } from './renderers/pavilions.js';
import { restaurantRenderer } from './renderers/restaurants.js';

export const TYPE_REGISTRY = {
   animal: animalRenderer,
   pavilion: pavilionRenderer,
   restaurant: restaurantRenderer,
   // ✅ do NOT include restroom here at all
};

export function getRendererForItem(item) {
   const key = String(item?.type || '').toLowerCase();
   return TYPE_REGISTRY[key] || null;
}