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
         defibrillator: [],
         emergencyIntercom: [],
         guestService: [],
         picnicSite: [],
         eventSite: [],
      },
      cache: {
         pavilion: { loaded: false, inFlight: null },
         restroom: { loaded: false, inFlight: null },
         exhibit: { loaded: false, inFlight: null },
         defibrillator: { loaded: false, inFlight: null },
         emergencyIntercom: { loaded: false, inFlight: null },
         guestService: { loaded: false, inFlight: null },
         picnicSite: { loaded: false, inFlight: null },
         eventSite: { loaded: false, inFlight: null },
      },
   };
}
