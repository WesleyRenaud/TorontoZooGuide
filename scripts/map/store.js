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
         wildEncounterMeetingSpot: [],
      },
      cache: {
         pavilion: { loaded: false, inFlight: null },
         restroom: { loaded: false, inFlight: null },
         wildEncounterMeetingSpot: { loaded: false, inFlight: null }
      },
   };
}