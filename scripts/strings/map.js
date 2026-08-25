import { asTrimmedString } from '../api/normalizeValues.js';

export const map = {
   exploreMenuAria: 'Explore menu',
   exploreTitle: 'Explore',
   filterLabel: 'Filter:',
   filterTypes: {
      defibrillator: 'Defibrillators',
      drinkingFountain: 'Drinking Fountains',
      emergencyIntercom: 'Emergency Intercoms',
      eventSite: 'Event Sites',
      giftShop: 'Gift Shops',
      guestService: 'Guest Services',
      guardiansTalk: 'Meet The Guardians Talks',
      pavilion: 'Pavilions',
      picnicSite: 'Picnic Sites',
      restaurant: 'Restaurants',
      restroom: 'Restrooms',
   },
   toggleLabels: {
      includeClosedAttractions: 'Include closed attractions',
      includeClosedGiftShops: 'Include closed gift shops',
      includeClosedRestaurants: 'Include closed restaurants',
      includeClosedRestrooms: 'Include closed restrooms',
      includeOffDisplayAnimals: 'Include off display animals',
      showMapLabels: 'Show region/pavilion text',
   },
   mapAria: 'Toronto Zoo Map',
   mapPresetPlaceholder: 'Select a map',
   mapPresets: {
      summer: 'Summer Map',
      winter: 'Winter Map',
      specificDay: 'Specific Map',
   },
   searchAnimals: 'Search animals',
   events: {
      title: 'Events',
   },
   updates: {
      title: 'Updates',
   },
   loadSvgFailed: status => `Failed to load zoo map SVG: ${status}`,
   filter: {
      attractions: 'Attractions',
   },
   hover: {
      defibrillator: 'Defibrillator',
      drinkingFountain: 'Drinking Fountain',
      emergencyIntercom: 'Emergency Intercom',
      eventSite: 'Event Site',
      guestService: 'Guest Service',
      guardiansTalkWithName: name => `${name} Meet The Guardians Talk`,
      picnicSite: 'Picnic Site',
      wildEncounterMeetingSpot: 'Wild Encounter Meeting Spot',
      wildEncounterMeetingSpotWithName: name => `Wild Encounter • ${name} - Meeting Spot`,
      wildEncounterMultiple: (name, count) => (
         `Wild Encounter • ${name} + ${count} more - Meeting Spot`
      ),
   },
   hideUpdates: 'Hide updates and events',
   nextEvent: 'Next event',
   nextUpdate: 'Next update',
   previousEvent: 'Previous event',
   previousUpdate: 'Previous update',
   showUpdates: 'Show updates and events',
   updatesAndEvents: 'Updates and events',
   transportationRoute: {
      none: 'None',
      current: 'Current Route',
      title: name => `${name} route`,
      route: route => {
         const normalized = asTrimmedString(route);

         if (!normalized) {
            return '';
         }

         return `${normalized.charAt(0).toUpperCase()}${normalized.slice(1)} Route`;
      },
   },
};

export const search = {
   extraCharge: 'Extra Charge',
   freeWithAdmission: 'Free With Admission',
   location: location => `Location: ${location}`,
   region: region => `Region: ${region}`,
};

export const tooltips = {
   defaultTransportationStationName: 'Zoomobile Station',
   description: value => `Description: ${value}`,
   guardiansTalkDescription: (
      'Join our knowledgeable Guardians as they share fascinating facts about our animal residents. Discover how they are cared for, learn about conservation efforts, and explore the important role enrichment plays in their well-being. You may also see the animals enjoying their meals, learn about their diets, and observe their natural behaviours in action. Follow the schedule below to learn more about your favourite Toronto Zoo animals!'
   ),
   likelihoodDetail: (phrase, percent) => `Likelihood: ${phrase} (~${percent}%)`,
   seasonalSchedule: value => `Seasonal Schedule: ${value}`,
   startTime: value => `Start Time: ${value}`,
   times: value => `Times: ${value}`,
   menu: 'MENU',
};
