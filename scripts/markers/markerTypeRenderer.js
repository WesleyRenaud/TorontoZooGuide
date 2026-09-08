import { IconUrlProvider } from '../assets/iconUrlProvider.js';
import { MarkerTypeRendererFactory } from './markerTypeRendererFactory.js';
import { ItemType } from '../shared/enums/itemType.js';

export class MarkerTypeRenderer {
   static attractionMarkerRenderer = MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
      type: ItemType.ATTRACTION,
      getIconUrl: (attraction, iconToken) => IconUrlProvider.getAttractionIconUrl(
         attraction?.name,
         iconToken
      ),
      applySize: (markerEl, attraction) => MarkerTypeRendererFactory.applyAttractionMarkerSize(
         markerEl,
         attraction?.name
      ),
   });

   static MARKER_TYPE_RENDERERS = {
      [ItemType.ANIMAL]: MarkerTypeRendererFactory.renderAnimalMarker,
      [ItemType.PAVILION]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.PAVILION
      ),
      [ItemType.RESTAURANT]: MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
         type: ItemType.RESTAURANT,
         getIconUrl: (_, iconToken) => IconUrlProvider.getRestaurantIconUrl(iconToken),
      }),
      [ItemType.RESTROOM]: MarkerTypeRendererFactory.renderRestroomMarker,
      [ItemType.GIFT_SHOP]: MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
         type: ItemType.GIFT_SHOP,
         getIconUrl: (_, iconToken) => IconUrlProvider.getGiftShopIconUrl(iconToken),
      }),
      [ItemType.ATTRACTION]: MarkerTypeRenderer.attractionMarkerRenderer,
      [ItemType.TRANSPORTATION]: MarkerTypeRenderer.attractionMarkerRenderer,
      [ItemType.TRANSPORTATION_STATION]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.TRANSPORTATION_STATION
      ),
      [ItemType.TRANSPORTATION_ROUTE_MARKER]: MarkerTypeRendererFactory.renderTransportationRouteMarker,
      [ItemType.GUARDIANS_TALK]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.GUARDIANS_TALK
      ),
      [ItemType.WILD_ENCOUNTER]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.WILD_ENCOUNTER
      ),
      [ItemType.DRINKING_FOUNTAIN]: MarkerTypeRendererFactory.renderDrinkingFountainMarker,
      [ItemType.DEFIBRILLATOR]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.DEFIBRILLATOR
      ),
      [ItemType.EMERGENCY_INTERCOM]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.EMERGENCY_INTERCOM
      ),
      [ItemType.GUEST_SERVICE]: MarkerTypeRendererFactory.renderGuestServiceMarker,
      [ItemType.PICNIC_SITE]: MarkerTypeRendererFactory.createGenericIconMarkerRenderer(
         ItemType.PICNIC_SITE
      ),
      [ItemType.EVENT_SITE]: MarkerTypeRendererFactory.renderEventSiteMarker,
   };

   static renderMarkerByType(markerEl, items) {
      const type = String(items?.[0]?.type || '');
      const renderer = MarkerTypeRenderer.MARKER_TYPE_RENDERERS[type];

      if (!renderer) {
         return false;
      }

      renderer(markerEl, items);
      return true;
   }

   static renderAnimalIcon(markerEl, animal) {
      MarkerTypeRendererFactory.renderAnimalMarker(markerEl, [animal]);
   }
}
