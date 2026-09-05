import { animalRenderer } from './renderers/animals.js';
import { attractionRenderer } from './renderers/attractions.js';
import { giftShopRenderer } from './renderers/giftShops.js';
import { guardiansTalkRenderer } from './renderers/guardiansTalks.js';
import { pavilionRenderer } from './renderers/pavilions.js';
import { restaurantRenderer } from './renderers/restaurants.js';
import { transportationStationRenderer } from './renderers/transportationStations.js';
import { wildEncounterRenderer } from './renderers/wildEncounters.js';

export class TooltipRenderers {
   static TYPE_REGISTRY = {
      animal: animalRenderer,
      pavilion: pavilionRenderer,
      restaurant: restaurantRenderer,
      giftShop: giftShopRenderer,
      attraction: attractionRenderer,
      transportation: attractionRenderer,
      transportationStation: transportationStationRenderer,
      guardiansTalk: guardiansTalkRenderer,
      wildEncounter: wildEncounterRenderer,
   };

   static getRendererForItem(item) {
      const key = String(item?.type || '');
      return TooltipRenderers.TYPE_REGISTRY[key] || null;
   }
}
