export const help = {
   continueUntilReopened: entityName => (
      `Leave blank to continue until the ${entityName} is reopened.`
   ),
   continueUntilScheduleEnded: 'Leave blank to continue until the schedule is ended.',
   endScheduleToday: 'Leave blank to end the schedule today.',
   endUpdateToday: 'Leave blank to end the update today.',
   keepAlertActiveUntilRemoved: 'Leave blank to keep the alert active until manually removed.',
   keepClosedUntilManuallyReopened: entityName => (
      `Leave blank to keep the ${entityName} closed until it is manually reopened.`
   ),
   keepCurrentEndDate: 'Leave blank to keep the current end date.',
   keepOffDisplayUntilOnDisplay: (
      'Leave blank to keep the animal off display until it is manually set back on display.'
   ),
   keepExplicitlyOpenUntilChanged: (entityName, subject = 'it is') => (
      `Leave blank to keep the ${entityName} explicitly open until ${subject} changed.`
   ),
   keepRouteUntilChanged: 'Leave blank to keep this route until it is changed again.',
   keepScheduleUntilChanged: 'Leave blank to keep this schedule active until it is changed.',
   keepUpdateActiveWithoutEndDate: 'Leave blank to keep the update active with no end date.',
   keepVisibilityScheduleUntilChanged: (
      'Leave blank to keep this visibility schedule in place until manually changed.'
   ),
   startImmediately: 'Leave blank to start immediately.',
};

export const loadErrors = {
   entityOptions: optionsLabel => `Failed to load ${optionsLabel}.`,
   exhibits: 'Failed to load exhibits.',
   locations: 'Failed to load locations.',
   options: 'Failed to load options.',
   restrooms: 'Failed to load restrooms.',
   updates: 'Failed to load updates.',
   wildEncounters: 'Failed to load Wild Encounters.',
};

export const placeholders = {
   attraction: 'Select an attraction',
   date: 'Select a date',
   dailyEndTime: 'Select a daily end time',
   dailyStartTime: 'Select a daily start time',
   endDate: 'Select an end date',
   exhibit: 'Select an exhibit',
   giftShop: 'Select a gift shop',
   keepCurrentType: 'Keep current type',
   location: 'Select a location',
   newEndDate: 'Select a new end date',
   option: 'Select an option',
   restaurant: 'Select a restaurant',
   restroom: 'Select a restroom',
   restroomAlertExample: 'Example: Women\'s restroom is temporarily unavailable',
   scheduleEndDate: 'Select the date the schedule should end',
   scheduledTime: label => `Select ${label} time`,
   speciesSearch: 'Search for a species',
   startDate: 'Select a start date',
   talk: 'Select a talk',
   time: 'Select a time',
   type: 'Select a type',
   update: 'Select an update',
   wildEncounter: 'Select a Wild Encounter',
   zoomobileStation: 'Select a zoomobile station',
};

export const textareas = {
   closedMessage: entityName => `Enter the message shown when the ${entityName} is closed`,
   closureMessage: 'Enter the closure message shown to guests',
   currentDescription: 'Leave blank to keep the current description',
   drinkingFountainsClosedMessage: 'Optional message shown while drinking fountains are closed',
   offDisplayReason: 'Enter the reason this animal is off display',
   optionalScheduleMessage: scheduleName => (
      `Enter an optional message for this ${scheduleName} schedule`
   ),
   scheduledClosedMessage: entityName => (
      `Enter the message shown when the ${entityName} is closed outside this schedule`
   ),
   updateDescription: 'Enter the update shown to guests',
   updateTitleExample: 'Example: New baby giraffe',
   viewingAlert: 'Enter the viewing alert shown to guests',
   viewingMessage: 'Enter the viewing message shown to guests',
};

