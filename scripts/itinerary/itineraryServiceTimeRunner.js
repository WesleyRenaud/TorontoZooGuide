import { ItineraryConfirmationRegistry } from './itineraryConfirmationRegistry.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItineraryService } from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidationResult } from './itineraryValidationResult.js';
import { PersistItineraryWarningSuppressor } from './persistItineraryWarningSuppressor.js';
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
                     await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(suppressionType);
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

      for (const entry of ItineraryConfirmationRegistry.getTimeChangeConfirmationEntries()) {
         if (ItineraryErrorTypes[entry.requiresMethod](initialResult.errorType)) {
            return ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
               requestFn,
               timeValue,
               ...ItineraryConfirmationRegistry.buildTimeChangeConfirmationOptions(entry),
            });
         }
      }

      throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(initialResult.errorType));
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
