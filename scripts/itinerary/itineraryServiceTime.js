import { ItineraryApi } from '../api/itineraryApi.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import {
   dispatchItineraryUpdated,
   getItinerary,
} from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidationResult } from './itineraryValidationResult.js';
import { EarlyAdmissionConfirmation } from './panel/earlyAdmissionConfirmation.js';
import { ShortVisitConfirmation } from './panel/shortVisitConfirmation.js';
import { PersistItineraryWarningSuppression } from './persistItineraryWarningSuppression.js';
import { ItineraryDiff } from './wizard/itineraryDiff.js';

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
                  await PersistItineraryWarningSuppression.persistItineraryWarningSuppression(suppressionType);
               }

               const confirmedResult = await requestFn(
                  timeValue,
                  confirmationOptions
               );

               if (!ItineraryErrorTypes.isItinerarySuccess(confirmedResult.errorType)) {
                  reject(new Error(
                     ItineraryErrorTypes.resolveItineraryErrorMessage(confirmedResult.errorType)
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

   if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
      return initialResult;
   }

   if (ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(initialResult.errorType)) {
      return requestConfirmedItineraryTimeChange({
         showConfirmation: EarlyAdmissionConfirmation.showEarlyAdmissionConfirmation,
         requestFn,
         timeValue,
         suppressionType: (
            ItineraryErrorTypes.getItineraryErrorTypes()?.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
         ),
         confirmationOptions: {
            confirmingEarlyAdmission: true,
         },
      });
   }

   if (!ItineraryErrorTypes.requiresShortVisitConfirmation(initialResult.errorType)) {
      throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(initialResult.errorType));
   }

   return requestConfirmedItineraryTimeChange({
      showConfirmation: ShortVisitConfirmation.showShortVisitConfirmation,
      requestFn,
      timeValue,
      suppressionType: ItineraryErrorTypes.getItineraryErrorTypes()?.ARRIVAL_DEPARTURE_TOO_CLOSE,
      confirmationOptions: {
         confirmingShortVisit: true,
      },
   });
}

function buildValidatedTimeSetItinerary(previousItinerary, result) {
   if (!result?.itinerary) {
      return null;
   }

   const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);
   const timeDiff = ItineraryDiff.buildItineraryDiff(
      ItineraryShape.normalizeItineraryDraft(previousItinerary),
      normalizedItinerary,
      {},
      normalizedItinerary.itineraryConfig ?? {}
   );

   normalizedItinerary.saveIssues = result.issues;
   ItineraryValidationResult.applyItineraryDiffToValidation(normalizedItinerary, timeDiff);

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
      ItineraryApi.setItineraryArrivalTimeRequest,
      arrivalTime
   );
}

export async function setItineraryDepartureTime(departureTime) {
   return setItineraryTimeAndDispatch(
      ItineraryApi.setItineraryDepartureTimeRequest,
      departureTime
   );
}
