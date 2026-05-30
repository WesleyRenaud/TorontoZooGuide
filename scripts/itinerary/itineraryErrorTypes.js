import { APP_STRINGS } from '../strings.js';

let itineraryErrorTypes = null;
let suppressedItineraryErrorTypes = [];

export function updateItineraryErrorTypesFromConfig(itineraryConfig = {}) {
   const errorTypes = itineraryConfig?.errorTypes;

   if (errorTypes && typeof errorTypes === 'object') {
      itineraryErrorTypes = Object.freeze({ ...errorTypes });
   }

   suppressedItineraryErrorTypes = [...itineraryConfig.suppressedErrorTypes];
}

export function isItineraryErrorSuppressed(errorType) {
   return suppressedItineraryErrorTypes.includes(errorType);
}

export function getItineraryErrorTypes() {
   return itineraryErrorTypes;
}

export function isItinerarySuccess(errorType) {
   return errorType === itineraryErrorTypes?.SUCCESS;
}

export function requiresShortVisitConfirmation(errorType) {
   if (isItineraryErrorSuppressed(itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE)) {
      return false;
   }

   return errorType === itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE;
}

export function resolveItineraryErrorMessage(
   errorType,
   strings = APP_STRINGS.itinerary.errors
) {
   if (errorType === itineraryErrorTypes?.ARRIVAL_DEPARTURE_TOO_CLOSE) {
      return strings.arrivalDepartureTooClose;
   }

   return strings.generic;
}

function normalizeItineraryErrorType(errorType, legacySuccess) {
   if (typeof errorType === 'string' && errorType.trim()) {
      return errorType.trim();
   }

   if (legacySuccess === false) {
      return itineraryErrorTypes?.SAVE_FAILED ?? 'saveFailed';
   }

   return itineraryErrorTypes?.SUCCESS ?? 'success';
}

export function normalizeItineraryErrorTypeFromResponse(source = {}) {
   return normalizeItineraryErrorType(
      source.errorType ?? source.error_type,
      source.success
   );
}
