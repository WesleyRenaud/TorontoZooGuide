import { AnimalTooltipRenderer } from './renderers/animalTooltipRenderer.js';
import { AttractionTooltipRenderer } from './renderers/attractionTooltipRenderer.js';
import { GiftShopTooltipRenderer } from './renderers/giftShopTooltipRenderer.js';
import { GuardiansTalkTooltipRenderer } from './renderers/guardiansTalkTooltipRenderer.js';
import { PavilionTooltipRenderer } from './renderers/pavilionTooltipRenderer.js';
import { RestaurantTooltipRenderer } from './renderers/restaurantTooltipRenderer.js';
import { TransportationStationTooltipRenderer } from './renderers/transportationStationTooltipRenderer.js';
import { WildEncounterTooltipRenderer } from './renderers/wildEncounterTooltipRenderer.js';

export class TooltipRenderer {
   static TYPE_REGISTRY = {
      animal: AnimalTooltipRenderer,
      pavilion: PavilionTooltipRenderer,
      restaurant: RestaurantTooltipRenderer,
      giftShop: GiftShopTooltipRenderer,
      attraction: AttractionTooltipRenderer,
      transportation: AttractionTooltipRenderer,
      transportationStation: TransportationStationTooltipRenderer,
      guardiansTalk: GuardiansTalkTooltipRenderer,
      wildEncounter: WildEncounterTooltipRenderer,
   };

   static getRendererForItem(item) {
      const key = String(item?.type || '');
      return TooltipRenderer.TYPE_REGISTRY[key] || null;
   }
}
