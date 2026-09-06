export class Common {
   static actions = {
      addEncounterScheduleRow: 'Add another',
      removeAlert: 'Remove alert',
      save: 'Save',
   };

   static common = {
      animalPosition: (index, total) => `${index} of ${total}`,
      close: 'Close',
      closeSymbol: '×',
      genericFailed: 'Failed.',
      headsUp: 'Heads up',
      moreInfo: 'More Info',
      nextAnimal: 'Next animal',
      nextSymbol: '>',
      noMatches: 'No matches',
      previousAnimal: 'Previous animal',
      previousSymbol: '<',
      requestFailed: 'Request failed.',
      viewOnMap: 'View on Map',
   };

   static entityLabels = {
      animal: 'Animal',
      attraction: 'Attraction',
      attractions: 'attractions',
      exhibit: 'Exhibit',
      exhibits: 'exhibits',
      giftShop: 'Gift Shop',
      giftShops: 'gift shops',
      guardiansTalk: 'Meet The Guardians Talk',
      item: 'Item',
      items: 'items',
      pavilion: 'Pavilion',
      restaurant: 'Restaurant',
      restaurants: 'restaurants',
      restroom: 'Restroom',
      restrooms: 'restrooms',
      wildEncounter: 'Wild Encounter',
      transportation: 'Transportation',
      transportationStation: 'Transportation Station',
      transportationStations: 'transportation stations',
   };

   static entityPhrases = {
      guardiansTalk: 'guardians talk',
      wildEncounter: 'wild encounter',
   };

   static labels = {
      alertMessage: 'Alert message',
      closedMessage: 'Closed message',
      closureMessage: 'Closure message',
      dailyViewingEndTime: 'Daily viewing end time',
      dailyViewingStartTime: 'Daily viewing start time',
      weekdayEndTime: 'Weekday end time',
      weekdayStartTime: 'Weekday start time',
      weekendHolidayEndTime: 'Weekend/holiday end time',
      weekendHolidayStartTime: 'Weekend/holiday start time',
      date: 'Date',
      departure: 'Departure',
      description: 'Description',
      encounterTime: 'Encounter time',
      encounterTimes: 'Encounter times',
      talkTimes: 'Talk times',
      endDate: 'End date',
      link: 'Link',
      location: 'Location',
      message: 'Message',
      name: 'Name',
      occursOnTheseDays: 'Occurs on these days',
      openOnTheseDays: 'Open on these days',
      price: 'Price',
      reason: 'Reason',
      route: 'Route',
      scheduleEndDate: 'Schedule end date',
      scheduleMode: 'Schedule mode',
      scheduleMessage: 'Schedule message',
      schedulePreset: 'Schedule preset',
      species: 'Species',
      scheduleStartDate: 'Schedule start date',
      startDate: 'Start date',
      talkName: 'Talk name',
      talkTimeEveryDay: 'Talk time for every day',
      talkTime: 'Talk time',
      time: 'Time',
      title: 'Title',
      transportationRoundTrip: station => `${station} (round trip)`,
      transportationStations: (first, last) => `${first} → ${last}`,
      type: 'Type',
      update: 'Update',
      viewingScope: 'Viewing scope',
   };

   static likelihood = {
      high: 'High',
      low: 'Low',
      medium: 'Medium',
      moderate: 'Moderate',
      veryHigh: 'Very high',
      veryLow: 'Very low',
   };

   static schedule = {
      dayLabels: {
         monday: 'Monday',
         tuesday: 'Tuesday',
         wednesday: 'Wednesday',
         thursday: 'Thursday',
         friday: 'Friday',
         saturday: 'Saturday',
         sunday: 'Sunday',
         holidays: 'Holidays',
      },
      presetLabels: {
         custom: 'Custom',
         everyDay: 'Every day',
         weekendsAndHolidays: 'Weekends + holidays only',
         weekendsOnly: 'Weekends only',
      },
      guardiansTalkTimeModeLabels: {
         sameTimeEveryDay: 'Same time every day',
         weekdayTimes: 'Different times by day',
      },
      routeLabels: {
         summer: 'Summer',
         winter: 'Winter',
      },
   };
}
