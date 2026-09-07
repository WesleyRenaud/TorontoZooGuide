import { IconUrls } from '../assets/iconUrls.js';
import { MarkerTypeRendererFactory } from './markerTypeRendererFactory.js';

const attractionMarkerRenderer = MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
   type: 'attraction',
   getIconUrl: (attraction, iconToken) => IconUrls.getAttractionIconUrl(
      attraction?.name,
      iconToken
   ),
   applySize: (markerEl, attraction) => MarkerTypeRendererFactory.applyAttractionMarkerSize(
      markerEl,
      attraction?.name
   ),
});

const MARKER_TYPE_RENDERERS = {
   animal: MarkerTypeRendererFactory.renderAnimalMarker,
   pavilion: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('pavilion'),
   restaurant: MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
      type: 'restaurant',
      getIconUrl: (_, iconToken) => IconUrls.getRestaurantIconUrl(iconToken),
   }),
   restroom: MarkerTypeRendererFactory.renderRestroomMarker,
   giftShop: MarkerTypeRendererFactory.createLikelihoodIconMarkerRenderer({
      type: 'giftShop',
      getIconUrl: (_, iconToken) => IconUrls.getGiftShopIconUrl(iconToken),
   }),
   attraction: attractionMarkerRenderer,
   transportation: attractionMarkerRenderer,
   transportationStation: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('transportationStation'),
   transportationRouteMarker: MarkerTypeRendererFactory.renderTransportationRouteMarker,
   guardiansTalk: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('guardiansTalk'),
   wildEncounter: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('wildEncounter'),
   drinkingFountain: MarkerTypeRendererFactory.renderDrinkingFountainMarker,
   defibrillator: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('defibrillator'),
   emergencyIntercom: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('emergencyIntercom'),
   guestService: MarkerTypeRendererFactory.renderGuestServiceMarker,
   picnicSite: MarkerTypeRendererFactory.createGenericIconMarkerRenderer('picnicSite'),
   eventSite: MarkerTypeRendererFactory.renderEventSiteMarker,
};

export class MarkerTypeRenderers {
   static renderMarkerByType(markerEl, items) {
      const type = String(items?.[0]?.type || '');
      const renderer = MARKER_TYPE_RENDERERS[type];

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
