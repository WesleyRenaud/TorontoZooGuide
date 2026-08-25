import { AnimalViewingScope } from '../shared/enums/animalViewingScope.js';

export const help = {
   continueUntilReopened: entityName => (
      `Leave blank to continue until the ${entityName} is reopened.`
   ),
   continueUntilScheduleEnded: 'Leave blank to continue until the schedule is ended.',
   endScheduleToday: 'Leave blank to end the schedule today.',
   endUpdateToday: 'Leave blank to end the update today.',
   keepAlertActiveUntilRemoved: 'Leave blank to keep the alert active until manually removed.',
   keepEventActiveWithoutEndDate: 'Leave blank to keep the event active with no end date.',
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
   endSingleWildEncounterScheduleTime: (
      'Leave blank to end all times for this encounter on the selected date.'
   ),
   endScheduleTimes: (
      'Select one or more scheduled times to end.'
   ),
   cancelOccurrenceTimes: (
      'Select one or more scheduled times to cancel.'
   ),
   noScheduledEncounterTimes: 'No scheduled times for this encounter.',
   encounterScheduleRows: 'Add each encounter time with the days it runs.',
   talkScheduleRows: 'Add each talk time with the days it runs.',
   removeEncounterScheduleRow: 'Remove this scheduled time',
   removeScheduledTime: time => `Remove ${time}`,
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
   attractionHoursTimeBounds: 'Failed to load zoo hours bounds for attraction hours.',
   restrooms: 'Failed to load restrooms.',
   updates: 'Failed to load updates.',
   wildEncounters: 'Failed to load Wild Encounters.',
};

export const placeholders = {
   attraction: 'Select an attraction',
   date: 'Select a date',
   dailyEndTime: 'Select a daily end time',
   dailyStartTime: 'Select a daily start time',
   weekdayEndTime: 'Select a weekday end time',
   weekdayStartTime: 'Select a weekday start time',
   weekendHolidayEndTime: 'Select a weekend/holiday end time',
   weekendHolidayStartTime: 'Select a weekend/holiday start time',
   endDate: 'Select an end date',
   encounterTimes: 'Select encounter times',
   selectWildEncounterFirst: 'Select a wild encounter first',
   selectDateFirst: 'Select a date first',
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
   viewingScope: 'Select viewing scope',
   wildEncounter: 'Select a Wild Encounter',
   transportationStation: 'Select a transportation station',
};

export const textareas = {
   closedMessage: entityName => `Enter the message shown when the ${entityName} is closed`,
   closureMessage: 'Enter the closure message shown to guests',
   currentDescription: 'Leave blank to keep the current description',
   drinkingFountainsClosedMessage: 'Optional message shown while drinking fountains are closed',
   eventDescription: 'Enter the event description shown to guests',
   eventLinkExample: 'https://www.torontozoo.com/...',
   eventLocationExample: 'Example: Front Courtyard',
   eventNameExample: 'Example: Conservation Carousel Ride Night',
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
   addGuardiansTalkOccurrence: 'Add Meet the Guardians talk occurrence',
   attractionClosed: 'Set attraction as closed',
   attractionClosureOverride: 'Create attraction closure override',
   attractionHoursSchedule: 'Set attraction hours',
   attractionOpeningSchedule: 'Set attraction opening schedule',
   cancelGuardiansTalkOccurrence: 'Cancel Meet the Guardians talk occurrence',
   cancelWildEncounterOccurrence: 'Cancel Wild Encounter occurrence',
   createEvent: 'Create event',
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
   giftShopOpeningSchedule: 'Set gift shop opening schedule',
   guardiansTalkSchedule: 'Set Meet the Guardians talk schedule',
   offDisplay: 'Set animal as off display',
   onDisplay: 'Set animal as on display',
   removeRestroomAlert: 'Remove restroom alert',
   removeViewingAlert: 'Remove animal viewing alert',
   removeVisibilitySchedule: 'Remove visibility schedule',
   restaurantClosed: 'Set restaurant as closed',
   restaurantClosureOverride: 'Create restaurant closure override',
   restaurantOpeningSchedule: 'Set restaurant opening schedule',
   restroomAlert: 'Set restroom alert',
   restroomClosed: 'Set restroom as closed',
   restroomOpen: 'Set restroom as open',
   viewingAlert: 'Set animal viewing alert',
   visibilitySchedule: 'Set animal visibility schedule',
   wildEncounterSchedule: 'Set Wild Encounter schedule',
   transportationRoute: 'Set current transportation route',
   transportationStationClosed: 'Set transportation station as closed',
   transportationStationOpen: 'Set transportation station as open',
};

