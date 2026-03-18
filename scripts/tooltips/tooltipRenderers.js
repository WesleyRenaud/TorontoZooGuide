import { animalRenderer } from './renderers/animals.js';
import { pavilionRenderer } from './renderers/pavilions.js';
import { restaurantRenderer } from './renderers/restaurants.js';
import { giftShopRenderer } from './renderers/giftShops.js';
import { attractionRenderer } from './renderers/attractions.js';
import { zoomobileStationRenderer } from './renderers/zoomobileStations.js';
import { guardiansTalkRenderer } from './renderers/guardiansTalks.js';
import { wildEncounterRenderer } from './renderers/wildEncounters.js';

export const TYPE_REGISTRY = {
   animal: animalRenderer,
   pavilion: pavilionRenderer,
   restaurant: restaurantRenderer,
   giftShop: giftShopRenderer,
   attraction: attractionRenderer,
   zoomobileStation: zoomobileStationRenderer,
   guardiansTalk: guardiansTalkRenderer,
   wildEncounter: wildEncounterRenderer,
};

export function getRendererForItem(item) {
   const key = String(item?.type || '');
   return TYPE_REGISTRY[key] || null;
}