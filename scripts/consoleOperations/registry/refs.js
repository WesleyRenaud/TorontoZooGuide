function getById(doc, id) {
   return doc.getElementById(id);
}

function createFormRefs(doc, {
   showButtonId,
   panelId,
   submitButtonId,
   statusId,
} = {}) {
   return {
      showButtonEl: getById(doc, showButtonId),
      panelEl: getById(doc, panelId),
      submitButtonEl: getById(doc, submitButtonId),
      statusEl: getById(doc, statusId),
   };
}

function createAnimalSpeciesRefs(doc, prefix) {
   return {
      speciesEl: getById(doc, `${prefix}Species`),
      speciesResultsEl: getById(doc, `${prefix}SpeciesResults`),
      exhibitEl: getById(doc, `${prefix}Exhibit`),
   };
}

function createDateRangeRefs(doc, prefix) {
   return {
      startDateEl: getById(doc, `${prefix}StartDate`),
      endDateEl: getById(doc, `${prefix}EndDate`),
   };
}

function createWeeklyAvailabilityRefs(doc, prefix) {
   return {
      presetEl: getById(doc, `${prefix}Preset`),
      ...createDateRangeRefs(doc, prefix),
      mondayEl: getById(doc, `${prefix}Monday`),
      tuesdayEl: getById(doc, `${prefix}Tuesday`),
      wednesdayEl: getById(doc, `${prefix}Wednesday`),
      thursdayEl: getById(doc, `${prefix}Thursday`),
      fridayEl: getById(doc, `${prefix}Friday`),
      saturdayEl: getById(doc, `${prefix}Saturday`),
      sundayEl: getById(doc, `${prefix}Sunday`),
      holidaysOnlyEl: getById(doc, `${prefix}HolidaysOnly`),
   };
}

function createWeekdayScheduleRefs(doc, prefix) {
   return {
      mondayEl: getById(doc, `${prefix}Monday`),
      tuesdayEl: getById(doc, `${prefix}Tuesday`),
      wednesdayEl: getById(doc, `${prefix}Wednesday`),
      thursdayEl: getById(doc, `${prefix}Thursday`),
      fridayEl: getById(doc, `${prefix}Friday`),
      saturdayEl: getById(doc, `${prefix}Saturday`),
      sundayEl: getById(doc, `${prefix}Sunday`),
   };
}