export const status = {
   animalOffDisplay: result => `${result.species} in ${result.exhibit} was set as off display.`,
   animalOnDisplay: result => `${result.species} in ${result.exhibit} was set as on display.`,
   closed: name => `${name} was set as closed.`,
   closureOverrideSaved: name => `${name} closure override was saved.`,
   drinkingFountainsClosed: 'Drinking fountains were set as closed.',
   drinkingFountainsOpen: 'Drinking fountains were set as open.',
   eventCreated: result => `${result.name} was created.`,
   guardiansTalkScheduleEnded: result => `${result.talk} in ${result.location} schedule was ended.`,
   guardiansTalkScheduleSaved: result => `${result.talk} in ${result.location} schedule was saved.`,
   open: name => `${name} was set as open.`,
   openingScheduleSaved: name => `${name} opening schedule was saved.`,
   attractionHoursScheduleSaved: name => `${name} attraction hours were saved.`,
   explicitlyOpen: name => `${name} was set as explicitly open.`,
   scheduleEnded: name => `${name} schedule was ended.`,
   scheduleSaved: name => `${name} schedule was saved.`,
   scheduleWasEnded: 'Schedule was ended.',
   scheduleWasSaved: 'Schedule was saved.',
   updateCreated: result => `${result.title} was created.`,
   updateEdited: 'Update was edited.',
   updateEnded: 'Update was ended.',
   transportationRouteSet: result => `Transportation route was set to ${result.route}.`,
};

export const confirm = {
   deleteOldSchedules: 'Delete Old Schedules',
   openingScheduleOverlapMessage: (
      'This schedule overlaps one or more existing schedules. Choose how to resolve the conflict.'
   ),
   openingScheduleOverlapTitle: 'Schedule conflict',
   trimOldSchedules: 'Trim Old Schedules',
};

export const updateTypes = [
   { value: 'Animal Birth' },
   { value: 'Animal Passing' },
   { value: 'Closure' },
   { value: 'New Arrival' },
];

export const viewingScopes = [
   { value: AnimalViewingScope.ALL, label: 'Indoor and outdoor' },
   { value: AnimalViewingScope.INDOOR, label: 'Indoor only' },
   { value: AnimalViewingScope.OUTDOOR, label: 'Outdoor only' },
];

export const validation = {
   dateRangeInvalid: 'Invalid start or end date.',
   dailyViewingTimes: 'Daily viewing start and end times are required.',
   duplicateEncounterTime: 'Each encounter time can only be added once.',
   encounterScheduleRowNeedsDay: 'Each scheduled time needs at least one day selected.',
   endDateBeforeStartDate: 'End date cannot be before the start date.',
   entityRequired: entityLabel => `${entityLabel} is required.`,
   oneDay: 'At least one day must be selected.',
   oneChange: 'Enter at least one change.',
   weeklyAvailability: 'At least one day or holidays must be selected.',
   attractionHoursTimesRequired: (
      'Weekday and weekend/holiday start and end times are required.'
   ),
   attractionHoursWeekdayOrder: (
      'Weekday start time must be before weekday end time.'
   ),
   attractionHoursWeekendHolidayOrder: (
      'Weekend/holiday start time must be before weekend/holiday end time.'
   ),
   attractionHoursWeekdayBounds: (
      'Weekday hours must fall within regular zoo hours.'
   ),
   attractionHoursWeekendHolidayBounds: (
      'Weekend/holiday hours must fall within regular zoo hours.'
   ),
};
