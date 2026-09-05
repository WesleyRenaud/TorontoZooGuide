import { MapApi } from '../api/mapApi.js';
import { SourceHelpers } from './sourceHelpers.js';
import {
   hideTransportationRouteLayers,
   showTransportationRouteLayer,
} from './transportationRouteOverlay.js';
import { TransportationRouteSource } from './transportationRouteSource.js';

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
      year: ctx.year,
      ...extra,
   };
}

function createTypedDynamicApiSource(store, type, fetchRows, buildPayload) {
   return SourceHelpers.createDynamicTypedSource(store, type, async (ctx) => {
      const rows = await fetchRows(buildPayload(ctx));
      return SourceHelpers.normalizeTypedRows(rows, type);
   });
}

function createTypedStaticApiSource(store, type, fetchRows) {
   return SourceHelpers.createStaticTypedSource(store, type, async () => (
      SourceHelpers.normalizeTypedRows(await fetchRows(), type)
   ));
}

function createClosedExhibitSource() {
   return createNoCacheSource(async (ctx) => {
      return await MapApi.getClosedExhibits({
         month: ctx.month,
         day: ctx.day,
         year: ctx.year,
         dayOfWeek: ctx.dayOfWeek,
      });
   });
}

export function createDataSources(store) {
   return {
      animal: createTypedDynamicApiSource(
         store,
         'animal',
         MapApi.getVisibleAnimals,
         (ctx) => buildDatePayload(ctx, {
            temp: ctx.temp,
            includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
            speciesToInclude: ctx.speciesToInclude,
            animalsToInclude: ctx.animalsToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      pavilion: createTypedStaticApiSource(store, 'pavilion', MapApi.getPavilions),

      restaurant: createTypedDynamicApiSource(
         store,
         'restaurant',
         MapApi.getRestaurants,
         (ctx) => buildDatePayload(ctx, {
            includeClosedRestaurants: ctx.includeClosedRestaurants,
            restaurantsToInclude: ctx.restaurantsToInclude,
         })
      ),

      restroom: createTypedDynamicApiSource(
         store,
         'restroom',
         MapApi.getRestrooms,
         (ctx) => buildDatePayload(ctx, {
            includeClosedRestrooms: ctx.includeClosedRestrooms,
         })
      ),

      giftShop: createTypedDynamicApiSource(
         store,
         'giftShop',
         MapApi.getGiftShops,
         (ctx) => buildDatePayload(ctx, {
            includeClosedGiftShops: ctx.includeClosedGiftShops,
            giftShopsToInclude: ctx.giftShopsToInclude,
         })
      ),

      attraction: createTypedDynamicApiSource(
         store,
         'attraction',
         MapApi.getAttractions,
         (ctx) => buildDatePayload(ctx, {
            includeClosedAttractions: ctx.includeClosedAttractions,
            attractionsToInclude: ctx.attractionsToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      transportationRoute: TransportationRouteSource.createTransportationRouteSource(store, {
         fetchTransportationRoute: MapApi.getTransportationRoute,
         hideRouteLayers: hideTransportationRouteLayers,
         showRouteLayer: showTransportationRouteLayer,
      }),

      guardiansTalk: createTypedDynamicApiSource(
         store,
         'guardiansTalk',
         MapApi.getGuardiansTalks,
         (ctx) => buildDatePayload(ctx, {
            guardiansTalksToInclude: ctx.guardiansTalksToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      wildEncounter: createTypedDynamicApiSource(
         store,
         'wildEncounter',
         MapApi.getWildEncounters,
         (ctx) => buildDatePayload(ctx, {
            wildEncountersToInclude: ctx.wildEncountersToInclude,
            itineraryMode: ctx.itineraryMode,
         })
      ),

      drinkingFountain: createTypedDynamicApiSource(
         store,
         'drinkingFountain',
         MapApi.getDrinkingFountains,
         (ctx) => buildDatePayload(ctx)
      ),

      defibrillator: createTypedStaticApiSource(store, 'defibrillator', MapApi.getDefibrillators),

      emergencyIntercom: createTypedStaticApiSource(
         store,
         'emergencyIntercom',
         MapApi.getEmergencyIntercoms
      ),

      guestService: createTypedStaticApiSource(
         store,
         'guestService',
         MapApi.getGuestServices
      ),

      picnicSite: createTypedStaticApiSource(
         store,
         'picnicSite',
         MapApi.getPicnicSites
      ),

      eventSite: createTypedStaticApiSource(
         store,
         'eventSite',
         MapApi.getEventSites
      ),

      exhibit: createTypedStaticApiSource(store, 'exhibit', MapApi.getExhibits),

      closedExhibit: createClosedExhibitSource(),
   };
}