export function getConsoleOperationsRefs(doc = document) {
   return {
      animals: {
         offDisplay: {
            ...createFormRefs(doc, {
               showButtonId: 'showOffDisplayForm',
               panelId: 'offDisplayPanel',
               submitButtonId: 'submitOffDisplay',
               statusId: 'offDisplayStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'offDisplay'),
            ...createDateRangeRefs(doc, 'offDisplay'),
            messageEl: getById(doc, 'offDisplayMessage'),
         },
         onDisplay: {
            ...createFormRefs(doc, {
               showButtonId: 'showOnDisplayForm',
               panelId: 'onDisplayPanel',
               submitButtonId: 'submitOnDisplay',
               statusId: 'onDisplayStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'onDisplay'),
         },
         visibilitySchedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showVisibilityScheduleForm',
               panelId: 'visibilitySchedulePanel',
               submitButtonId: 'submitVisibilitySchedule',
               statusId: 'visibilityScheduleStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'visibilitySchedule'),
            ...createDateRangeRefs(doc, 'visibilitySchedule'),
            dailyStartTimeEl: getById(doc, 'visibilityScheduleDailyStartTime'),
            dailyEndTimeEl: getById(doc, 'visibilityScheduleDailyEndTime'),
            messageEl: getById(doc, 'visibilityScheduleMessage'),
         },
         removeVisibilitySchedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showRemoveVisibilityScheduleForm',
               panelId: 'removeVisibilitySchedulePanel',
               submitButtonId: 'submitRemoveVisibilitySchedule',
               statusId: 'removeVisibilityScheduleStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'removeVisibilitySchedule'),
         },
         viewingAlert: {
            ...createFormRefs(doc, {
               showButtonId: 'showViewingAlertForm',
               panelId: 'viewingAlertPanel',
               submitButtonId: 'submitViewingAlert',
               statusId: 'viewingAlertStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'viewingAlert'),
            ...createDateRangeRefs(doc, 'viewingAlert'),
            messageEl: getById(doc, 'viewingAlertMessage'),
         },
         removeViewingAlert: {
            ...createFormRefs(doc, {
               showButtonId: 'showRemoveViewingAlertForm',
               panelId: 'removeViewingAlertPanel',
               submitButtonId: 'submitRemoveViewingAlert',
               statusId: 'removeViewingAlertStatus',
            }),
            ...createAnimalSpeciesRefs(doc, 'removeViewingAlert'),
         },
      },
      exhibits: {
         closed: {
            ...createFormRefs(doc, {
               showButtonId: 'showExhibitClosedForm',
               panelId: 'exhibitClosedPanel',
               submitButtonId: 'submitExhibitClosed',
               statusId: 'exhibitClosedStatus',
            }),
            exhibitEl: getById(doc, 'exhibitClosedExhibit'),
            ...createDateRangeRefs(doc, 'exhibitClosed'),
            messageEl: getById(doc, 'exhibitClosedMessage'),
         },
         open: {
            ...createFormRefs(doc, {
               showButtonId: 'showExhibitOpenForm',
               panelId: 'exhibitOpenPanel',
               submitButtonId: 'submitExhibitOpen',
               statusId: 'exhibitOpenStatus',
            }),
            exhibitEl: getById(doc, 'exhibitOpenExhibit'),
            ...createDateRangeRefs(doc, 'exhibitOpen'),
         },
      },
      restaurants: {
         closed: {
            ...createFormRefs(doc, {
               showButtonId: 'showRestaurantClosedForm',
               panelId: 'restaurantClosedPanel',
               submitButtonId: 'submitRestaurantClosed',
               statusId: 'restaurantClosedStatus',
            }),
            restaurantEl: getById(doc, 'restaurantClosedRestaurant'),
            ...createDateRangeRefs(doc, 'restaurantClosed'),
            messageEl: getById(doc, 'restaurantClosedMessage'),
         },
         open: {
            ...createFormRefs(doc, {
               showButtonId: 'showRestaurantOpenForm',
               panelId: 'restaurantOpenPanel',
               submitButtonId: 'submitRestaurantOpen',
               statusId: 'restaurantOpenStatus',
            }),
            restaurantEl: getById(doc, 'restaurantOpenRestaurant'),
            ...createWeeklyAvailabilityRefs(doc, 'restaurantOpen'),
            messageEl: getById(doc, 'restaurantOpenMessage'),
         },
      },
      giftShops: {
         closed: {
            ...createFormRefs(doc, {
               showButtonId: 'showGiftShopClosedForm',
               panelId: 'giftShopClosedPanel',
               submitButtonId: 'submitGiftShopClosed',
               statusId: 'giftShopClosedStatus',
            }),
            giftShopEl: getById(doc, 'giftShopClosedGiftShop'),
            ...createDateRangeRefs(doc, 'giftShopClosed'),
            messageEl: getById(doc, 'giftShopClosedMessage'),
         },
         open: {
            ...createFormRefs(doc, {
               showButtonId: 'showGiftShopOpenForm',
               panelId: 'giftShopOpenPanel',
               submitButtonId: 'submitGiftShopOpen',
               statusId: 'giftShopOpenStatus',
            }),
            giftShopEl: getById(doc, 'giftShopOpenGiftShop'),
            ...createWeeklyAvailabilityRefs(doc, 'giftShopOpen'),
            messageEl: getById(doc, 'giftShopOpenMessage'),
         },
      },
      attractions: {
         closed: {
            ...createFormRefs(doc, {
               showButtonId: 'showAttractionClosedForm',
               panelId: 'attractionClosedPanel',
               submitButtonId: 'submitAttractionClosed',
               statusId: 'attractionClosedStatus',
            }),
            attractionEl: getById(doc, 'attractionClosedAttraction'),
            ...createDateRangeRefs(doc, 'attractionClosed'),
            messageEl: getById(doc, 'attractionClosedMessage'),
         },
         open: {
            ...createFormRefs(doc, {
               showButtonId: 'showAttractionOpenForm',
               panelId: 'attractionOpenPanel',
               submitButtonId: 'submitAttractionOpen',
               statusId: 'attractionOpenStatus',
            }),
            attractionEl: getById(doc, 'attractionOpenAttraction'),
            ...createWeeklyAvailabilityRefs(doc, 'attractionOpen'),
            messageEl: getById(doc, 'attractionOpenMessage'),
         },
      },
      zoomobile: {
         stationClosed: {
            ...createFormRefs(doc, {
               showButtonId: 'showZoomobileStationClosedForm',
               panelId: 'zoomobileStationClosedPanel',
               submitButtonId: 'submitZoomobileStationClosed',
               statusId: 'zoomobileStationClosedStatus',
            }),
            zoomobileStationEl: getById(doc, 'zoomobileStationClosedZoomobileStation'),
            ...createDateRangeRefs(doc, 'zoomobileStationClosed'),
            messageEl: getById(doc, 'zoomobileStationClosedMessage'),
         },
         stationOpen: {
            ...createFormRefs(doc, {
               showButtonId: 'showZoomobileStationOpenForm',
               panelId: 'zoomobileStationOpenPanel',
               submitButtonId: 'submitZoomobileStationOpen',
               statusId: 'zoomobileStationOpenStatus',
            }),
            zoomobileStationEl: getById(doc, 'zoomobileStationOpenZoomobileStation'),
         },
         route: {
            ...createFormRefs(doc, {
               showButtonId: 'showZoomobileRouteForm',
               panelId: 'zoomobileRoutePanel',
               submitButtonId: 'submitZoomobileRoute',
               statusId: 'zoomobileRouteStatus',
            }),
            ...createDateRangeRefs(doc, 'zoomobileRoute'),
            summerRouteEl: getById(doc, 'zoomobileRouteSummer'),
            winterRouteEl: getById(doc, 'zoomobileRouteWinter'),
         },
      },
      guardiansTalks: {
         schedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showGuardiansTalkScheduleForm',
               panelId: 'guardiansTalkSchedulePanel',
               submitButtonId: 'submitGuardiansTalkSchedule',
               statusId: 'guardiansTalkScheduleStatus',
            }),
            locationEl: getById(doc, 'guardiansTalkScheduleLocation'),
            talkNameEl: getById(doc, 'guardiansTalkScheduleTalkName'),
            ...createDateRangeRefs(doc, 'guardiansTalkSchedule'),
            ...createWeekdayScheduleRefs(doc, 'guardiansTalkSchedule'),
            timeEl: getById(doc, 'guardiansTalkScheduleTime'),
            messageEl: getById(doc, 'guardiansTalkScheduleMessage'),
         },
         endSchedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showEndGuardiansTalkScheduleForm',
               panelId: 'endGuardiansTalkSchedulePanel',
               submitButtonId: 'submitEndGuardiansTalkSchedule',
               statusId: 'endGuardiansTalkScheduleStatus',
            }),
            locationEl: getById(doc, 'endGuardiansTalkScheduleLocation'),
            talkNameEl: getById(doc, 'endGuardiansTalkScheduleTalkName'),
            endDateEl: getById(doc, 'endGuardiansTalkScheduleEndDate'),
         },
         cancelOccurrence: {
            ...createFormRefs(doc, {
               showButtonId: 'showCancelGuardiansTalkOccurrenceForm',
               panelId: 'cancelGuardiansTalkOccurrencePanel',
               submitButtonId: 'submitCancelGuardiansTalkOccurrence',
               statusId: 'cancelGuardiansTalkOccurrenceStatus',
            }),
            locationEl: getById(doc, 'cancelGuardiansTalkOccurrenceLocation'),
            talkNameEl: getById(doc, 'cancelGuardiansTalkOccurrenceTalkName'),
            dateEl: getById(doc, 'cancelGuardiansTalkOccurrenceDate'),
            timeEl: getById(doc, 'cancelGuardiansTalkOccurrenceTime'),
         },
      },
      wildEncounters: {
         schedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showWildEncounterScheduleForm',
               panelId: 'wildEncounterSchedulePanel',
               submitButtonId: 'submitWildEncounterSchedule',
               statusId: 'wildEncounterScheduleStatus',
            }),
            wildEncounterEl: getById(doc, 'wildEncounterScheduleName'),
            ...createDateRangeRefs(doc, 'wildEncounterSchedule'),
            ...createWeekdayScheduleRefs(doc, 'wildEncounterSchedule'),
            timeEl: getById(doc, 'wildEncounterScheduleTime'),
            messageEl: getById(doc, 'wildEncounterScheduleMessage'),
         },
         endSchedule: {
            ...createFormRefs(doc, {
               showButtonId: 'showEndWildEncounterScheduleForm',
               panelId: 'endWildEncounterSchedulePanel',
               submitButtonId: 'submitEndWildEncounterSchedule',
               statusId: 'endWildEncounterScheduleStatus',
            }),
            wildEncounterEl: getById(doc, 'endWildEncounterScheduleName'),
            endDateEl: getById(doc, 'endWildEncounterScheduleDate'),
         },
         cancelOccurrence: {
            ...createFormRefs(doc, {
               showButtonId: 'showCancelWildEncounterOccurrenceForm',
               panelId: 'cancelWildEncounterOccurrencePanel',
               submitButtonId: 'submitCancelWildEncounterOccurrence',
               statusId: 'cancelWildEncounterOccurrenceStatus',
            }),
            wildEncounterEl: getById(doc, 'cancelWildEncounterOccurrenceName'),
            dateEl: getById(doc, 'cancelWildEncounterOccurrenceDate'),
            timeEl: getById(doc, 'cancelWildEncounterOccurrenceTime'),
         },
      },
   };
}
