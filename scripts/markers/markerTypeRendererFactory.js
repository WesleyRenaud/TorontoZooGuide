import { IconUrlProvider } from '../assets/iconUrlProvider.js';
import { MarkerVisualHelper } from './markerVisualHelper.js';

export class MarkerTypeRendererFactory {
   static DEFAULT_ATTRACTION_MARKER_SIZE = 32;

   static LIMITED_VIEWING_MARKER_CLASS = 'marker-has-limited-viewing';

   static CLOSED_RESTROOM_ICON_TOKEN = 'closed';

   static FIRST_AID_AND_FAMILY_CENTER_TYPE = 'First Aid & Family Center';

   static GENERIC_ICON_PATHS = Object.freeze({
      pavilion: '/images/icons/pavilion/pavilion-open.png',
      restroom: '/images/icons/restroom/restroom-open.png',
      transportationStation: '/images/icons/zoomobile-station/zoomobile-station.png',
      guardiansTalk: '/images/icons/guardians-talk/guardians-talk.png',
      wildEncounter: '/images/icons/wild-encounter/wild-encounter.png',
      defibrillator: '/images/icons/defibrillator/defibrillator.png',
      emergencyIntercom: '/images/icons/emergency-intercom/emergency-intercom.png',
      picnicSite: '/images/icons/picnic-site/picnic-site.png',
   });

   static MARKER_CLASS_BY_TYPE = Object.freeze({
      restaurant: 'marker-restaurant',
      restroom: 'marker-restroom',
      giftShop: 'marker-gift-shop',
      attraction: 'marker-attraction',
      transportationStation: 'marker-zoomobile-station',
      transportationRouteMarker: 'marker-zoomobile-route-marker',
      guardiansTalk: 'marker-guardians-talk',
      wildEncounter: 'marker-wild-encounter',
      drinkingFountain: 'marker-drinking-fountain',
      defibrillator: 'marker-defibrillator',
      emergencyIntercom: 'marker-emergency-intercom',
      guestService: 'marker-guest-service',
      firstAidGuestService: 'marker-guest-service-first-aid',
      picnicSite: 'marker-picnic-site',
      eventSite: 'marker-event-site',
   });

   static ZOOMOBILE_ROUTE_COLORS = Object.freeze({
      winter: '#003366',
      default: '#556B2F',
   });

   static ATTRACTION_MARKER_SCALE_OVERRIDES = Object.freeze({
      'Greenhouse': 2.5,
      'Wildlife Health & Science Centre': 2.5,
      'Splash Island': 2.5,
      'Gorilla Climb Ropes Course': 1.35,
      'TundraAir Ride': 2.0,
      'Conservation Carousel': 2.5,
      'Zoomobile': 2.0,
   });

   static shouldShowLimitedViewingIndicator(animal) {
      return Boolean(
         !animal?.off_display_message
         && (
            (animal?.has_limited_viewing_schedule && animal?.limited_viewing_message)
            || animal?.viewing_alert_messages?.length
         )
      );
   }

   static shouldShowRestroomAlertIndicator(restroom) {
      return Boolean(
         !restroom?.is_closed
         && restroom?.has_alert
         && restroom?.alert_message
      );
   }

   static applyAttractionMarkerSize(markerEl, attractionName) {
      const scale = MarkerTypeRendererFactory.ATTRACTION_MARKER_SCALE_OVERRIDES[attractionName];

      if (!scale) return;

      const size = Math.round(MarkerTypeRendererFactory.DEFAULT_ATTRACTION_MARKER_SIZE * scale);
      markerEl.style.width = `${size}px`;
      markerEl.style.height = `${size}px`;
   }

   static applyOptionalSize(markerEl, item, applySize) {
      if (typeof applySize === 'function') {
         applySize(markerEl, item);
      }
   }

