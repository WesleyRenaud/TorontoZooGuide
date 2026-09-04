import { ItineraryApi } from '../api/itineraryApi.js';
import { ItineraryConfirmationResult } from './itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryNormalizer } from './itineraryNormalizer.js';
import { ItinerarySearchContext } from './itinerarySearchContext.js';
import { dispatchItineraryUpdated } from './itineraryService.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryValidationResult } from './itineraryValidationResult.js';
import { showAttractionWithoutAnimalConfirmation } from './panel/attractionWithoutAnimalConfirmation.js';
import { showFixedTimeItemLongWaitConfirmation } from './panel/fixedTimeItemLongWaitConfirmation.js';
import { showGuardiansTalkUnscheduleConfirmation } from './panel/guardiansTalkUnscheduleConfirmation.js';
import { showGuardiansTalkWithoutAnimalConfirmation } from './panel/guardiansTalkWithoutAnimalConfirmation.js';
import {
   buildConfirmedOptionsFromBuildWarnings,
   hasMultipleItineraryBuildWarnings,
   showItineraryBuildWarningsConfirmation,
} from './panel/itineraryBuildWarningsConfirmation.js';
import { showScheduleTimeConflictConfirmation } from './panel/scheduleTimeConflictConfirmation.js';
import { showWildEncounterUnscheduleConfirmation } from './panel/wildEncounterUnscheduleConfirmation.js';
import { ItineraryDiff } from './wizard/itineraryDiff.js';
import { WildEncounterConflictResolution } from './wizard/wildEncounterConflictResolution.js';

function createConfirmedSetItineraryResult(result, diffBaseline = null) {
   return {
      result,
      diffBaseline,
   };
}

function getSetItineraryResultPayload(result) {
   return result?.itinerary
      ? ItineraryShape.toSetItineraryPayload(result.itinerary)
      : {};
}

function requestSetItineraryConfirmation({
   showConfirmation,
   initialResult,
   payload,
   diffBaseline,
   buildConfirmedPayload,
   getConfirmedDiffBaseline = () => diffBaseline,
}) {
   return new Promise((resolve) => {
      showConfirmation({
         issues: initialResult.issues,
         onConfirm: async (...confirmationArgs) => {
            const confirmedPayload = buildConfirmedPayload(...confirmationArgs);
            const confirmedResult = await requestSetItineraryWithConfirmations(
               confirmedPayload,
               getConfirmedDiffBaseline(confirmedPayload)
            );

            resolve(confirmedResult);
         },
         onCancel: () => {
            resolve(ItineraryConfirmationResult.createItineraryConfirmationCancelledResult({
               issues: initialResult.issues,
            }));
         },
      });
   });
}
async function requestSetItineraryWithConfirmations(
   payload,
   diffBaseline = null,
) {
   const initialResult = await ItineraryApi.setItineraryRequest(payload);

   if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
      return createConfirmedSetItineraryResult(initialResult, diffBaseline);
   }

   if (ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showScheduleTimeConflictConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: (selectedItems) => {
            const resultPayload = getSetItineraryResultPayload(initialResult);
            const {
               guardiansTalks,
               wildEncounters,
            } = WildEncounterConflictResolution.applyConflictSelectionToItineraryDraft(
               {
                  guardiansTalks: payload.guardiansTalks,
                  wildEncounters: payload.wildEncounters,
               },
               initialResult.issues,
               selectedItems
            );

            return {
               ...payload,
               animals: resultPayload.animals ?? payload.animals,
               attractions: resultPayload.attractions ?? payload.attractions,
               guardiansTalks,
               wildEncounters,
               overridingConflictingGuardiansTalks: true,
            };
         },
         getConfirmedDiffBaseline: (confirmedPayload) => confirmedPayload,
      });
   }

   if (hasMultipleItineraryBuildWarnings(initialResult.issues)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showItineraryBuildWarningsConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            ...buildConfirmedOptionsFromBuildWarnings(initialResult.issues),
         }),
      });
   }

   if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showGuardiansTalkUnscheduleConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingGuardiansTalkUnschedule: true,
         }),
      });
   }

   if (ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showGuardiansTalkWithoutAnimalConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingGuardiansTalkWithoutAnimal: true,
         }),
      });
   }

   if (ItineraryErrorTypes.requiresAttractionWithoutAnimalConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showAttractionWithoutAnimalConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingAttractionWithoutAnimal: true,
         }),
      });
   }

   if (ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showFixedTimeItemLongWaitConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingFixedTimeItemLongWait: true,
         }),
      });
   }

   if (ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showWildEncounterUnscheduleConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingWildEncounterUnschedule: true,
         }),
      });
   }

   return createConfirmedSetItineraryResult(initialResult, diffBaseline);
}

export async function saveItinerary(
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

   const confirmationResult = await requestSetItineraryWithConfirmations(basePayload);

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
   dispatchItineraryUpdated(normalizedItinerary);

   return normalizedItinerary;
}
