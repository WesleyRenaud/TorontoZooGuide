export class SourceHelpersInternals {
   static asRows(value) {
      return Array.isArray(value) ? value : [];
   }

   static ensureStaticCache(store, type) {
      if (!store.cache[type]) {
         store.cache[type] = {
            loaded: false,
            inFlight: null,
         };
      }

      return store.cache[type];
   }
}