   static createGenericIconMarkerRenderer(type) {
      return (markerEl, items) => {
         MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[type]);
         MarkerVisualHelper.applyGenericIcon(markerEl, MarkerTypeRendererFactory.GENERIC_ICON_PATHS[type], items.length);
      };
   }

   static createLikelihoodIconMarkerRenderer({
      type,
      getIconUrl,
      applySize = null,
      getLikelihood = item => item?.likelihood,
   } = {}) {
      return (markerEl, items) => {
         const item = items[0];
         const count = items.length;

         MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[type]);
         MarkerTypeRendererFactory.applyOptionalSize(markerEl, item, applySize);

         const { colour, iconToken } = MarkerVisualHelper.getLikelihoodVisual(getLikelihood(item));

         if (count > 1) {
            MarkerVisualHelper.applyCountMarker(markerEl, count, colour);
            return;
         }

         MarkerVisualHelper.applyBackgroundImage(markerEl, getIconUrl(item, iconToken));
      };
   }

   static renderAnimalMarker(markerEl, items) {
      const animal = items[0];
      const count = items.length;
      const { colour } = MarkerVisualHelper.getLikelihoodVisual(animal?.likelihood);
      const colourForUrl = String(colour || '').replace('#', '');

      if (count > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, count, colour);
      } else {
         MarkerVisualHelper.applyBackgroundImage(
            markerEl,
            IconUrlProvider.getAnimalIconUrl(animal?.exhibit, animal?.species, colourForUrl),
            colour
         );
      }

      if (MarkerTypeRendererFactory.shouldShowLimitedViewingIndicator(animal)) {
         MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.LIMITED_VIEWING_MARKER_CLASS);
      }
   }

   static renderRestroomMarker(markerEl, items) {
      const restroom = items[0];
      const count = items.length;
      const likelihood = restroom?.is_closed ? 0 : 100;
      const { colour, iconToken } = MarkerVisualHelper.getLikelihoodVisual(likelihood);

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.restroom);

      if (count > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, count, colour);
      } else {
         MarkerVisualHelper.applyBackgroundImage(
            markerEl,
            IconUrlProvider.getRestroomIconUrl(
               restroom?.is_closed ? MarkerTypeRendererFactory.CLOSED_RESTROOM_ICON_TOKEN : iconToken
            )
         );
      }

      if (items.some(MarkerTypeRendererFactory.shouldShowRestroomAlertIndicator)) {
         MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.LIMITED_VIEWING_MARKER_CLASS);
      }
   }

   static renderTransportationRouteMarker(markerEl, items) {
      const routeType = items[0]?.route_type;
      const routeColor = MarkerTypeRendererFactory.ZOOMOBILE_ROUTE_COLORS[routeType]
         || MarkerTypeRendererFactory.ZOOMOBILE_ROUTE_COLORS.default;

      markerEl.style.backgroundColor = routeColor;
      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.transportationRouteMarker);
   }

   static renderDrinkingFountainMarker(markerEl, items) {
      const drinkingFountain = items[0];
      const count = items.length;
      const likelihood = Number.isFinite(Number(drinkingFountain?.likelihood))
         ? Number(drinkingFountain.likelihood) * 100
         : (drinkingFountain?.is_closed ? 0 : 100);
      const { colour, iconToken } = MarkerVisualHelper.getLikelihoodVisual(likelihood);

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.drinkingFountain);

      if (count > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, count, colour);
         return;
      }

      MarkerVisualHelper.applyBackgroundImage(
         markerEl,
         IconUrlProvider.getDrinkingFountainIconUrl(iconToken)
      );
   }

   static renderGuestServiceMarker(markerEl, items) {
      const guestService = items[0];
      const serviceType = String(guestService?.service_type || '').trim();

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.guestService);

      if (serviceType === MarkerTypeRendererFactory.FIRST_AID_AND_FAMILY_CENTER_TYPE) {
         MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.firstAidGuestService);
      }

      if (items.length > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, items.length);
         return;
      }

      MarkerVisualHelper.applyBackgroundImage(
         markerEl,
         IconUrlProvider.getGuestServiceIconUrl(serviceType)
      );
   }

   static renderEventSiteMarker(markerEl, items) {
      const eventSite = items[0];

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE.eventSite);

      if (items.length > 1) {
         MarkerVisualHelper.applyCountMarker(markerEl, items.length);
         return;
      }

      MarkerVisualHelper.applyBackgroundImage(
         markerEl,
         IconUrlProvider.getEventSiteIconUrl(eventSite?.name)
      );
   }
}
