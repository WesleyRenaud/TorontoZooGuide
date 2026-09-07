import { MapApi } from '../api/mapApi.js';
import { SourceHelpers } from './sourceHelpers.js';
import { TransportationRouteOverlay } from './transportationRouteOverlay.js';
import { TransportationRouteSource } from './transportationRouteSource.js';

export class MapDataSourceFactory {
   static createNoCacheSource(fetchRows) {
      return {
         fetch: fetchRows,
         cachePolicy: 'no-cache',
      };
   }

   static buildDatePayload(ctx, extra = {}) {
      return {
         month: ctx.month,
         day: ctx.day,
         year: ctx.year,
         ...extra,
      };
   }

   static createTypedDynamicApiSource(store, type, fetchRows, buildPayload) {
      return SourceHelpers.createDynamicTypedSource(store, type, async (ctx) => {
         const rows = await fetchRows(buildPayload(ctx));
         return SourceHelpers.normalizeTypedRows(rows, type);
      });
   }

   static createTypedStaticApiSource(store, type, fetchRows) {
      return SourceHelpers.createStaticTypedSource(store, type, async () => (
         SourceHelpers.normalizeTypedRows(await fetchRows(), type)
      ));
   }

   static createClosedExhibitSource() {
      return MapDataSourceFactory.createNoCacheSource(async (ctx) => {
         return await MapApi.getClosedExhibits({
            month: ctx.month,
            day: ctx.day,
            year: ctx.year,
            dayOfWeek: ctx.dayOfWeek,
         });
      });
   }

   static createDataSources(store) {
      return {
         animal: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'animal',
            MapApi.getVisibleAnimals,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               temp: ctx.temp,
               includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
               speciesToInclude: ctx.speciesToInclude,
               animalsToInclude: ctx.animalsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         pavilion: MapDataSourceFactory.createTypedStaticApiSource(store, 'pavilion', MapApi.getPavilions),

         restaurant: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'restaurant',
            MapApi.getRestaurants,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestaurants: ctx.includeClosedRestaurants,
               restaurantsToInclude: ctx.restaurantsToInclude,
            })
         ),

         restroom: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'restroom',
            MapApi.getRestrooms,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestrooms: ctx.includeClosedRestrooms,
            })
         ),

         giftShop: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'giftShop',
            MapApi.getGiftShops,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedGiftShops: ctx.includeClosedGiftShops,
               giftShopsToInclude: ctx.giftShopsToInclude,
            })
         ),

         attraction: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'attraction',
            MapApi.getAttractions,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedAttractions: ctx.includeClosedAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         transportationRoute: TransportationRouteSource.createTransportationRouteSource(store, {
            fetchTransportationRoute: MapApi.getTransportationRoute,
            hideRouteLayers: TransportationRouteOverlay.hideTransportationRouteLayers,
            showRouteLayer: TransportationRouteOverlay.showTransportationRouteLayer,
         }),

         guardiansTalk: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'guardiansTalk',
            MapApi.getGuardiansTalks,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               guardiansTalksToInclude: ctx.guardiansTalksToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         wildEncounter: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'wildEncounter',
            MapApi.getWildEncounters,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               wildEncountersToInclude: ctx.wildEncountersToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         drinkingFountain: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'drinkingFountain',
            MapApi.getDrinkingFountains,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx)
         ),

         defibrillator: MapDataSourceFactory.createTypedStaticApiSource(store, 'defibrillator', MapApi.getDefibrillators),

         emergencyIntercom: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'emergencyIntercom',
            MapApi.getEmergencyIntercoms
         ),

         guestService: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'guestService',
            MapApi.getGuestServices
         ),

         picnicSite: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'picnicSite',
            MapApi.getPicnicSites
         ),

         eventSite: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'eventSite',
            MapApi.getEventSites
         ),

         exhibit: MapDataSourceFactory.createTypedStaticApiSource(store, 'exhibit', MapApi.getExhibits),

         closedExhibit: MapDataSourceFactory.createClosedExhibitSource(),
      };
   }
}
