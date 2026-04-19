export function createMapStore() {
   return {
      byType: {
         animal: [],
         pavilion: [],
         restaurant: [],
         restroom: [],
         giftShop: [],
         attraction: [],
         zoomobileStation: [],
         guardiansTalk: [],
         wildEncounter: [],
      },
      cache: {
         pavilion: { loaded: false, inFlight: null },
         restroom: { loaded: false, inFlight: null },
         exhibit: { loaded: false, inFlight: null },
      },
   };
}
