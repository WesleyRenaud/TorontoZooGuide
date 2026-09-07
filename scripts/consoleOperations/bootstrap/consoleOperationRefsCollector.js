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
      hoursSchedule: {
         operationName: 'attractionHoursSchedule',
         fieldSuffixes: {
            attractionEl: 'Attraction',
            startDateEl: 'StartDate',
            endDateEl: 'EndDate',
            weekdayStartTimeEl: 'WeekdayStartTime',
            weekdayEndTimeEl: 'WeekdayEndTime',
            weekendHolidayStartTimeEl: 'WeekendHolidayStartTime',
            weekendHolidayEndTimeEl: 'WeekendHolidayEndTime',
         },
      },
   },
   transportation: {
      stationClosed: {
         operationName: 'transportationStationClosed',
         includeDateRange: true,
         fieldSuffixes: {
            transportationStationEl: 'TransportationStation',
            messageEl: 'Message',
         },
      },
      stationOpen: {
         operationName: 'transportationStationOpen',
         fieldSuffixes: {
            transportationStationEl: 'TransportationStation',
         },
      },
      route: {
         operationName: 'transportationRoute',
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
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            scheduleRowsEl: 'ScheduleRows',
            addScheduleRowEl: 'AddScheduleRow',
            messageEl: 'Message',
         },
      },
      endSchedule: {
         operationName: 'endGuardiansTalkSchedule',
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            timesEl: 'Times',
            endDateEl: 'EndDate',
         },
      },
      addOccurrence: {
         operationName: 'addGuardiansTalkOccurrence',
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            dateEl: 'Date',
            timeEl: 'Time',
         },
      },
      cancelOccurrence: {
         operationName: 'cancelGuardiansTalkOccurrence',
         fieldSuffixes: {
            locationEl: 'Location',
            talkNameEl: 'TalkName',
            dateEl: 'Date',
            timesEl: 'Times',
         },
      },
   },
   wildEncounters: {
      schedule: {
         operationName: 'wildEncounterSchedule',
         includeDateRange: true,
         fieldSuffixes: {
            scheduleRowsEl: 'ScheduleRows',
            addScheduleRowEl: 'AddScheduleRow',
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
   events: {
      create: {
         operationName: 'createEvent',
         includeDateRange: true,
         fieldSuffixes: {
            nameEl: 'Name',
            locationEl: 'Location',
            descriptionEl: 'Description',
            linkEl: 'Link',
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

export class ConsoleOperationRefsCollector {
   static getById(doc, id) {
      return doc.getElementById(id);
   }

   static capitalizeFirstLetter(value = '') {
      return value.charAt(0).toUpperCase() + value.slice(1);
   }

   static createElementRefs(doc, idsByKey = {}) {
      const refs = {};

      Object.entries(idsByKey).forEach(([key, id]) => {
         refs[key] = ConsoleOperationRefsCollector.getById(doc, id);
      });

      return refs;
   }

   static createPrefixedRefs(doc, prefix, suffixesByKey = {}) {
      const idsByKey = {};

      Object.entries(suffixesByKey).forEach(([key, suffix]) => {
         idsByKey[key] = `${prefix}${suffix}`;
      });

      return ConsoleOperationRefsCollector.createElementRefs(doc, idsByKey);
   }

   static createFormRefs(doc, operationName) {
      const capitalizedOperationName = ConsoleOperationRefsCollector.capitalizeFirstLetter(operationName);

      return ConsoleOperationRefsCollector.createElementRefs(doc, {
         showButtonEl: `show${capitalizedOperationName}Form`,
         panelEl: `${operationName}Panel`,
         submitButtonEl: `submit${capitalizedOperationName}`,
         statusEl: `${operationName}Status`,
      });
   }

   static createAnimalSpeciesRefs(doc, operationName) {
      return ConsoleOperationRefsCollector.createPrefixedRefs(doc, operationName, {
         speciesEl: 'Species',
         speciesResultsEl: 'SpeciesResults',
         exhibitEl: 'Exhibit',
      });
   }

   static createDateRangeRefs(doc, operationName) {
      return ConsoleOperationRefsCollector.createPrefixedRefs(doc, operationName, {
         startDateEl: 'StartDate',
         endDateEl: 'EndDate',
      });
   }

   static createWeekdayScheduleRefs(doc, operationName) {
      return ConsoleOperationRefsCollector.createPrefixedRefs(doc, operationName, WEEKDAY_FIELD_SUFFIXES);
   }

   static createWeeklyAvailabilityRefs(doc, operationName) {
      return ConsoleOperationRefsCollector.createPrefixedRefs(doc, operationName, {
         presetEl: 'Preset',
         startDateEl: 'StartDate',
         endDateEl: 'EndDate',
         ...WEEKDAY_FIELD_SUFFIXES,
         holidaysOnlyEl: 'HolidaysOnly',
      });
   }

   static createOperationRefs(doc, {
      operationName,
      includeAnimalSpecies = false,
      includeDateRange = false,
      includeWeekdaySchedule = false,
      includeWeeklyAvailability = false,
      fieldSuffixes = {},
      fieldIds = {},
   } = {}) {
      return {
         ...ConsoleOperationRefsCollector.createFormRefs(doc, operationName),
         ...(includeAnimalSpecies ? ConsoleOperationRefsCollector.createAnimalSpeciesRefs(doc, operationName) : {}),
         ...(includeDateRange ? ConsoleOperationRefsCollector.createDateRangeRefs(doc, operationName) : {}),
         ...(includeWeekdaySchedule ? ConsoleOperationRefsCollector.createWeekdayScheduleRefs(doc, operationName) : {}),
         ...(includeWeeklyAvailability ? ConsoleOperationRefsCollector.createWeeklyAvailabilityRefs(doc, operationName) : {}),
         ...ConsoleOperationRefsCollector.createPrefixedRefs(doc, operationName, fieldSuffixes),
         ...ConsoleOperationRefsCollector.createElementRefs(doc, fieldIds),
      };
   }

   static createGroupRefs(doc, groupConfig = {}) {
      const groupRefs = {};

      Object.entries(groupConfig).forEach(([key, config]) => {
         groupRefs[key] = ConsoleOperationRefsCollector.createOperationRefs(doc, config);
      });

      return groupRefs;
   }

   static collectConsoleOperationRefs(doc = document) {
      const refs = {};

      Object.entries(CONSOLE_OPERATION_REF_CONFIG).forEach(([key, groupConfig]) => {
         refs[key] = ConsoleOperationRefsCollector.createGroupRefs(doc, groupConfig);
      });

      return refs;
   }
}