export const panelTitles = {
   attractionClosed: 'Set attraction as closed',
   attractionClosureOverride: 'Create attraction closure override',
   attractionOpen: 'Set attraction as open',
   cancelGuardiansTalkOccurrence: 'Cancel Meet the Guardians talk occurrence',
   cancelWildEncounterOccurrence: 'Cancel Wild Encounter occurrence',
   createUpdate: 'Create update',
   drinkingFountainsClosed: 'Close drinking fountains',
   drinkingFountainsOpen: 'Open drinking fountains',
   editUpdate: 'Edit update',
   endGuardiansTalkSchedule: 'End Meet the Guardians talk schedule',
   endUpdate: 'End update',
   endWildEncounterSchedule: 'End Wild Encounter schedule',
   exhibitClosed: 'Set exhibit as closed',
   exhibitOpen: 'Set exhibit as open',
   giftShopClosed: 'Set gift shop as closed',
   giftShopClosureOverride: 'Create gift shop closure override',
   giftShopOpen: 'Set gift shop as open',
   guardiansTalkSchedule: 'Set Meet the Guardians talk schedule',
   offDisplay: 'Set animal as off display',
   onDisplay: 'Set animal as on display',
   removeRestroomAlert: 'Remove restroom alert',
   removeViewingAlert: 'Remove animal viewing alert',
   removeVisibilitySchedule: 'Remove visibility schedule',
   restaurantClosed: 'Set restaurant as closed',
   restaurantClosureOverride: 'Create restaurant closure override',
   restaurantOpen: 'Set restaurant as open',
   restroomAlert: 'Set restroom alert',
   restroomClosed: 'Set restroom as closed',
   restroomOpen: 'Set restroom as open',
   viewingAlert: 'Set animal viewing alert',
   visibilitySchedule: 'Set animal visibility schedule',
   wildEncounterSchedule: 'Set Wild Encounter schedule',
   zoomobileRoute: 'Set current Zoomobile route',
   zoomobileStationClosed: 'Set zoomobile station as closed',
   zoomobileStationOpen: 'Set zoomobile station as open',
};

export const status = {
   animalOffDisplay: result => `${result.species} in ${result.exhibit} was set as off display.`,
   animalOnDisplay: result => `${result.species} in ${result.exhibit} was set as on display.`,
   closed: name => `${name} was set as closed.`,
   closureOverrideSaved: name => `${name} closure override was saved.`,
   drinkingFountainsClosed: 'Drinking fountains were set as closed.',
   drinkingFountainsOpen: 'Drinking fountains were set as open.',
   guardiansTalkScheduleEnded: result => `${result.talk} in ${result.location} schedule was ended.`,
   guardiansTalkScheduleSaved: result => `${result.talk} in ${result.location} schedule was saved.`,
   open: name => `${name} was set as open.`,
   openingScheduleSaved: name => `${name} opening schedule was saved.`,
   explicitlyOpen: name => `${name} was set as explicitly open.`,
   scheduleEnded: name => `${name} schedule was ended.`,
   scheduleSaved: name => `${name} schedule was saved.`,
   scheduleWasEnded: 'Schedule was ended.',
   scheduleWasSaved: 'Schedule was saved.',
   updateCreated: result => `${result.title} was created.`,
   updateEdited: 'Update was edited.',
   updateEnded: 'Update was ended.',
   zoomobileRouteSet: result => `Zoomobile route was set to ${result.route}.`,
};

export const updateTypes = [
   { value: 'Animal Birth' },
   { value: 'Animal Passing' },
   { value: 'Closure' },
   { value: 'New Arrival' },
   { value: 'Departure' },
];

export const validation = {
   dateRangeInvalid: 'Invalid start or end date.',
   dailyViewingTimes: 'Daily viewing start and end times are required.',
   endDateBeforeStartDate: 'End date cannot be before the start date.',
   entityRequired: entityLabel => `${entityLabel} is required.`,
   oneDay: 'At least one day must be selected.',
   oneChange: 'Enter at least one change.',
   weeklyAvailability: 'At least one day or holidays must be selected.',
};
