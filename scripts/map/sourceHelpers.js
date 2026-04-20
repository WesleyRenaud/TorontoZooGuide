function asRows(value) {
   return Array.isArray(value) ? value : [];
}

export function normalizeTypedRows(rows, type) {
   return asRows(rows).map((row) => ({
      ...row,
      type,
   }));
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

export function setSourceRows(store, type, rows) {
   const normalizedRows = asRows(rows);
   store.byType[type] = normalizedRows;
   return normalizedRows;
}

export function createDynamicTypedSource(store, type, fetchRows) {
   return {
      fetch: async (ctx) => {
         const rows = await fetchRows(ctx);
         return setSourceRows(store, type, rows);
      },
      cachePolicy: 'no-cache',
   };
}

export function createStaticTypedSource(store, type, fetchRows) {
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
               return setSourceRows(store, type, rows);
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
