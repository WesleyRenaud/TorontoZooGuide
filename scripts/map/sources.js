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

export function createDataSources(store) {
   return {
      animal: {
         fetch: async (ctx) => {
            const res = await getVisibleAnimals({
               month: ctx.month,
               day: ctx.day,
               temp: ctx.temp,
               includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
               speciesToInclude: ctx.speciesToInclude,
               animalsToInclude: ctx.animalsToInclude,
               itineraryMode: ctx.itineraryMode,
            });

            const animals = res?.animals ?? [];
            const normalized = animals.map(a => ({ ...a, type: 'animal' }));
            store.byType.animal = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      pavilion: {
         fetch: async () => {
            const cache = store.cache.pavilion ?? store.cache.pavilions;

            if (!cache) {
               const res = await getPavilions();
               const rows = res?.pavilions ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'pavilion' }));
               store.byType.pavilion = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.pavilion ?? store.byType.pavilions ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = getPavilions()
               .then(res => {
                  const rows = res?.pavilions ?? res?.results ?? res ?? [];
                  const normalized = rows.map(p => ({ ...p, type: 'pavilion' }));

                  store.byType.pavilion = normalized;
                  cache.loaded = true;
                  cache.inFlight = null;
                  return normalized;
               })
               .catch(err => {
                  cache.inFlight = null;
                  throw err;
               });

            return cache.inFlight;
         },
         cachePolicy: 'static',
      },

      restaurant: {
         fetch: async (ctx) => {
            const res = await getRestaurants({
               month: ctx.month,
               day: ctx.day,
               includeClosedRestaurants: ctx.includeClosedRestaurants,
               restaurantsToInclude: ctx.restaurantsToInclude,
            });

            const rows = res?.restaurants ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'restaurant' }));

            store.byType.restaurant = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      restroom: {
         fetch: async () => {
            const cache = store.cache.restroom ?? store.cache.restrooms;

            if (!cache) {
               const res = await getRestrooms();
               const rows = res?.restrooms ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'restroom' }));
               store.byType.restroom = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.restroom ?? store.byType.restrooms ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = getRestrooms()
               .then(res => {
                  const rows = res?.restrooms ?? res?.results ?? res ?? [];
                  const normalized = rows.map(p => ({ ...p, type: 'restroom' }));

                  store.byType.restroom = normalized;
                  cache.loaded = true;
                  cache.inFlight = null;
                  return normalized;
               })
               .catch(err => {
                  cache.inFlight = null;
                  throw err;
               });

            return cache.inFlight;
         },
         cachePolicy: 'static',
      },

      giftShop: {
         fetch: async (ctx) => {
            const res = await getGiftShops({
               month: ctx.month,
               day: ctx.day,
               includeClosedGiftShops: ctx.includeClosedGiftShops,
               giftShopsToInclude: ctx.giftShopsToInclude,
            });

            const rows = res?.gift_shops ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'giftShop' }));

            store.byType.giftShop = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      attraction: {
         fetch: async (ctx) => {
            const res = await getAttractions({
               month: ctx.month,
               day: ctx.day,
               includeClosedAttractions: ctx.includeClosedAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
               itineraryMode: ctx.itineraryMode,
            });

            const rows = res?.attractions ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'attraction' }));

            store.byType.attraction = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      zoomobileRoute: {
         fetch: async (ctx) => {
            const svgRoot = document.querySelector('#zooMapMount svg');

            const hideAllRouteLayers = () => {
               if (!svgRoot) return;

               svgRoot.querySelector('#zoomobile-route-summer')?.style.setProperty('display', 'none');
               svgRoot.querySelector('#zoomobile-route-winter')?.style.setProperty('display', 'none');
            };

            hideAllRouteLayers();

            if (ctx.zoomobileRoute === 'none') {
               store.byType.zoomobileStation = [];
               store.byType.zoomobileRoute = [];
               return [];
            }

            const res = await getZoomobileRoute({
               zoomobileRoute: ctx.zoomobileRoute,
               month: ctx.month,
               day: ctx.day,
               zoomobileStationsToInclude: ctx.zoomobileStationsToInclude,
            });

            console.log(res);

            const route = String(res?.route || '').trim().toLowerCase();

            if (svgRoot) {
               if (route === 'summer') {
                  svgRoot.querySelector('#zoomobile-route-summer')?.style.setProperty('display', '');
               } else if (route === 'winter') {
                  svgRoot.querySelector('#zoomobile-route-winter')?.style.setProperty('display', '');
               }
            }

            const stations = Array.isArray(res?.zoomobile_stations)
               ? res.zoomobile_stations.map((station) => ({
                  ...station,
                  type: 'zoomobileStation',
               }))
               : [];

            store.byType.zoomobileStation = stations;
            store.byType.zoomobileRoute = [];

            return stations;
         },
         cachePolicy: 'no-cache',
      },

      guardiansTalk: {
         fetch: async (ctx) => {
            const res = await getGuardiansTalks({
               month: ctx.month,
               day: ctx.day,
               guardiansTalksToInclude: ctx.guardiansTalksToInclude,
               itineraryMode: ctx.itineraryMode,
            });

            const rows = res?.guardians_talks ?? res?.talks ?? res?.results ?? res ?? [];
            const normalized = (Array.isArray(rows) ? rows : []).map(t => ({ ...t, type: 'guardiansTalk' }));

            store.byType.guardiansTalk = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      wildEncounter: {
         fetch: async (ctx) => {
            const res = await getWildEncounters({
               month: ctx.month,
               day: ctx.day,
               wildEncountersToInclude: ctx.wildEncountersToInclude,
               itineraryMode: ctx.itineraryMode,
            });

            const rows = res?.wild_encounters ?? res?.results ?? res ?? [];
            const normalized = (Array.isArray(rows) ? rows : []).map(w => ({ ...w, type: 'wildEncounter' }));

            store.byType.wildEncounter = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      exhibit: {
         fetch: async () => {
            const cache = store.cache.exhibit ?? store.cache.exhibits;

            if (!cache) {
               const res = await getExhibits();
               const rows = res?.exhibits ?? res?.results ?? res ?? [];
               const normalized = rows.map(e => ({ ...e, type: 'exhibit' }));
               store.byType.exhibit = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.exhibit ?? store.byType.exhibits ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = getExhibits()
               .then(res => {
                  const rows = res?.exhibits ?? res?.results ?? res ?? [];
                  const normalized = rows.map(e => ({ ...e, type: 'exhibit' }));

                  store.byType.exhibit = normalized;
                  cache.loaded = true;
                  cache.inFlight = null;
                  return normalized;
               })
               .catch(err => {
                  cache.inFlight = null;
                  throw err;
               });

            return cache.inFlight;
         },
         cachePolicy: 'static',
      },

      closedExhibit: {
         fetch: async (ctx) => {
            const res = await getClosedExhibits({
               month: ctx.month,
               day: ctx.day,
               dayOfWeek: ctx.dayOfWeek,
            });

            return Array.isArray(res?.closed_exhibits) ? res.closed_exhibits : [];
         },
         cachePolicy: 'no-cache',
      },
   };
}
