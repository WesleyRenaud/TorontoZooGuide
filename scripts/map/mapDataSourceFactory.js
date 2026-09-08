import { MapClient } from '../api/mapClient.js';
import { ItemType } from '../shared/enums/itemType.js';
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
         [ItemType.ANIMAL]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.ANIMAL,
            MapClient.getVisibleAnimals,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               temp: ctx.temp,
               includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
               speciesToInclude: ctx.speciesToInclude,
               animalsToInclude: ctx.animalsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         [ItemType.PAVILION]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.PAVILION,
            MapClient.getPavilions
         ),

         [ItemType.RESTAURANT]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.RESTAURANT,
            MapClient.getRestaurants,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestaurants: ctx.includeClosedRestaurants,
               restaurantsToInclude: ctx.restaurantsToInclude,
            })
         ),

         [ItemType.RESTROOM]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.RESTROOM,
            MapClient.getRestrooms,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedRestrooms: ctx.includeClosedRestrooms,
            })
         ),

         [ItemType.GIFT_SHOP]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.GIFT_SHOP,
            MapClient.getGiftShops,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedGiftShops: ctx.includeClosedGiftShops,
               giftShopsToInclude: ctx.giftShopsToInclude,
            })
         ),

         [ItemType.ATTRACTION]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.ATTRACTION,
            MapClient.getAttractions,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               includeClosedAttractions: ctx.includeClosedAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         [ItemType.TRANSPORTATION_ROUTE]: TransportationRouteProvider.createTransportationRouteSource(store, {
            fetchTransportationRoute: MapClient.getTransportationRoute,
            hideRouteLayers: TransportationRouteFragment.hideTransportationRouteLayers,
            showRouteLayer: TransportationRouteFragment.showTransportationRouteLayer,
         }),

         [ItemType.GUARDIANS_TALK]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.GUARDIANS_TALK,
            MapClient.getGuardiansTalks,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               guardiansTalksToInclude: ctx.guardiansTalksToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         [ItemType.WILD_ENCOUNTER]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.WILD_ENCOUNTER,
            MapClient.getWildEncounters,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx, {
               wildEncountersToInclude: ctx.wildEncountersToInclude,
               itineraryMode: ctx.itineraryMode,
            })
         ),

         [ItemType.DRINKING_FOUNTAIN]: MapDataSourceFactory.createTypedDynamicApiSource(
            store,
            ItemType.DRINKING_FOUNTAIN,
            MapClient.getDrinkingFountains,
            (ctx) => MapDataSourceFactory.buildDatePayload(ctx)
         ),

         [ItemType.DEFIBRILLATOR]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.DEFIBRILLATOR,
            MapClient.getDefibrillators
         ),

         [ItemType.EMERGENCY_INTERCOM]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.EMERGENCY_INTERCOM,
            MapClient.getEmergencyIntercoms
         ),

         [ItemType.GUEST_SERVICE]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.GUEST_SERVICE,
            MapClient.getGuestServices
         ),

         [ItemType.PICNIC_SITE]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.PICNIC_SITE,
            MapClient.getPicnicSites
         ),

         [ItemType.EVENT_SITE]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.EVENT_SITE,
            MapClient.getEventSites
         ),

         [ItemType.EXHIBIT]: MapDataSourceFactory.createTypedStaticApiSource(
            store,
            ItemType.EXHIBIT,
            MapClient.getExhibits
         ),

         closedExhibit: MapDataSourceFactory.createClosedExhibitSource(),
      };
   }
}
