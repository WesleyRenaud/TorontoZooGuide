import { ItineraryErrorTypesHelper } from './itineraryErrorTypesHelper.js';
import { ItineraryErrorType } from '../shared/enums/itineraryErrorType.js';
import { Strings } from '../strings.js';

export class ItineraryErrorTypes {
   static suppressedItineraryErrorTypes = [];

   static updateItineraryErrorTypesFromConfig(itineraryConfig = {}) {
      ItineraryErrorTypes.suppressedItineraryErrorTypes = [
         ...(itineraryConfig?.suppressedErrorTypes ?? []),
      ];
   }

   static isItineraryErrorSuppressed(errorType) {
      return ItineraryErrorTypes.suppressedItineraryErrorTypes.includes(errorType);
   }

   static isItinerarySuccess(errorType) {
      return errorType === ItineraryErrorType.SUCCESS;
   }

   static requiresShortVisitConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
      )) {
         return false;
      }

      return errorType === ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   }

   static requiresEarlyAdmissionConfirmation(errorType) {
      if (
         ItineraryErrorTypes.isItineraryErrorSuppressed(
            ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
         )
      ) {
         return false;
      }

      return errorType === ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;
   }

   static requiresScheduleItemNotOnItineraryConfirmation(errorType) {
      if (ItineraryErrorTypes.isItineraryErrorSuppressed(
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY
      )) {
         return false;
      }

      return errorType === ItineraryErrorType.ITEM_NOT_ON_ITINERARY;
   }

   static requiresAttractionOutsideOperatingHoursConfirmation(errorType) {
      return errorType === ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS;
   }

   static requiresGuardiansTalkUnscheduleConfirmation(errorType) {
      return errorType === ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresFixedTimeItemLongWaitConfirmation(errorType) {
      return errorType === ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT;
   }

   static requiresGuardiansTalkWithoutAnimalConfirmation(errorType) {
      return errorType === ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL;
   }

   static requiresAttractionWithoutAnimalConfirmation(errorType) {
      return errorType === ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL;
   }

   static requiresWildEncounterUnscheduleConfirmation(errorType) {
      return errorType === ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS;
   }

   static requiresGuardiansTalkWildEncounterTimeConflictConfirmation(errorType) {
      return errorType === ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT;
   }

   static resolveItineraryErrorMessage(
      errorType,
      strings = Strings.itinerary.errors
   ) {
      if (errorType === ItineraryErrorType.ITINERARY_DATE_NOT_SET) {
         return strings.itineraryDateNotSet;
      }

      if (errorType === ItineraryErrorType.SAVE_FAILED) {
         return strings.saveFailed;
      }

      if (errorType === ItineraryErrorType.TIME_ORDER_INVALID) {
         return strings.timeOrderInvalid;
      }

      if (errorType === ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE) {
         return strings.arrivalDepartureTooClose;
      }

      if (errorType === ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP) {
         return strings.earlyAdmissionRequiresMembership;
      }

      if (errorType === ItineraryErrorType.NO_AVAILABLE_SLOT) {
         return strings.noAvailableSlot;
      }

      if (errorType === ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE) {
         return strings.requestedTimeNotAvailable;
      }

      if (errorType === ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS) {
         return strings.attractionOutsideOperatingHours;
      }

      if (errorType === ItineraryErrorType.ITEM_NOT_ON_ITINERARY) {
         return strings.itemNotOnItinerary;
      }

      if (errorType === ItineraryErrorType.ITEM_ALREADY_SCHEDULED) {
         return strings.itemAlreadyScheduled;
      }

      if (errorType === ItineraryErrorType.TIME_OUT_OF_BOUNDS) {
         return strings.timeOutOfBounds;
      }

      if (errorType === ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE) {
         return strings.activityNotOnDaySchedule;
      }

      if (errorType === ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE) {
         return strings.scheduleWindowUnavailable;
      }

      if (errorType === ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED) {
         return strings.bulkScheduleItineraryAlreadyScheduled;
      }

      if (errorType === ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED) {
         return strings.unscheduleAllNothingScheduled;
      }

      return strings.generic;
   }

   static normalizeItineraryErrorTypeFromResponse(source = {}) {
      return ItineraryErrorTypesHelper.normalizeItineraryErrorType(
         source.status,
         source.success
      );
   }
}
