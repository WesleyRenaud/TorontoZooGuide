function asRows(value) {
   return Array.isArray(value) ? value : [];
}

function ensureStaticCache(store, type) {
   if (!store.cache[type]) {
      store.cache[type] = {
         loaded: false,
         inFlight: null,
      };
   }

   return store.cache[type];
}

export class SourceHelpers {
   static normalizeTypedRows(rows, type) {
      return asRows(rows).map((row) => ({
         ...row,
         type,
      }));
   }

   static setSourceRows(store, type, rows) {
      const normalizedRows = asRows(rows);
      store.byType[type] = normalizedRows;
      return normalizedRows;
   }

   static createDynamicTypedSource(store, type, fetchRows) {
      return {
         fetch: async (ctx) => {
            const rows = await fetchRows(ctx);
            return SourceHelpers.setSourceRows(store, type, rows);
         },
         cachePolicy: 'no-cache',
      };
   }

   static createStaticTypedSource(store, type, fetchRows) {
      return {
         fetch: async (ctx) => {
            const cache = ensureStaticCache(store, type);

            if (cache.loaded) {
               return store.byType[type] || [];
            }

            if (cache.inFlight) {
               return cache.inFlight;
            }

            cache.inFlight = Promise.resolve(fetchRows(ctx))
               .then((rows) => {
                  cache.loaded = true;
                  cache.inFlight = null;
                  return SourceHelpers.setSourceRows(store, type, rows);
               })
               .catch((error) => {
                  cache.inFlight = null;
                  throw error;
               });

            return cache.inFlight;
         },
         cachePolicy: 'static',
      };
   }
}
