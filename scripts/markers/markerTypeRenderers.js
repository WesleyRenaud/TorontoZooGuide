import {
   getAnimalIconUrl,
   getAttractionIconUrl,
   getGiftShopIconUrl,
   getRestaurantIconUrl,
   getRestroomIconUrl,
} from '../assets/iconUrls.js';
import {
   applyBackgroundImage,
   applyCountMarker,
   applyGenericIcon,
   applyMarkerClass,
   getLikelihoodVisual,
} from './markerVisualUtils.js';

const DEFAULT_ATTRACTION_MARKER_SIZE = 32;
const LIMITED_VIEWING_MARKER_CLASS = 'marker-has-limited-viewing';
const CLOSED_RESTROOM_ICON_TOKEN = 'closed';

const GENERIC_ICON_PATHS = Object.freeze({
   pavilion: '/images/generic-icons/pavilion-open.png',
   restroom: '/images/generic-icons/restroom-open.png',
   zoomobileStation: '/images/generic-icons/zoomobile-station.png',
   guardiansTalk: '/images/generic-icons/guardians-talk.png',
   wildEncounter: '/images/generic-icons/wild-encounter.png',
});

const MARKER_CLASS_BY_TYPE = Object.freeze({
   restaurant: 'marker-restaurant',
   restroom: 'marker-restroom',
   giftShop: 'marker-gift-shop',
   attraction: 'marker-attraction',
   zoomobileStation: 'marker-zoomobile-station',
   zoomobileRouteMarker: 'marker-zoomobile-route-marker',
   guardiansTalk: 'marker-guardians-talk',
   wildEncounter: 'marker-wild-encounter',
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
         || (animal?.has_viewing_alert && animal?.viewing_alert_message)
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
      applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE[type]);
      applyGenericIcon(markerEl, GENERIC_ICON_PATHS[type], items.length);
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

      applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE[type]);
      applyOptionalSize(markerEl, item, applySize);

      const { colour, iconToken } = getLikelihoodVisual(getLikelihood(item));

      if (count > 1) {
         applyCountMarker(markerEl, count, colour);
         return;
      }

      applyBackgroundImage(markerEl, getIconUrl(item, iconToken));
   };
}

function renderAnimalMarker(markerEl, items) {
   const animal = items[0];
   const count = items.length;
   const { colour } = getLikelihoodVisual(animal?.likelihood);
   const colourForUrl = String(colour || '').replace('#', '');

   if (count > 1) {
      applyCountMarker(markerEl, count, colour);
   } else {
      applyBackgroundImage(
         markerEl,
         getAnimalIconUrl(animal?.exhibit, animal?.species, colourForUrl),
         colour
      );
   }

   if (shouldShowLimitedViewingIndicator(animal)) {
      applyMarkerClass(markerEl, LIMITED_VIEWING_MARKER_CLASS);
   }
}

function renderRestroomMarker(markerEl, items) {
   const restroom = items[0];
   const count = items.length;
   const likelihood = restroom?.is_closed ? 0 : 100;
   const { colour, iconToken } = getLikelihoodVisual(likelihood);

   applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.restroom);

   if (count > 1) {
      applyCountMarker(markerEl, count, colour);
   } else {
      applyBackgroundImage(
         markerEl,
         getRestroomIconUrl(
            restroom?.is_closed ? CLOSED_RESTROOM_ICON_TOKEN : iconToken
         )
      );
   }

   if (items.some(shouldShowRestroomAlertIndicator)) {
      applyMarkerClass(markerEl, LIMITED_VIEWING_MARKER_CLASS);
   }
}

function renderZoomobileRouteMarker(markerEl, items) {
   const routeType = items[0]?.route_type;
   const routeColor = ZOOMOBILE_ROUTE_COLORS[routeType]
      || ZOOMOBILE_ROUTE_COLORS.default;

   markerEl.style.backgroundColor = routeColor;
   applyMarkerClass(markerEl, MARKER_CLASS_BY_TYPE.zoomobileRouteMarker);
}

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
   attraction: createLikelihoodIconMarkerRenderer({
      type: 'attraction',
      getIconUrl: (attraction, iconToken) => getAttractionIconUrl(
         attraction?.name,
         iconToken
      ),
      applySize: (markerEl, attraction) => applyAttractionMarkerSize(
         markerEl,
         attraction?.name
      ),
   }),
   zoomobileStation: createGenericIconMarkerRenderer('zoomobileStation'),
   zoomobileRouteMarker: renderZoomobileRouteMarker,
   guardiansTalk: createGenericIconMarkerRenderer('guardiansTalk'),
   wildEncounter: createGenericIconMarkerRenderer('wildEncounter'),
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
