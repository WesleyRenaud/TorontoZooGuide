const WEEKDAY_FIELD_SUFFIXES = {
   mondayEl: 'Monday',
   tuesdayEl: 'Tuesday',
   wednesdayEl: 'Wednesday',
   thursdayEl: 'Thursday',
   fridayEl: 'Friday',
   saturdayEl: 'Saturday',
   sundayEl: 'Sunday',
};

const CONSOLE_OPERATION_REF_CONFIG = {
   animals: {
      offDisplay: {
         operationName: 'offDisplay',
         includeAnimalSpecies: true,
         includeDateRange: true,
         fieldSuffixes: {
            viewingScopeEl: 'ViewingScope',
            messageEl: 'Message',
         },
      },
      onDisplay: {
         operationName: 'onDisplay',
         includeAnimalSpecies: true,
         fieldSuffixes: {
            viewingScopeEl: 'ViewingScope',
         },
      },
      visibilitySchedule: {
         operationName: 'visibilitySchedule',
         includeAnimalSpecies: true,
         includeDateRange: true,
         fieldSuffixes: {
            dailyStartTimeEl: 'DailyStartTime',
            dailyEndTimeEl: 'DailyEndTime',
            messageEl: 'Message',
         },
      },
      removeVisibilitySchedule: {
         operationName: 'removeVisibilitySchedule',
         includeAnimalSpecies: true,
      },
      viewingAlert: {
         operationName: 'viewingAlert',
         includeAnimalSpecies: true,
         includeDateRange: true,
         fieldSuffixes: {
            messageEl: 'Message',
         },
      },
      removeViewingAlert: {
         operationName: 'removeViewingAlert',
         includeAnimalSpecies: true,
      },
   },
   exhibits: {
      closed: {
         operationName: 'exhibitClosed',
         includeDateRange: true,
         fieldSuffixes: {
            exhibitEl: 'Exhibit',
            messageEl: 'Message',
         },
      },
      open: {
         operationName: 'exhibitOpen',
         includeDateRange: true,
         fieldSuffixes: {
            exhibitEl: 'Exhibit',
         },
      },
   },
   restaurants: {
      closed: {
         operationName: 'restaurantClosed',
         includeDateRange: true,
         fieldSuffixes: {
            restaurantEl: 'Restaurant',
            messageEl: 'Message',
         },
      },
      closureOverride: {
         operationName: 'restaurantClosureOverride',
         includeDateRange: true,
         fieldSuffixes: {
            restaurantEl: 'Restaurant',
            messageEl: 'Message',
         },
      },
      openingSchedule: {
         operationName: 'restaurantOpeningSchedule',
         includeWeeklyAvailability: true,
         fieldSuffixes: {
            restaurantEl: 'Restaurant',
            messageEl: 'Message',
         },
      },
   },
   restrooms: {
      closed: {
         operationName: 'restroomClosed',
         includeDateRange: true,
         fieldSuffixes: {
            restroomEl: 'Restroom',
            messageEl: 'Message',
         },
      },
      open: {
         operationName: 'restroomOpen',
         includeDateRange: true,
         fieldSuffixes: {
            restroomEl: 'Restroom',
         },
      },
      alert: {
         operationName: 'restroomAlert',
         includeDateRange: true,
         fieldSuffixes: {
            restroomEl: 'Restroom',
            messageEl: 'Message',
         },
      },
      removeAlert: {
         operationName: 'removeRestroomAlert',
         fieldSuffixes: {
            restroomEl: 'Restroom',
         },
      },
   },
   giftShops: {
      closed: {
         operationName: 'giftShopClosed',
         includeDateRange: true,
         fieldSuffixes: {
            giftShopEl: 'GiftShop',
            messageEl: 'Message',
         },
      },
      closureOverride: {
         operationName: 'giftShopClosureOverride',
         includeDateRange: true,
         fieldSuffixes: {
            giftShopEl: 'GiftShop',
            messageEl: 'Message',
         },
      },
      openingSchedule: {
         operationName: 'giftShopOpeningSchedule',
         includeWeeklyAvailability: true,
         fieldSuffixes: {
            giftShopEl: 'GiftShop',
            messageEl: 'Message',
         },
      },
   },
   attractions: {
      closed: {
         operationName: 'attractionClosed',
         includeDateRange: true,
         fieldSuffixes: {
            attractionEl: 'Attraction',
            messageEl: 'Message',
         },
      },
      closureOverride: {
         operationName: 'attractionClosureOverride',
         includeDateRange: true,
         fieldSuffixes: {
            attractionEl: 'Attraction',
            messageEl: 'Message',
         },
      },
      openingSchedule: {
         operationName: 'attractionOpeningSchedule',
         includeWeeklyAvailability: true,
         fieldSuffixes: {
            attractionEl: 'Attraction',
            messageEl: 'Message',
         },
      },
   },
   zoomobile: {
      stationClosed: {
         operationName: 'zoomobileStationClosed',
         includeDateRange: true,
         fieldSuffixes: {
            zoomobileStationEl: 'ZoomobileStation',
            messageEl: 'Message',
         },
      },
      stationOpen: {
         operationName: 'zoomobileStationOpen',
         fieldSuffixes: {
            zoomobileStationEl: 'ZoomobileStation',
         },
      },
      route: {
         operationName: 'zoomobileRoute',
         includeDateRange: true,
         fieldSuffixes: {
            summerRouteEl: 'Summer',
            winterRouteEl: 'Winter',
         },
      },
   },
   guardiansTalks: {
      schedule: {
         operationName: 'guardiansTalkSchedule',
         includeDateRange: true,
         includeWeekdaySchedule: true,
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            sameTimeEveryDayModeEl: 'SameTimeEveryDayMode',
            weekdayTimesModeEl: 'WeekdayTimesMode',
            dailyTimeEl: 'DailyTime',
            mondayTimeEl: 'MondayTime',
            tuesdayTimeEl: 'TuesdayTime',
            wednesdayTimeEl: 'WednesdayTime',
            thursdayTimeEl: 'ThursdayTime',
            fridayTimeEl: 'FridayTime',
            saturdayTimeEl: 'SaturdayTime',
            sundayTimeEl: 'SundayTime',
            messageEl: 'Message',
         },
      },
      endSchedule: {
         operationName: 'endGuardiansTalkSchedule',
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            endDateEl: 'EndDate',
         },
      },
      cancelOccurrence: {
         operationName: 'cancelGuardiansTalkOccurrence',
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            dateEl: 'Date',
            timeEl: 'Time',
         },
      },
   },
   wildEncounters: {
      schedule: {
         operationName: 'wildEncounterSchedule',
         includeDateRange: true,
         includeWeekdaySchedule: true,
         fieldSuffixes: {
            timesListEl: 'Times',
            timeEl: 'Time',
            messageEl: 'Message',
         },
         fieldIds: {
            wildEncounterEl: 'wildEncounterScheduleName',
         },
      },
      endSchedule: {
         operationName: 'endWildEncounterSchedule',
         fieldSuffixes: {
            timesEl: 'Times',
         },
         fieldIds: {
            wildEncounterEl: 'endWildEncounterScheduleName',
            endDateEl: 'endWildEncounterScheduleDate',
         },
      },
      cancelOccurrence: {
         operationName: 'cancelWildEncounterOccurrence',
         fieldSuffixes: {
            dateEl: 'Date',
            timesEl: 'Times',
         },
         fieldIds: {
            wildEncounterEl: 'cancelWildEncounterOccurrenceName',
         },
      },
   },
   drinkingFountains: {
      closed: {
         operationName: 'drinkingFountainsClosed',
         fieldSuffixes: {
            startDateEl: 'StartDate',
            endDateEl: 'EndDate',
            messageEl: 'Message',
         },
      },
      open: {
         operationName: 'drinkingFountainsOpen',
         fieldSuffixes: {
            startDateEl: 'StartDate',
            endDateEl: 'EndDate',
         },
      },
   },
   updates: {
      create: {
         operationName: 'createUpdate',
         includeDateRange: true,
         fieldSuffixes: {
            titleEl: 'Title',
            descriptionEl: 'Description',
            typeEl: 'Type',
         },
      },
      end: {
         operationName: 'endUpdate',
         fieldSuffixes: {
            updateEl: 'Key',
            endDateEl: 'EndDate',
         },
      },
      edit: {
         operationName: 'editUpdate',
         fieldSuffixes: {
            updateEl: 'Key',
            descriptionEl: 'Description',
            typeEl: 'Type',
            endDateEl: 'EndDate',
         },
      },
   },
};

