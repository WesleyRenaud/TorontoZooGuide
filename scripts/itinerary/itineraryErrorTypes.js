import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryConfirmationRegistry } from './itineraryConfirmationRegistry.js';
import { ItineraryErrorType } from '../shared/enums/itineraryErrorType.js';
import { Strings } from '../strings.js';

export class ItineraryErrorTypes {
   static suppressedItineraryErrorTypes = [];

   static ITINERARY_ERROR_MESSAGE_KEYS = Object.freeze({
      [ItineraryErrorType.ITINERARY_DATE_NOT_SET]: 'itineraryDateNotSet',
      [ItineraryErrorType.SAVE_FAILED]: 'saveFailed',
      [ItineraryErrorType.TIME_ORDER_INVALID]: 'timeOrderInvalid',
      [ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE]: 'arrivalDepartureTooClose',
      [ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP]: 'earlyAdmissionRequiresMembership',
      [ItineraryErrorType.NO_AVAILABLE_SLOT]: 'noAvailableSlot',
      [ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE]: 'requestedTimeNotAvailable',
      [ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS]: 'attractionOutsideOperatingHours',
      [ItineraryErrorType.ITEM_NOT_ON_ITINERARY]: 'itemNotOnItinerary',
      [ItineraryErrorType.ITEM_ALREADY_SCHEDULED]: 'itemAlreadyScheduled',
      [ItineraryErrorType.TIME_OUT_OF_BOUNDS]: 'timeOutOfBounds',
      [ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE]: 'activityNotOnDaySchedule',
      [ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE]: 'scheduleWindowUnavailable',
      [ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED]: 'bulkScheduleItineraryAlreadyScheduled',
      [ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED]: 'unscheduleAllNothingScheduled',
   });

   static syncSuppressedItineraryErrorTypes(itineraryConfig = {}) {
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
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorTypes.isItineraryErrorSuppressed
      );
   }

   static requiresEarlyAdmissionConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
         ItineraryErrorTypes.isItineraryErrorSuppressed
      );
   }

   static requiresScheduleItemNotOnItineraryConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         ItineraryErrorTypes.isItineraryErrorSuppressed
      );
   }

   static requiresAttractionOutsideOperatingHoursConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS
      );
   }

   static requiresGuardiansTalkUnscheduleConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
      );
   }

   static requiresFixedTimeItemLongWaitConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
      );
   }

   static requiresGuardiansTalkWithoutAnimalConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
      );
   }

   static requiresAttractionWithoutAnimalConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
      );
   }

   static requiresWildEncounterUnscheduleConfirmation(errorType) {
      return ItineraryConfirmationRegistry.requiresConfirmation(
         errorType,
         ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
      );
   }

   static requiresGuardiansTalkWildEncounterTimeConflictConfirmation(errorType) {
      return errorType === ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT;
   }

   static resolveItineraryErrorMessage(
      errorType,
      strings = Strings.itinerary.errors
   ) {
      const messageKey = ItineraryErrorTypes.ITINERARY_ERROR_MESSAGE_KEYS[errorType];

      if (messageKey) {
         return strings[messageKey];
      }

      return strings.generic;
   }

   static normalizeItineraryErrorType(errorType, legacySuccess) {
      const normalizedErrorType = ValueNormalizer.asTrimmedString(errorType);

      if (normalizedErrorType) {
         return normalizedErrorType;
      }

      if (legacySuccess === false) {
         return ItineraryErrorType.SAVE_FAILED;
      }

      return ItineraryErrorType.SUCCESS;
   }

   static normalizeItineraryErrorTypeFromResponse(source = {}) {
      return ItineraryErrorTypes.normalizeItineraryErrorType(
         source.status,
         source.success
      );
   }
}
