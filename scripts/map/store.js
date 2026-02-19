export function createMapStore() {
   return {
      byType: {
         animal: [],
         pavilion: [],
      },
      cache: {
         pavilion: { loaded: false, inFlight: null },
      },
   };
}