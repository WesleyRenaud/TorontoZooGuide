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
            store.byType.animal = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
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

      // ✅ singular layer key
      restaurant: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-restaurants', {
               month: ctx.month,
               includeSeasonalRestaurants: ctx.includeSeasonalRestaurants,
               restaurantsToInclude: ctx.restaurantsToInclude,
            });

            const rows = res?.restaurants ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'restaurant' }));

            store.byType.restaurant = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
      restroom: {
         fetch: async () => {
            const cache = store.cache.restroom ?? store.cache.restroom;

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

      // ✅ singular layer key
      giftShop: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-gift-shops', {
               month: ctx.month,
               includeSeasonalGiftShops: ctx.includeSeasonalGiftShops,
               giftShopsToInclude: ctx.giftShopsToInclude,
            });

            const rows = res?.gift_shops ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'giftShop' }));

            store.byType.giftShop = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
      attraction: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-attractions', {
               month: ctx.month,
               includeSeasonalAttractions: ctx.includeSeasonalAttractions,
               attractionsToInclude: ctx.attractionsToInclude,
            });

            const rows = res?.attractions ?? res?.results ?? res ?? [];
            const normalized = rows.map(r => ({ ...r, type: 'attraction' }));

            store.byType.attraction = normalized;
            return normalized;
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
      zoomobileRoute: {
         fetch: async (ctx) => {
            const res = await ajaxPost('/get-zoomobile-route', {
               zoomobileRouteType: ctx.zoomobileRouteType,
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

            // 🔥 Store separately so combine() can merge correctly
            store.byType.zoomobileStation = stations;
            store.byType.zoomobileRouteMarker = routeMarkers;

            // Return both so this layer renders both
            return [...stations, ...routeMarkers];
         },
         cachePolicy: 'no-cache',
      },

      // ✅ singular layer key
      wildEncounterMeetingSpot: {
         fetch: async () => {
            const cache = store.cache.wildEncounterMeetingSpot ?? store.cache.wildEncounterMeetingSpot;

            if (!cache) {
               const res = await ajaxPost('/get-wild-encounter-meeting-spots', {});
               const rows = res?.wild_encounter_meeting_spots ?? res?.results ?? res ?? [];
               const normalized = rows.map(p => ({ ...p, type: 'wildEncounterMeetingSpot' }));
               store.byType.wildEncounterMeetingSpot = normalized;
               return normalized;
            }

            if (cache.loaded) return store.byType.wildEncounterMeetingSpot ?? store.byType.wildEncounterMeetingSpot ?? [];
            if (cache.inFlight) return cache.inFlight;

            cache.inFlight = ajaxPost('/get-wild-encounter-meeting-spots', {})
               .then(res => {
                  const rows = res?.wild_encounter_meeting_spots ?? res?.results ?? res ?? [];
                  const normalized = rows.map(p => ({ ...p, type: 'wildEncounterMeetingSpot' }));

                  store.byType.wildEncounterMeetingSpot = normalized;
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