import { MapClient } from '../api/mapClient.js';
import { SourceHelper } from './sourceHelper.js';
import { TransportationRouteFragment } from './transportationRouteFragment.js';
import { TransportationRouteProvider } from './transportationRouteProvider.js';

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
      return SourceHelper.createDynamicTypedSource(store, type, async (ctx) => {
         const rows = await fetchRows(buildPayload(ctx));
         return SourceHelper.normalizeTypedRows(rows, type);
      });
   }

   static createTypedStaticApiSource(store, type, fetchRows) {
      return SourceHelper.createStaticTypedSource(store, type, async () => (
         SourceHelper.normalizeTypedRows(await fetchRows(), type)
      ));
   }

   static createClosedExhibitSource() {
      return MapDataSourceFactory.createNoCacheSource(async (ctx) => {
         return await MapClient.getClosedExhibits({
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
            MapClient.getVisibleAnimals,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               temp: ctx.temp,
               includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
               speciesToInclude: ctx.speciesToInclude,
               animalsToInclude: ctx.animalsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         pavilion: MapDataSourceFactory.createTypedStaticApiSource(store, 'pavilion', MapClient.getPavilions),

         restaurant: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'restaurant',
            MapClient.getRestaurants,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestaurants: ctx.includeClosedRestaurants,
               restaurantsToInclude: ctx.restaurantsToInclude,
            })
         ),

         restroom: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'restroom',
            MapClient.getRestrooms,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestrooms: ctx.includeClosedRestrooms,
            })
         ),

         giftShop: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'giftShop',
            MapClient.getGiftShops,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedGiftShops: ctx.includeClosedGiftShops,
               giftShopsToInclude: ctx.giftShopsToInclude,
            })
         ),

         attraction: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'attraction',
            MapClient.getAttractions,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedAttractions: ctx.includeClosedAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         transportationRoute: TransportationRouteProvider.createTransportationRouteSource(store, {
            fetchTransportationRoute: MapClient.getTransportationRoute,
            hideRouteLayers: TransportationRouteFragment.hideTransportationRouteLayers,
            showRouteLayer: TransportationRouteFragment.showTransportationRouteLayer,
         }),

         guardiansTalk: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'guardiansTalk',
            MapClient.getGuardiansTalks,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               guardiansTalksToInclude: ctx.guardiansTalksToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         wildEncounter: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'wildEncounter',
            MapClient.getWildEncounters,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               wildEncountersToInclude: ctx.wildEncountersToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         drinkingFountain: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            'drinkingFountain',
            MapClient.getDrinkingFountains,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx)
         ),

         defibrillator: MapDataSourceFactory.createTypedStaticApiSource(store, 'defibrillator', MapClient.getDefibrillators),

         emergencyIntercom: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'emergencyIntercom',
            MapClient.getEmergencyIntercoms
         ),

         guestService: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'guestService',
            MapClient.getGuestServices
         ),

         picnicSite: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'picnicSite',
            MapClient.getPicnicSites
         ),

         eventSite: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            'eventSite',
            MapClient.getEventSites
         ),

         exhibit: MapDataSourceFactory.createTypedStaticApiSource(store, 'exhibit', MapClient.getExhibits),

         closedExhibit: MapDataSourceFactory.createClosedExhibitSource(),
      };
   }
}
