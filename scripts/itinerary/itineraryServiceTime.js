import {
   setItineraryArrivalTimeRequest,
   setItineraryDepartureTimeRequest,
} from '../api/itineraryApi.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
   requiresEarlyAdmissionConfirmation,
   requiresShortVisitConfirmation,
   resolveItineraryErrorMessage,
} from './itineraryErrorTypes.js';
import { normalizeItinerary } from './itineraryNormalization.js';
import {
   dispatchItineraryUpdated,
   getItinerary,
} from './itineraryService.js';
import { normalizeItineraryDraft } from './itineraryShape.js';
import { applyItineraryDiffToValidation } from './itineraryValidationResult.js';
import { showEarlyAdmissionConfirmation } from './panel/earlyAdmissionConfirmation.js';
import { showShortVisitConfirmation } from './panel/shortVisitConfirmation.js';
import { persistItineraryWarningSuppression } from './persistItineraryWarningSuppression.js';
import { buildItineraryDiff } from './wizard/itineraryDiff.js';

class ItineraryTimeChangeCancelledError extends Error {
   constructor() {
      super('Itinerary time change cancelled.');
      this.name = 'ItineraryTimeChangeCancelledError';
   }
}

function requestConfirmedItineraryTimeChange({
   showConfirmation,
   requestFn,
   timeValue,
   suppressionType,
   confirmationOptions,
}) {
   return new Promise((resolve, reject) => {
      showConfirmation({
         onConfirm: async ({ doNotShowAgain = false } = {}) => {
            try {
               if (doNotShowAgain) {
                  await persistItineraryWarningSuppression(suppressionType);
               }

               const confirmedResult = await requestFn(
                  timeValue,
                  confirmationOptions
               );

               if (!isItinerarySuccess(confirmedResult.errorType)) {
                  reject(new Error(
                     resolveItineraryErrorMessage(confirmedResult.errorType)
                  ));
                  return;
               }

               resolve(confirmedResult);
            }
            catch (error) {
               reject(error);
            }
         },
         onCancel: () => {
            reject(new ItineraryTimeChangeCancelledError());
         },
      });
   });
}

async function setItineraryTimeWithConfirmation(requestFn, timeValue) {
   const initialResult = await requestFn(timeValue);

   if (isItinerarySuccess(initialResult.errorType)) {
      return initialResult;
   }

   if (requiresEarlyAdmissionConfirmation(initialResult.errorType)) {
      return requestConfirmedItineraryTimeChange({
         showConfirmation: showEarlyAdmissionConfirmation,
         requestFn,
         timeValue,
         suppressionType: (
            getItineraryErrorTypes()?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
         ),
         confirmationOptions: {
            confirmingEarlyAdmission: true,
         },
      });
   }

   if (!requiresShortVisitConfirmation(initialResult.errorType)) {
      throw new Error(resolveItineraryErrorMessage(initialResult.errorType));
   }

   return requestConfirmedItineraryTimeChange({
      showConfirmation: showShortVisitConfirmation,
      requestFn,
      timeValue,
      suppressionType: getItineraryErrorTypes()?.ARRIVAL_DEPARTURE_TOO_CLOSE,
      confirmationOptions: {
         confirmingShortVisit: true,
      },
   });
}

function buildValidatedTimeSetItinerary(previousItinerary, result) {
   if (!result?.itinerary) {
      return null;
   }

   const normalizedItinerary = normalizeItinerary({
      ...result.itinerary,
      itineraryConfig: result.itineraryConfig,
   });
   const timeDiff = buildItineraryDiff(
      normalizeItineraryDraft(previousItinerary),
      normalizedItinerary,
      {},
      normalizedItinerary.itineraryConfig ?? {}
   );

   normalizedItinerary.saveIssues = result.issues;
   applyItineraryDiffToValidation(
      normalizedItinerary,
      timeDiff,
      { adjustments: result.adjustments ?? [] });

   return normalizedItinerary;
}

async function setItineraryTimeAndDispatch(requestFn, timeValue) {
   const previousItinerary = await getItinerary();
   const result = await setItineraryTimeWithConfirmation(requestFn, timeValue);
   const normalizedItinerary = buildValidatedTimeSetItinerary(
      previousItinerary,
      result
   );

   if (normalizedItinerary) {
      dispatchItineraryUpdated(normalizedItinerary);
      return normalizedItinerary;
   }

   return result;
}

export async function setItineraryArrivalTime(arrivalTime) {
   return setItineraryTimeAndDispatch(
      setItineraryArrivalTimeRequest,
      arrivalTime
   );
}

export async function setItineraryDepartureTime(departureTime) {
   return setItineraryTimeAndDispatch(
      setItineraryDepartureTimeRequest,
      departureTime
   );
}
