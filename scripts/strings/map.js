export const map = {
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
   hideUpdates: 'Hide updates',
   nextUpdate: 'Next update',
   previousUpdate: 'Previous update',
   showUpdates: 'Show updates',
   zoomobileRoute: {
      none: 'None',
      title: 'Zoomobile route',
   },
};

export const search = {
   extraCharge: 'Extra Charge',
   freeWithAdmission: 'Free With Admission',
   location: location => `Location: ${location}`,
   region: region => `Region: ${region}`,
};

export const tooltips = {
   description: value => `Description: ${value}`,
   guardiansTalkDescription: (
      'Join our knowledgeable Guardians as they share fascinating facts about our animal residents. Discover how they are cared for, learn about conservation efforts, and explore the important role enrichment plays in their well-being. You may also see the animals enjoying their meals, learn about their diets, and observe their natural behaviours in action. Follow the schedule below to learn more about your favourite Toronto Zoo animals!'
   ),
   seasonalSchedule: value => `Seasonal Schedule: ${value}`,
   startTime: value => `Start Time: ${value}`,
   menu: 'MENU',
};
