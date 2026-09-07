import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItineraryService } from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidationResult } from './itineraryValidationResult.js';
import { EarlyAdmissionConfirmation } from './panel/earlyAdmissionConfirmation.js';
import { ShortVisitConfirmation } from './panel/shortVisitConfirmation.js';
import { PersistItineraryWarningSuppression } from './persistItineraryWarningSuppression.js';
import { ItineraryDiff } from './wizard/itineraryDiff.js';

export class ItineraryServiceTimeRunner {
   static createItineraryTimeChangeCancelledError() {
      const error = new Error('Itinerary time change cancelled.');
      error.name = 'ItineraryTimeChangeCancelledError';
      return error;
   }

   static requestConfirmedItineraryTimeChange({
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
               reject(ItineraryServiceTimeRunner.createItineraryTimeChangeCancelledError());
            },
         });
      });
   }

   static async setItineraryTimeWithConfirmation(requestFn, timeValue) {
      const initialResult = await requestFn(timeValue);

      if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
         return initialResult;
      }

      if (ItineraryErrorTypes.requiresEarlyAdmissionConfirmation(initialResult.errorType)) {
         return ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
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

      return ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ShortVisitConfirmation.showShortVisitConfirmation,
         requestFn,
         timeValue,
         suppressionType: ItineraryErrorTypes.getItineraryErrorTypes()?.ARRIVAL_DEPARTURE_TOO_CLOSE,
         confirmationOptions: {
            confirmingShortVisit: true,
         },
      });
   }

   static buildValidatedTimeSetItinerary(previousItinerary, result) {
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

   static async setItineraryTimeAndDispatch(requestFn, timeValue) {
      const previousItinerary = await ItineraryService.getItinerary();
      const result = await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(requestFn, timeValue);
      const normalizedItinerary = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(
         previousItinerary,
         result
      );

      if (normalizedItinerary) {
         ItineraryService.dispatchItineraryUpdated(normalizedItinerary);
         return normalizedItinerary;
      }

      return result;
   }
}