function getById(doc, id) {
   return doc.getElementById(id);
}

function capitalizeFirstLetter(value = '') {
   return value.charAt(0).toUpperCase() + value.slice(1);
}

function createElementRefs(doc, idsByKey = {}) {
   const refs = {};

   Object.entries(idsByKey).forEach(([key, id]) => {
      refs[key] = getById(doc, id);
   });

   return refs;
}

function createPrefixedRefs(doc, prefix, suffixesByKey = {}) {
   const idsByKey = {};

   Object.entries(suffixesByKey).forEach(([key, suffix]) => {
      idsByKey[key] = `${prefix}${suffix}`;
   });

   return createElementRefs(doc, idsByKey);
}

function createFormRefs(doc, operationName) {
   const capitalizedOperationName = capitalizeFirstLetter(operationName);

   return createElementRefs(doc, {
      showButtonEl: `show${capitalizedOperationName}Form`,
      panelEl: `${operationName}Panel`,
      submitButtonEl: `submit${capitalizedOperationName}`,
      statusEl: `${operationName}Status`,
   });
}

function createAnimalSpeciesRefs(doc, operationName) {
   return createPrefixedRefs(doc, operationName, {
      speciesEl: 'Species',
      speciesResultsEl: 'SpeciesResults',
      exhibitEl: 'Exhibit',
   });
}

