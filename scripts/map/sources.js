import { ajaxPost } from '../utils/ajax.js';

export function createDataSources(store) {
   return {
\      animal: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-visible-animals', {
               month: ctx.month,
               day: ctx.day,
               temp: ctx.temp,
               includeOffDisplayAnimals: ctx.includeOffDisplayAnimals,
               speciesToInclude: ctx.speciesToInclude,
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
               const res = await ajaxPost('/get-pavilions', {});
               const rows = res?.pavilions ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'pavilion' }));
               store.byType.pavilion = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.pavilion ?? store.byType.pavilions ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = ajaxPost('/get-pavilions', {})
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
            const res = await ajaxPost('/get-restaurants', {
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
               const res = await ajaxPost('/get-restrooms', {});
               const rows = res?.restrooms ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'restroom' }));
               store.byType.restroom = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.restroom ?? store.byType.restrooms ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = ajaxPost('/get-restrooms', {})
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
            const res = await ajaxPost('/get-gift-shops', {
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
            const res = await ajaxPost('/get-attractions', {
               month: ctx.month,
               day: ctx.day,
               includeClosedAttractions: ctx.includeClosedAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
            });

            const rows = res?.attractions ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'attraction' }));

            store.byType.attraction = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      guardiansTalk: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-guardians-talks', {
               month: ctx.month,
               day: ctx.day,
               talksToInclude: ctx.talksToInclude,
            });

            const rows = res?.guardians_talks ?? res?.talks ?? res?.results ?? res ?? [];
            const normalized = (Array.isArray(rows) ? rows : []).map(t => ({ ...t, type: 'guardiansTalk' }));

            store.byType.guardiansTalk = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      zoomobileRoute: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-zoomobile-route', {
               zoomobileRoute: ctx.zoomobileRoute,
               zoomobileStationsToInclude: ctx.zoomobileStationsToInclude,
            });

            const stations = (res?.zoomobile_stations ?? []).map(r => ({
               ...r,
               type: 'zoomobileStation',
            }));

            const routeMarkers = (res?.zoomobile_route_markers ?? []).map(r => ({
               ...r,
               type: 'zoomobileRouteMarker',
            }));

            store.byType.zoomobileStation = stations;
            store.byType.zoomobileRouteMarker = routeMarkers;

            return [...stations, ...routeMarkers];
         },
         cachePolicy: 'no-cache',
      },

      wildEncounter: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-wild-encounters', {
               month: ctx.month,
               day: ctx.day,
               wildEncountersToInclude: ctx.wildEncountersToInclude,
            });

            const rows = res?.wild_encounters ?? res?.results ?? res ?? [];
            const normalized = (Array.isArray(rows) ? rows : []).map(w => ({ ...w, type: 'wildEncounter' }));

            store.byType.wildEncounter = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      buildItinerary: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/build-itinerary', {
               month: ctx.month,
               day: ctx.day,
               temp: ctx.temp,

               animals: ctx.animals || [],
               attractions: ctx.attractions || [],
               guardiansTalks: ctx.guardiansTalks || [],
               wildEncounters: ctx.wildEncounters || [],
            });

            const animals = Array.isArray(res?.animals) ? res.animals.map(r => ({ ...r, type: 'animal' })) : [];
            const attractions = Array.isArray(res?.attractions) ? res.attractions.map(r => ({ ...r, type: 'attraction' })) : [];
            const talks = Array.isArray(res?.guardians_talks)
               ? res.guardians_talks.map(r => ({ ...r, type: 'guardiansTalk' }))
               : Array.isArray(res?.guardiansTalks)
               ? res.guardiansTalks.map(r => ({ ...r, type: 'guardiansTalk' }))
               : [];
            const wild = Array.isArray(res?.wild_encounters)
               ? res.wild_encounters.map(r => ({ ...r, type: 'wildEncounter' }))
               : Array.isArray(res?.wildEncounters)
               ? res.wild_encounters.map(r => ({ ...r, type: 'wildEncounter' }))
               : [];

            const flat = [...animals, ...attractions, ...talks, ...wild];

            store.byType.buildItinerary = flat;
            return flat;
         },
         cachePolicy: 'no-cache',
      },

      exhibit: {
         fetch: async () => {
            const cache = store.cache.exhibit ?? store.cache.exhibits;

            if (!cache) {
               const res = await ajaxPost('/get-exhibits', {});
               const rows = res?.exhibits ?? res?.results ?? res ?? [];
               const normalized = rows.map(e => ({ ...e, type: 'exhibit' }));
               store.byType.exhibit = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.exhibit ?? store.byType.exhibits ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = ajaxPost('/get-exhibits', {})
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
   };
}