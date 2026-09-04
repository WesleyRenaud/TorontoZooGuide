import {
   getAnimalIconUrl,
   getAttractionIconUrl,
   getDrinkingFountainIconUrl,
   getEventSiteIconUrl,
   getGiftShopIconUrl,
   getGuestServiceIconUrl,
   getRestaurantIconUrl,
   getRestroomIconUrl,
} from '../assets/iconUrls.js';
import { MarkerVisualUtils } from './markerVisualUtils.js';

const DEFAULT_ATTRACTION_MARKER_SIZE = 32;
const LIMITED_VIEWING_MARKER_CLASS = 'marker-has-limited-viewing';
const CLOSED_RESTROOM_ICON_TOKEN = 'closed';
const FIRST_AID_AND_FAMILY_CENTER_TYPE = 'First Aid & Family Center';

const GENERIC_ICON_PATHS = Object.freeze({
   pavilion: '/images/icons/pavilion/pavilion-open.png',
   restroom: '/images/icons/restroom/restroom-open.png',
   transportationStation: '/images/icons/zoomobile-station/zoomobile-station.png',
   guardiansTalk: '/images/icons/guardians-talk/guardians-talk.png',
   wildEncounter: '/images/icons/wild-encounter/wild-encounter.png',
   defibrillator: '/images/icons/defibrillator/defibrillator.png',
   emergencyIntercom: '/images/icons/emergency-intercom/emergency-intercom.png',
   picnicSite: '/images/icons/picnic-site/picnic-site.png',
});

const MARKER_CLASS_BY_TYPE = Object.freeze({
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

const ZOOMOBILE_ROUTE_COLORS = Object.freeze({
   winter: '#003366',
   default: '#556B2F',
});

const ATTRACTION_MARKER_SCALE_OVERRIDES = Object.freeze({
   'Greenhouse': 2.5,
   'Wildlife Health & Science Centre': 2.5,
   'Splash Island': 2.5,
   'Gorilla Climb Ropes Course': 1.35,
   'TundraAir Ride': 2.0,
   'Conservation Carousel': 2.5,
   'Zoomobile': 2.0,
});

function shouldShowLimitedViewingIndicator(animal) {
   return Boolean(
      !animal?.off_display_message
      && (
         (animal?.has_limited_viewing_schedule && animal?.limited_viewing_message)
         || animal?.viewing_alert_messages?.length
      )
   );
}

function shouldShowRestroomAlertIndicator(restroom) {
   return Boolean(
      !restroom?.is_closed
      && restroom?.has_alert
      && restroom?.alert_message
   );
}

function applyAttractionMarkerSize(markerEl, attractionName) {
   const scale = ATTRACTION_MARKER_SCALE_OVERRIDES[attractionName];

   if (!scale) return;

   const size = Math.round(DEFAULT_ATTRACTION_MARKER_SIZE * scale);
   markerEl.style.width = `${size}px`;
   markerEl.style.height = `${size}px`;
}

function applyOptionalSize(markerEl, item, applySize) {
   if (typeof applySize === 'function') {
      applySize(markerEl, item);
   }
}

function createGenericIconMarkerRenderer(type) {
   return (markerEl, items) => {
      MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE[type]);
      MarkerVisualUtils.applyGenericIcon(markerEl, GENERIC_ICON_PATHS[type], items.length);
   };
}

function createLikelihoodIconMarkerRenderer({
   type,
   getIconUrl,
   applySize = null,
   getLikelihood = item => item?.likelihood,
} = {}) {
   return (markerEl, items) => {
      const item = items[0];
      const count = items.length;

      MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE[type]);
      applyOptionalSize(markerEl, item, applySize);

      const { colour, iconToken } = MarkerVisualUtils.getLikelihoodVisual(getLikelihood(item));

      if (count > 1) {
         MarkerVisualUtils.applyCountMarker(markerEl, count, colour);
         return;
      }

      MarkerVisualUtils.applyBackgroundImage(markerEl, getIconUrl(item, iconToken));
   };
}

function renderAnimalMarker(markerEl, items) {
   const animal = items[0];
   const count = items.length;
   const { colour } = MarkerVisualUtils.getLikelihoodVisual(animal?.likelihood);
   const colourForUrl = String(colour || '').replace('#', '');

   if (count > 1) {
      MarkerVisualUtils.applyCountMarker(markerEl, count, colour);
   } else {
      MarkerVisualUtils.applyBackgroundImage(
         markerEl,
         getAnimalIconUrl(animal?.exhibit, animal?.species, colourForUrl),
         colour
      );
   }

   if (shouldShowLimitedViewingIndicator(animal)) {
      MarkerVisualUtils.applyMarkerClass(markerEl, LIMITED_VIEWING_MARKER_CLASS);
   }
}

