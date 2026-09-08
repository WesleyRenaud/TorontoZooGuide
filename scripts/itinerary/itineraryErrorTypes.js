import { ItineraryErrorTypesHelpers } from './itineraryErrorTypesHelpers.js';
import { Strings } from '../strings.js';

export class ItineraryErrorTypes {
   static itineraryErrorTypes = null;

   static suppressedItineraryErrorTypes = [];

   static updateItineraryErrorTypesFromConfig(itineraryConfig = {}) {
      const errorTypes = itineraryConfig?.errorTypes;

      if (errorTypes && typeof errorTypes === 'object') {
         ItineraryErrorTypes.itineraryErrorTypes = Object.freeze({ ...errorTypes });
      }

      ItineraryErrorTypes.suppressedItineraryErrorTypes = [...itineraryConfig.suppressedErrorTypes];
   }

   static isItineraryErrorSuppressed(errorType) {
      return ItineraryErrorTypes.suppressedItineraryErrorTypes.includes(errorType);
   }

   static getItineraryErrorTypes() {
      return ItineraryErrorTypes.itineraryErrorTypes;
   }

   static isItinerarySuccess(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.SUCCESS;
   }

   static requiresShortVisitConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         ItineraryErrorTypes.itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE
      )) {
         return false;
      }

      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE;
   }

   static requiresEarlyAdmissionConfirmation(errorType) {
      if (
         ItineraryErrorTypes.isItineraryErrorSuppressed(
            ItineraryErrorTypes.itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
         )
      ) {
         return false;
      }

      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;
   }

   static requiresScheduleItemNotOnItineraryConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         ItineraryErrorTypes.itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY
      )) {
         return false;
      }

      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY;
   }

   static requiresAttractionOutsideOperatingHoursConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.ATTRACTION_OUTSIDE_OPERATING_HOURS;
   }

   static requiresGuardiansTalkUnscheduleConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresFixedTimeItemLongWaitConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static requiresGuardiansTalkWithoutAnimalConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.GUARDIANS_TALK_WITHOUT_ANIMAL;
   }

   static requiresAttractionWithoutAnimalConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.ATTRACTION_WITHOUT_ANIMAL;
   }

   static requiresWildEncounterUnscheduleConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresGuardiansTalkWildEncounterTimeConflictConfirmation(errorType) {
      return errorType === ItineraryErrorTypes.itineraryErrorTypes?.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT;
   }

   static resolveItineraryErrorMessage(
      errorType,
      strings = Strings.itinerary.errors
   ) {
      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ITINERARY_DATE_NOT_SET) {
         return strings.itineraryDateNotSet;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.SAVE_FAILED) {
         return strings.saveFailed;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.TIME_ORDER_INVALID) {
         return strings.timeOrderInvalid;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE) {
         return strings.arrivalDepartureTooClose;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP) {
         return strings.earlyAdmissionRequiresMembership;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.NO_AVAILABLE_SLOT) {
         return strings.noAvailableSlot;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.REQUESTED_TIME_NOT_AVAILABLE) {
         return strings.requestedTimeNotAvailable;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ATTRACTION_OUTSIDE_OPERATING_HOURS) {
         return strings.attractionOutsideOperatingHours;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ITEM_NOT_ON_ITINERARY) {
         return strings.itemNotOnItinerary;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ITEM_ALREADY_SCHEDULED) {
         return strings.itemAlreadyScheduled;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.TIME_OUT_OF_BOUNDS) {
         return strings.timeOutOfBounds;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.ACTIVITY_NOT_ON_DAY_SCHEDULE) {
         return strings.activityNotOnDaySchedule;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.SCHEDULE_WINDOW_UNAVAILABLE) {
         return strings.scheduleWindowUnavailable;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED) {
         return strings.bulkScheduleItineraryAlreadyScheduled;
      }

      if (errorType === ItineraryErrorTypes.itineraryErrorTypes?.UNSCHEDULE_ALL_NOTHING_SCHEDULED) {
         return strings.unscheduleAllNothingScheduled;
      }

      return strings.generic;
   }

   static normalizeItineraryErrorTypeFromResponse(source = {}) {
      return ItineraryErrorTypesHelpers.normalizeItineraryErrorType(
         source.status,
         source.success
      );
   }
}
