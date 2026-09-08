import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { ItineraryService } from './itineraryService.js';
import { ItineraryServiceSaveConfirmer } from './itineraryServiceSaveConfirmer.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidationResult } from './itineraryValidationResult.js';
import { ItineraryDiff } from './wizard/itineraryDiff.js';

export class ItineraryServiceSaver {
   static async saveItinerary(
   itinerary = {},
   {
      overridingConflictingGuardiansTalks = false,
      selectedExhibits = [],
   } = {},
) {
      const savePayload = ItineraryShape.toSetItineraryPayload(itinerary);
      const basePayload = {
         ...savePayload,
         selectedExhibits,
         temp: (await ItinerarySearchContext.getItineraryDateSearchContext({ date: savePayload.date })).temp,
         overridingConflictingGuardiansTalks,
      };

      const confirmationResult = await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations(basePayload);

      if (confirmationResult.cancelled) {
         return confirmationResult;
      }

      const { result, diffBaseline } = confirmationResult;

      if (!ItineraryErrorTypes.isItinerarySuccess(result.errorType)) {
         throw new Error(ItineraryErrorTypes.resolveItineraryErrorMessage(result.errorType));
      }

      const normalizedItinerary = ItineraryNormalizer.normalizeItineraryFromApiResult(result);
      const saveDiff = ItineraryDiff.buildItineraryDiff(
         ItineraryShape.normalizeItineraryDraft(diffBaseline ?? itinerary),
         normalizedItinerary,
         {},
         normalizedItinerary.itineraryConfig ?? {}
      );

      normalizedItinerary.saveIssues = result.issues;
      ItineraryValidationResult.applyItineraryDiffToValidation(
         normalizedItinerary,
         saveDiff,
         { adjustments: result.adjustments ?? [] });
      ItineraryService.dispatchItineraryUpdated(normalizedItinerary);

      return normalizedItinerary;
   }
}
