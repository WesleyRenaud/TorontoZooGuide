import {
   getAttractions,
   getClosedExhibits,
   getExhibits,
   getGiftShops,
   getGuardiansTalks,
   getPavilions,
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
   setSourceRows,
} from './sourceHelpers.js';
import {
   hideZoomobileRouteLayers,
   showZoomobileRouteLayer,
} from './zoomobileRouteOverlay.js';

export function createDataSources(store) {
   return {
      animal: createDynamicTypedSource(store, 'animal', async (ctx) => {
         const animals = await getVisibleAnimals({
            month: ctx.month,
            day: ctx.day,
            temp: ctx.temp,
            includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
            speciesToInclude: ctx.speciesToInclude,
            animalsToInclude: ctx.animalsToInclude,
            itineraryMode: ctx.itineraryMode,
         });

         return normalizeTypedRows(animals, 'animal');
      }),

      pavilion: createStaticTypedSource(store, 'pavilion', async () => {
         return normalizeTypedRows(await getPavilions(), 'pavilion');
      }),

      restaurant: createDynamicTypedSource(store, 'restaurant', async (ctx) => {
         const restaurants = await getRestaurants({
            month: ctx.month,
            day: ctx.day,
            includeClosedRestaurants: ctx.includeClosedRestaurants,
            restaurantsToInclude: ctx.restaurantsToInclude,
         });

         return normalizeTypedRows(restaurants, 'restaurant');
      }),

      restroom: createStaticTypedSource(store, 'restroom', async () => {
         return normalizeTypedRows(await getRestrooms(), 'restroom');
      }),

      giftShop: createDynamicTypedSource(store, 'giftShop', async (ctx) => {
         const giftShops = await getGiftShops({
            month: ctx.month,
            day: ctx.day,
            includeClosedGiftShops: ctx.includeClosedGiftShops,
            giftShopsToInclude: ctx.giftShopsToInclude,
         });

         return normalizeTypedRows(giftShops, 'giftShop');
      }),

      attraction: createDynamicTypedSource(store, 'attraction', async (ctx) => {
         const attractions = await getAttractions({
            month: ctx.month,
            day: ctx.day,
            includeClosedAttractions: ctx.includeClosedAttractions,
            attractionsToInclude: ctx.attractionsToInclude,
            itineraryMode: ctx.itineraryMode,
         });

         return normalizeTypedRows(attractions, 'attraction');
      }),

      zoomobileRoute: {
         fetch: async (ctx) => {
            hideZoomobileRouteLayers();

            if (ctx.zoomobileRoute === 'none') {
               setSourceRows(store, 'zoomobileStation', []);
               setSourceRows(store, 'zoomobileRoute', []);
               return [];
            }

            const {
               route,
               zoomobileStations,
            } = await getZoomobileRoute({
               zoomobileRoute: ctx.zoomobileRoute,
               month: ctx.month,
               day: ctx.day,
               zoomobileStationsToInclude: ctx.zoomobileStationsToInclude,
            });

            showZoomobileRouteLayer(route);

            const stations = normalizeTypedRows(
               zoomobileStations,
               'zoomobileStation'
            );

            setSourceRows(store, 'zoomobileStation', stations);
            setSourceRows(store, 'zoomobileRoute', []);

            return stations;
         },
         cachePolicy: 'no-cache',
      },

      guardiansTalk: createDynamicTypedSource(store, 'guardiansTalk', async (ctx) => {
         const guardiansTalks = await getGuardiansTalks({
            month: ctx.month,
            day: ctx.day,
            guardiansTalksToInclude: ctx.guardiansTalksToInclude,
            itineraryMode: ctx.itineraryMode,
         });

         return normalizeTypedRows(guardiansTalks, 'guardiansTalk');
      }),

      wildEncounter: createDynamicTypedSource(store, 'wildEncounter', async (ctx) => {
         const wildEncounters = await getWildEncounters({
            month: ctx.month,
            day: ctx.day,
            wildEncountersToInclude: ctx.wildEncountersToInclude,
            itineraryMode: ctx.itineraryMode,
         });

         return normalizeTypedRows(wildEncounters, 'wildEncounter');
      }),

      exhibit: createStaticTypedSource(store, 'exhibit', async () => {
         return normalizeTypedRows(await getExhibits(), 'exhibit');
      }),

      closedExhibit: {
         fetch: async (ctx) => {
            return await getClosedExhibits({
               month: ctx.month,
               day: ctx.day,
               dayOfWeek: ctx.dayOfWeek,
            });
         },
         cachePolicy: 'no-cache',
      },
   };
}
