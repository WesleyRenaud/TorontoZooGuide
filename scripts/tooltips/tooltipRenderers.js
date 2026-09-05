import { Animals } from './renderers/animals.js';
import { Attractions } from './renderers/attractions.js';
import { GiftShops } from './renderers/giftShops.js';
import { GuardiansTalks } from './renderers/guardiansTalks.js';
import { Pavilions } from './renderers/pavilions.js';
import { Restaurants } from './renderers/restaurants.js';
import { TransportationStations } from './renderers/transportationStations.js';
import { WildEncounters } from './renderers/wildEncounters.js';

export class TooltipRenderers {
   static TYPE_REGISTRY = {
      animal: Animals,
      pavilion: Pavilions,
      restaurant: Restaurants,
      giftShop: GiftShops,
      attraction: Attractions,
      transportation: Attractions,
      transportationStation: TransportationStations,
      guardiansTalk: GuardiansTalks,
      wildEncounter: WildEncounters,
   };

   static getRendererForItem(item) {
      const key = String(item?.type || '');
      return TooltipRenderers.TYPE_REGISTRY[key] || null;
   }
}
