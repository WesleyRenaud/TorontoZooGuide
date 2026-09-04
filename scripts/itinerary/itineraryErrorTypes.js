import { APP_STRINGS } from '../strings.js';

let itineraryErrorTypes = null;
let suppressedItineraryErrorTypes = [];

function normalizeItineraryErrorType(errorType, legacySuccess) {
   if (typeof errorType === 'string' && errorType.trim()) {
      return errorType.trim();
   }

   if (legacySuccess === false) {
      return itineraryErrorTypes?.SAVE_FAILED;
   }

   return itineraryErrorTypes?.SUCCESS;
}

export class ItineraryErrorTypes {
   static updateItineraryErrorTypesFromConfig(itineraryConfig = {}) {
      const errorTypes = itineraryConfig?.errorTypes;

      if (errorTypes && typeof errorTypes === 'object') {
         itineraryErrorTypes = Object.freeze({ ...errorTypes });
      }

      suppressedItineraryErrorTypes = [...itineraryConfig.suppressedErrorTypes];
   }

   static isItineraryErrorSuppressed(errorType) {
      return suppressedItineraryErrorTypes.includes(errorType);
   }

   static getItineraryErrorTypes() {
      return itineraryErrorTypes;
   }

   static isItinerarySuccess(errorType) {
      return errorType === itineraryErrorTypes?.SUCCESS;
   }

   static requiresShortVisitConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE
      )) {
         return false;
      }

      return errorType === itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE;
   }

   static requiresEarlyAdmissionConfirmation(errorType) {
      if (
         ItineraryErrorTypes.isItineraryErrorSuppressed(
            itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
         )
      ) {
         return false;
      }

      return errorType === itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;
   }

   static requiresScheduleItemNotOnItineraryConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY
      )) {
         return false;
      }

      return errorType === itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY;
   }

   static requiresAttractionOutsideOperatingHoursConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.ATTRACTION_OUTSIDE_OPERATING_HOURS;
   }

   static requiresGuardiansTalkUnscheduleConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresFixedTimeItemLongWaitConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static requiresGuardiansTalkWithoutAnimalConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.GUARDIANS_TALK_WITHOUT_ANIMAL;
   }

   static requiresAttractionWithoutAnimalConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.ATTRACTION_WITHOUT_ANIMAL;
   }

   static requiresWildEncounterUnscheduleConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresGuardiansTalkWildEncounterTimeConflictConfirmation(errorType) {
      return errorType === itineraryErrorTypes?.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT;
   }

   static resolveItineraryErrorMessage(
      errorType,
      strings = APP_STRINGS.itinerary.errors
   ) {
      if (errorType === itineraryErrorTypes?.ITINERARY_DATE_NOT_SET) {
         return strings.itineraryDateNotSet;
      }

      if (errorType === itineraryErrorTypes?.SAVE_FAILED) {
         return strings.saveFailed;
      }

      if (errorType === itineraryErrorTypes?.TIME_ORDER_INVALID) {
         return strings.timeOrderInvalid;
      }

      if (errorType === itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE) {
         return strings.arrivalDepartureTooClose;
      }

      if (errorType === itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP) {
         return strings.earlyAdmissionRequiresMembership;
      }

      if (errorType === itineraryErrorTypes?.NO_AVAILABLE_SLOT) {
         return strings.noAvailableSlot;
      }

      if (errorType === itineraryErrorTypes?.REQUESTED_TIME_NOT_AVAILABLE) {
         return strings.requestedTimeNotAvailable;
      }

      if (errorType === itineraryErrorTypes?.ATTRACTION_OUTSIDE_OPERATING_HOURS) {
         return strings.attractionOutsideOperatingHours;
      }

      if (errorType === itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY) {
         return strings.itemNotOnItinerary;
      }

      if (errorType === itineraryErrorTypes?.ITEM_ALREADY_SCHEDULED) {
         return strings.itemAlreadyScheduled;
      }

      if (errorType === itineraryErrorTypes?.TIME_OUT_OF_BOUNDS) {
         return strings.timeOutOfBounds;
      }

      if (errorType === itineraryErrorTypes?.ACTIVITY_NOT_ON_DAY_SCHEDULE) {
         return strings.activityNotOnDaySchedule;
      }

      if (errorType === itineraryErrorTypes?.SCHEDULE_WINDOW_UNAVAILABLE) {
         return strings.scheduleWindowUnavailable;
      }

      if (errorType === itineraryErrorTypes?.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED) {
         return strings.bulkScheduleItineraryAlreadyScheduled;
      }

      if (errorType === itineraryErrorTypes?.UNSCHEDULE_ALL_NOTHING_SCHEDULED) {
         return strings.unscheduleAllNothingScheduled;
      }

      return strings.generic;
   }

   static normalizeItineraryErrorTypeFromResponse(source = {}) {
      return normalizeItineraryErrorType(
         source.status,
         source.success
      );
   }
}