function createDateRangeRefs(doc, operationName) {
   return createPrefixedRefs(doc, operationName, {
      startDateEl: 'StartDate',
      endDateEl: 'EndDate',
   });
}

function createWeekdayScheduleRefs(doc, operationName) {
   return createPrefixedRefs(doc, operationName, WEEKDAY_FIELD_SUFFIXES);
}

function createWeeklyAvailabilityRefs(doc, operationName) {
   return createPrefixedRefs(doc, operationName, {
      presetEl: 'Preset',
      startDateEl: 'StartDate',
      endDateEl: 'EndDate',
      ...WEEKDAY_FIELD_SUFFIXES,
      holidaysOnlyEl: 'HolidaysOnly',
   });
}

function createOperationRefs(doc, {
   operationName,
   includeAnimalSpecies = false,
   includeDateRange = false,
   includeWeekdaySchedule = false,
   includeWeeklyAvailability = false,
   fieldSuffixes = {},
   fieldIds = {},
} = {}) {
   return {
      ...createFormRefs(doc, operationName),
      ...(includeAnimalSpecies ? createAnimalSpeciesRefs(doc, operationName) : {}),
      ...(includeDateRange ? createDateRangeRefs(doc, operationName) : {}),
      ...(includeWeekdaySchedule ? createWeekdayScheduleRefs(doc, operationName) : {}),
      ...(includeWeeklyAvailability ? createWeeklyAvailabilityRefs(doc, operationName) : {}),
      ...createPrefixedRefs(doc, operationName, fieldSuffixes),
      ...createElementRefs(doc, fieldIds),
   };
}

function createGroupRefs(doc, groupConfig = {}) {
   const groupRefs = {};

   Object.entries(groupConfig).forEach(([key, config]) => {
      groupRefs[key] = createOperationRefs(doc, config);
   });

   return groupRefs;
}

export function collectConsoleOperationRefs(doc = document) {
   const refs = {};

   Object.entries(CONSOLE_OPERATION_REF_CONFIG).forEach(([key, groupConfig]) => {
      refs[key] = createGroupRefs(doc, groupConfig);
   });

   return refs;
}
