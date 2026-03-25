import { postJson } from '../api/apiClient.js';

export function createDataSources(store) {
   return {
      animal: {
         fetch: async (ctx) => {
            const res = await postJson('/get-visible-animals', {
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
               const res = await postJson('/get-pavilions', {});
               const rows = res?.pavilions ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'pavilion' }));
               store.byType.pavilion = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.pavilion ?? store.byType.pavilions ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = postJson('/get-pavilions', {})
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
            const res = await postJson('/get-restaurants', {
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
               const res = await postJson('/get-restrooms', {});
               const rows = res?.restrooms ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'restroom' }));
               store.byType.restroom = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.restroom ?? store.byType.restrooms ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = postJson('/get-restrooms', {})
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
            const res = await postJson('/get-gift-shops', {
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
            const res = await postJson('/get-attractions', {
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

      guardiansTalk: {
         fetch: async (ctx) => {
            const res = await postJson('/get-guardians-talks', {
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
            const res = await postJson('/get-wild-encounters', {
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
               const res = await postJson('/get-exhibits', {});
               const rows = res?.exhibits ?? res?.results ?? res ?? [];
               const normalized = rows.map(e => ({ ...e, type: 'exhibit' }));
               store.byType.exhibit = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.exhibit ?? store.byType.exhibits ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = postJson('/get-exhibits', {})
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