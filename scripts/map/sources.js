import {
   getAttractions,
   getClosedExhibits,
   getDefibrillators,
   getDrinkingFountains,
   getEmergencyIntercoms,
   getEventSites,
   getExhibits,
   getGiftShops,
   getGuardiansTalks,
   getGuestServices,
   getPavilions,
   getPicnicSites,
   getRestaurants,
   getRestrooms,
   getVisibleAnimals,
   getWildEncounters,
   getZoomobileRoute,
} from '../api/mapApi.js';
import {
   createDynamicTypedSource,
   createStaticTypedSource,
   normalizeTypedRows,
} from './sourceHelpers.js';
import {
   hideZoomobileRouteLayers,
   showZoomobileRouteLayer,
} from './zoomobileRouteOverlay.js';
import { createZoomobileRouteSource } from './zoomobileRouteSource.js';

function createNoCacheSource(fetchRows) {
   return {
      fetch: fetchRows,
      cachePolicy: 'no-cache',
   };
}

function buildDatePayload(ctx, extra = {}) {
   return {
      month: ctx.month,
      day: ctx.day,
      ...extra,
   };
}

function createTypedDynamicApiSource(store, type, fetchRows, buildPayload) {
   return createDynamicTypedSource(store, type, async (ctx) => {
      const rows = await fetchRows(buildPayload(ctx));
      return normalizeTypedRows(rows, type);
   });
}

function createTypedStaticApiSource(store, type, fetchRows) {
   return createStaticTypedSource(store, type, async () => (
      normalizeTypedRows(await fetchRows(), type)
   ));
}

function createClosedExhibitSource() {
   return createNoCacheSource(async (ctx) => {
      return await getClosedExhibits({
         month: ctx.month,
         day: ctx.day,
         dayOfWeek: ctx.dayOfWeek,
      });
   });
}

export function createDataSources(store) {
   return {
      animal: createTypedDynamicApiSource(
         store,
         'animal',
         getVisibleAnimals,
         (ctx) => buildDatePayload(ctx, {
            temp: ctx.temp,
            includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
            speciesToInclude: ctx.speciesToInclude,
            animalsToInclude: ctx.animalsToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      pavilion: createTypedStaticApiSource(store, 'pavilion', getPavilions),

      restaurant: createTypedDynamicApiSource(
         store,
         'restaurant',
         getRestaurants,
         (ctx) => buildDatePayload(ctx, {
            includeClosedRestaurants: ctx.includeClosedRestaurants,
            restaurantsToInclude: ctx.restaurantsToInclude,
         })
      ),

      restroom: createTypedDynamicApiSource(
         store,
         'restroom',
         getRestrooms,
         (ctx) => buildDatePayload(ctx, {
            includeClosedRestrooms: ctx.includeClosedRestrooms,
         })
      ),

      giftShop: createTypedDynamicApiSource(
         store,
         'giftShop',
         getGiftShops,
         (ctx) => buildDatePayload(ctx, {
            includeClosedGiftShops: ctx.includeClosedGiftShops,
            giftShopsToInclude: ctx.giftShopsToInclude,
         })
      ),

      attraction: createTypedDynamicApiSource(
         store,
         'attraction',
         getAttractions,
         (ctx) => buildDatePayload(ctx, {
            includeClosedAttractions: ctx.includeClosedAttractions,
            attractionsToInclude: ctx.attractionsToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      zoomobileRoute: createZoomobileRouteSource(store, {
         fetchZoomobileRoute: getZoomobileRoute,
         hideRouteLayers: hideZoomobileRouteLayers,
         showRouteLayer: showZoomobileRouteLayer,
      }),

      guardiansTalk: createTypedDynamicApiSource(
         store,
         'guardiansTalk',
         getGuardiansTalks,
         (ctx) => buildDatePayload(ctx, {
            guardiansTalksToInclude: ctx.guardiansTalksToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      wildEncounter: createTypedDynamicApiSource(
         store,
         'wildEncounter',
         getWildEncounters,
         (ctx) => buildDatePayload(ctx, {
            wildEncountersToInclude: ctx.wildEncountersToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      drinkingFountain: createTypedDynamicApiSource(
         store,
         'drinkingFountain',
         getDrinkingFountains,
         (ctx) => buildDatePayload(ctx)
      ),

      defibrillator: createTypedStaticApiSource(store, 'defibrillator', getDefibrillators),

      emergencyIntercom: createTypedStaticApiSource(
         store,
         'emergencyIntercom',
         getEmergencyIntercoms
      ),

      guestService: createTypedStaticApiSource(
         store,
         'guestService',
         getGuestServices
      ),

      picnicSite: createTypedStaticApiSource(
         store,
         'picnicSite',
         getPicnicSites
      ),

      eventSite: createTypedStaticApiSource(
         store,
         'eventSite',
         getEventSites
      ),

      exhibit: createTypedStaticApiSource(store, 'exhibit', getExhibits),

      closedExhibit: createClosedExhibitSource(),
   };
}
