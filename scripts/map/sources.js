import { ajaxPost } from '../utils/ajax.js';

export function createDataSources(store) {
   return {
      // ✅ singular layer key
      animal: {
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

            // keep store consistent with layer key
            store.byType.animal = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
      pavilion: {
         fetch: async () => {
            // Back-compat if store/cache were previously plural
            const cache = store.cache.pavilion ?? store.cache.pavilions;
            if (!cache) {
               // If cache object wasn't initialized, behave like no-cache
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

      // ✅ singular layer key
      restaurant: {
         fetch: async () => {
            // Back-compat if store/cache were previously plural
            const cache = store.cache.restaurant ?? store.cache.restaurants;
            if (!cache) {
               // If cache object wasn't initialized, behave like no-cache
               const res = await ajaxPost('/get-restaurants', {});
               const rows = res?.restaurants ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'restaurant' }));
               store.byType.restaurant = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.restaurant ?? store.byType.restaurants ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = ajaxPost('/get-restaurants', {})
               .then(res => {
                  const rows = res?.restaurants ?? res?.results ?? res ?? [];
                  const normalized = rows.map(p => ({ ...p, type: 'restaurant' }));

                  store.byType.restaurant = normalized;
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