function renderRestroomMarker(markerEl, items) {
   const restroom = items[0];
   const count = items.length;
   const likelihood = restroom?.is_closed ? 0 : 100;
   const { colour, iconToken } = MarkerVisualUtils.getLikelihoodVisual(likelihood);

   MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.restroom);

   if (count > 1) {
      MarkerVisualUtils.applyCountMarker(markerEl, count, colour);
   } else {
      MarkerVisualUtils.applyBackgroundImage(
         markerEl,
         getRestroomIconUrl(
            restroom?.is_closed ? CLOSED_RESTROOM_ICON_TOKEN : iconToken
         )
      );
   }

   if (items.some(shouldShowRestroomAlertIndicator)) {
      MarkerVisualUtils.applyMarkerClass(markerEl, LIMITED_VIEWING_MARKER_CLASS);
   }
}

function renderTransportationRouteMarker(markerEl, items) {
   const routeType = items[0]?.route_type;
   const routeColor = ZOOMOBILE_ROUTE_COLORS[routeType]
      || ZOOMOBILE_ROUTE_COLORS.default;

   markerEl.style.backgroundColor = routeColor;
   MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.transportationRouteMarker);
}

function renderDrinkingFountainMarker(markerEl, items) {
   const drinkingFountain = items[0];
   const count = items.length;
   const likelihood = Number.isFinite(Number(drinkingFountain?.likelihood))
      ? Number(drinkingFountain.likelihood) * 100
      : (drinkingFountain?.is_closed ? 0 : 100);
   const { colour, iconToken } = MarkerVisualUtils.getLikelihoodVisual(likelihood);

   MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.drinkingFountain);

   if (count > 1) {
      MarkerVisualUtils.applyCountMarker(markerEl, count, colour);
      return;
   }

   MarkerVisualUtils.applyBackgroundImage(
      markerEl,
      getDrinkingFountainIconUrl(iconToken)
   );
}

function renderGuestServiceMarker(markerEl, items) {
   const guestService = items[0];
   const serviceType = String(guestService?.service_type || '').trim();

   MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.guestService);

   if (serviceType === FIRST_AID_AND_FAMILY_CENTER_TYPE) {
      MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.firstAidGuestService);
   }

   if (items.length > 1) {
      MarkerVisualUtils.applyCountMarker(markerEl, items.length);
      return;
   }

   MarkerVisualUtils.applyBackgroundImage(
      markerEl,
      getGuestServiceIconUrl(serviceType)
   );
}

function renderEventSiteMarker(markerEl, items) {
   const eventSite = items[0];

   MarkerVisualUtils.applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.eventSite);

   if (items.length > 1) {
      MarkerVisualUtils.applyCountMarker(markerEl, items.length);
      return;
   }

   MarkerVisualUtils.applyBackgroundImage(
      markerEl,
      getEventSiteIconUrl(eventSite?.name)
   );
}

const attractionMarkerRenderer = createLikelihoodIconMarkerRenderer({
   type: 'attraction',
   getIconUrl: (attraction, iconToken) => getAttractionIconUrl(
      attraction?.name,
      iconToken
   ),
   applySize: (markerEl, attraction) => applyAttractionMarkerSize(
      markerEl,
      attraction?.name
   ),
});

const MARKER_TYPE_RENDERERS = {
   animal: renderAnimalMarker,
   pavilion: createGenericIconMarkerRenderer('pavilion'),
   restaurant: createLikelihoodIconMarkerRenderer({
      type: 'restaurant',
      getIconUrl: (_, iconToken) => getRestaurantIconUrl(iconToken),
   }),
   restroom: renderRestroomMarker,
   giftShop: createLikelihoodIconMarkerRenderer({
      type: 'giftShop',
      getIconUrl: (_, iconToken) => getGiftShopIconUrl(iconToken),
   }),
   attraction: attractionMarkerRenderer,
   transportation: attractionMarkerRenderer,
   transportationStation: createGenericIconMarkerRenderer('transportationStation'),
   transportationRouteMarker: renderTransportationRouteMarker,
   guardiansTalk: createGenericIconMarkerRenderer('guardiansTalk'),
   wildEncounter: createGenericIconMarkerRenderer('wildEncounter'),
   drinkingFountain: renderDrinkingFountainMarker,
   defibrillator: createGenericIconMarkerRenderer('defibrillator'),
   emergencyIntercom: createGenericIconMarkerRenderer('emergencyIntercom'),
   guestService: renderGuestServiceMarker,
   picnicSite: createGenericIconMarkerRenderer('picnicSite'),
   eventSite: renderEventSiteMarker,
};

export function renderMarkerByType(markerEl, items) {
   const type = String(items?.[0]?.type || '');
   const renderer = MARKER_TYPE_RENDERERS[type];

   if (!renderer) {
      return false;
   }

   renderer(markerEl, items);
   return true;
}

export function renderAnimalIcon(markerEl, animal) {
   renderAnimalMarker(markerEl, [animal]);
}
