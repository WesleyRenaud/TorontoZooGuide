import {
   getAnimalIconUrl,
   getAttractionIconUrl,
   getGiftShopIconUrl,
   getRestaurantIconUrl,
} from '../assets/iconUrls.js';
import {
   applyBackgroundImage,
   applyCountMarker,
   applyGenericIcon,
   applyMarkerClass,
   getLikelihoodVisual,
} from './markerVisualUtils.js';

const DEFAULT_ATTRACTION_MARKER_SIZE = 32;

const ATTRACTION_MARKER_SCALE_OVERRIDES = {
   'Greenhouse': 2.5,
   'Wildlife Health & Science Centre': 2.5,
   'Splash Island': 2.5,
   'Gorilla Climb Ropes Course': 1.35,
   'TundraAir Ride': 2.0,
   'Conservation Carousel': 2.5,
   'Zoomobile': 2.0,
};

function shouldShowLimitedViewingIndicator(animal) {
   return Boolean(
      !animal?.off_display_message
      && (
         (animal?.has_limited_viewing_schedule && animal?.limited_viewing_message)
         || (animal?.has_viewing_alert && animal?.viewing_alert_message)
      )
   );
}

function applyAttractionMarkerSize(markerEl, attractionName) {
   const scale = ATTRACTION_MARKER_SCALE_OVERRIDES[attractionName];

   if (!scale) return;

   const size = Math.round(DEFAULT_ATTRACTION_MARKER_SIZE * scale);
   markerEl.style.width = `${size}px`;
   markerEl.style.height = `${size}px`;
}

function renderLikelihoodIconMarker(
   markerEl,
   item,
   count,
   { className, getIconUrl, applySize }
) {
   applyMarkerClass(markerEl, className);

   if (typeof applySize === 'function') {
      applySize(markerEl, item);
   }

   const { colour, iconToken } = getLikelihoodVisual(item?.likelihood);

   if (count > 1) {
      applyCountMarker(markerEl, count, colour);
      return;
   }

   applyBackgroundImage(markerEl, getIconUrl(item, iconToken));
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
      applyMarkerClass(markerEl, 'marker-has-limited-viewing');
   }
}

function renderPavilionMarker(markerEl, items) {
   applyGenericIcon(markerEl, '/images/generic-icons/pavilion-open.png', items.length);
}

function renderRestaurantMarker(markerEl, items) {
   renderLikelihoodIconMarker(markerEl, items[0], items.length, {
      className: 'marker-restaurant',
      getIconUrl: (_, iconToken) => getRestaurantIconUrl(iconToken),
   });
}

function renderRestroomMarker(markerEl, items) {
   applyMarkerClass(markerEl, 'marker-restroom');
   applyGenericIcon(markerEl, '/images/generic-icons/restroom-open.png', items.length);
}

function renderGiftShopMarker(markerEl, items) {
   renderLikelihoodIconMarker(markerEl, items[0], items.length, {
      className: 'marker-gift-shop',
      getIconUrl: (_, iconToken) => getGiftShopIconUrl(iconToken),
   });
}

function renderAttractionMarker(markerEl, items) {
   renderLikelihoodIconMarker(markerEl, items[0], items.length, {
      className: 'marker-attraction',
      getIconUrl: (attraction, iconToken) => getAttractionIconUrl(
         attraction?.name,
         iconToken
      ),
      applySize: (el, attraction) => applyAttractionMarkerSize(el, attraction?.name),
   });
}

function renderZoomobileStationMarker(markerEl, items) {
   applyMarkerClass(markerEl, 'marker-zoomobile-station');
   applyGenericIcon(markerEl, '/images/generic-icons/zoomobile-station.png', items.length);
}

function renderZoomobileRouteMarker(markerEl, items) {
   const routeType = items[0]?.route_type;

   markerEl.style.backgroundColor = routeType === 'winter'
      ? '#003366'
      : '#556B2F';

   applyMarkerClass(markerEl, 'marker-zoomobile-route-marker');
}

function renderGuardiansTalkMarker(markerEl, items) {
   applyMarkerClass(markerEl, 'marker-guardians-talk');
   applyGenericIcon(markerEl, '/images/generic-icons/guardians-talk.png', items.length);
}

function renderWildEncounterMarker(markerEl, items) {
   applyMarkerClass(markerEl, 'marker-wild-encounter');
   applyGenericIcon(markerEl, '/images/generic-icons/wild-encounter.png', items.length);
}

const MARKER_TYPE_RENDERERS = {
   animal: renderAnimalMarker,
   pavilion: renderPavilionMarker,
   restaurant: renderRestaurantMarker,
   restroom: renderRestroomMarker,
   giftShop: renderGiftShopMarker,
   attraction: renderAttractionMarker,
   zoomobileStation: renderZoomobileStationMarker,
   zoomobileRouteMarker: renderZoomobileRouteMarker,
   guardiansTalk: renderGuardiansTalkMarker,
   wildEncounter: renderWildEncounterMarker,
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
