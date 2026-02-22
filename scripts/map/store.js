export function createMapStore() {
   return {
      byType: {
         animal: [],
         pavilion: [],
         restaurant: [],
         restroom: [],
         giftShop: [],
      },
      cache: {
         pavilion: { loaded: false, inFlight: null },
         restroom: { loaded: false, inFlight: null }
      },
   };
}