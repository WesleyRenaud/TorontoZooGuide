import { ValueNormalizer } from '../api/valueNormalizer.js';
import { IconUrlProvider } from '../assets/iconUrlProvider.js';
import { MarkerVisualHelper } from './markerVisualHelper.js';
import { ItemType } from '../shared/enums/itemType.js';

export class MarkerTypeRendererFactory {
   static DEFAULT_ATTRACTION_MARKER_SIZE = 32;

   static LIMITED_VIEWING_MARKER_CLASS = 'marker-has-limited-viewing';

   static CLOSED_RESTROOM_ICON_TOKEN = 'closed';

   static FIRST_AID_AND_FAMILY_CENTER_TYPE = 'First Aid & Family Center';

   static GENERIC_ICON_PATHS = Object.freeze({
      [ItemType.PAVILION]: '/images/icons/pavilion/pavilion-open.png',
      [ItemType.RESTROOM]: '/images/icons/restroom/restroom-open.png',
      [ItemType.TRANSPORTATION_STATION]: '/images/icons/zoomobile-station/zoomobile-station.png',
      [ItemType.GUARDIANS_TALK]: '/images/icons/guardians-talk/guardians-talk.png',
      [ItemType.WILD_ENCOUNTER]: '/images/icons/wild-encounter/wild-encounter.png',
      [ItemType.DEFIBRILLATOR]: '/images/icons/defibrillator/defibrillator.png',
      [ItemType.EMERGENCY_INTERCOM]: '/images/icons/emergency-intercom/emergency-intercom.png',
      [ItemType.PICNIC_SITE]: '/images/icons/picnic-site/picnic-site.png',
   });

   static MARKER_CLASS_BY_TYPE = Object.freeze({
      [ItemType.RESTAURANT]: 'marker-restaurant',
      [ItemType.RESTROOM]: 'marker-restroom',
      [ItemType.GIFT_SHOP]: 'marker-gift-shop',
      [ItemType.ATTRACTION]: 'marker-attraction',
      [ItemType.TRANSPORTATION_STATION]: 'marker-zoomobile-station',
      [ItemType.TRANSPORTATION_ROUTE_MARKER]: 'marker-zoomobile-route-marker',
      [ItemType.GUARDIANS_TALK]: 'marker-guardians-talk',
      [ItemType.WILD_ENCOUNTER]: 'marker-wild-encounter',
      [ItemType.DRINKING_FOUNTAIN]: 'marker-drinking-fountain',
      [ItemType.DEFIBRILLATOR]: 'marker-defibrillator',
      [ItemType.EMERGENCY_INTERCOM]: 'marker-emergency-intercom',
      [ItemType.GUEST_SERVICE]: 'marker-guest-service',
      firstAidGuestService: 'marker-guest-service-first-aid',
      [ItemType.PICNIC_SITE]: 'marker-picnic-site',
      [ItemType.EVENT_SITE]: 'marker-event-site',
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

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.RESTROOM]);

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
      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.TRANSPORTATION_ROUTE_MARKER]);
   }

   static renderDrinkingFountainMarker(markerEl, items) {
      const drinkingFountain = items[0];
      const count = items.length;
      const likelihood = Number.isFinite(Number(drinkingFountain?.likelihood))
         ? Number(drinkingFountain.likelihood) * 100
         : (drinkingFountain?.is_closed ? 0 : 100);
      const { colour, iconToken } = MarkerVisualHelper.getLikelihoodVisual(likelihood);

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.DRINKING_FOUNTAIN]);

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
      const serviceType = ValueNormalizer.asTrimmedString(guestService?.service_type);

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.GUEST_SERVICE]);

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

      MarkerVisualHelper.applyMarkerClass(markerEl, MarkerTypeRendererFactory.MARKER_CLASS_BY_TYPE[ItemType.EVENT_SITE]);

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
