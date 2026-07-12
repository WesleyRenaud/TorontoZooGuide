import { setItineraryRequest } from '../api/itineraryApi.js';
import {
   isItinerarySuccess,
   requiresGuardiansTalkLongWaitConfirmation,
   requiresGuardiansTalkUnscheduleConfirmation,
   requiresGuardiansTalkWildEncounterTimeConflictConfirmation,
   requiresGuardiansTalkWithoutAnimalConfirmation,
   requiresWildEncounterUnscheduleConfirmation,
   resolveItineraryErrorMessage,
} from './itineraryErrorTypes.js';
import { normalizeItineraryFromApiResult } from './itineraryNormalization.js';
import { getItineraryDateSearchContext } from './itinerarySearchContext.js';
import { dispatchItineraryUpdated } from './itineraryService.js';
import {
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from './itineraryShape.js';
import { applyItineraryDiffToValidation } from './itineraryValidationResult.js';
import { showGuardiansTalkLongWaitConfirmation } from './panel/guardiansTalkLongWaitConfirmation.js';
import { showGuardiansTalkUnscheduleConfirmation } from './panel/guardiansTalkUnscheduleConfirmation.js';
import { showGuardiansTalkWithoutAnimalConfirmation } from './panel/guardiansTalkWithoutAnimalConfirmation.js';
import {
   buildConfirmedOptionsFromBuildWarnings,
   hasMultipleItineraryBuildWarnings,
   showItineraryBuildWarningsConfirmation,
} from './panel/itineraryBuildWarningsConfirmation.js';
import { showScheduleTimeConflictConfirmation } from './panel/scheduleTimeConflictConfirmation.js';
import { showWildEncounterUnscheduleConfirmation } from './panel/wildEncounterUnscheduleConfirmation.js';
import { buildItineraryDiff } from './wizard/itineraryDiff.js';
import { applyConflictSelectionToItineraryDraft } from './wizard/wildEncounterConflictResolution.js';

function createConfirmedSetItineraryResult(result, diffBaseline = null) {
   return {
      result,
      diffBaseline,
   };
}

function getSetItineraryResultPayload(result) {
   return result?.itinerary
      ? toSetItineraryPayload(result.itinerary)
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
            resolve({
               cancelled: true,
               diffBaseline,
            });
         },
      });
   });
}

async function requestSetItineraryWithConfirmations(
   payload,
   diffBaseline = null,
) {
   const initialResult = await setItineraryRequest(payload);

   if (isItinerarySuccess(initialResult.errorType)) {
      return createConfirmedSetItineraryResult(initialResult, diffBaseline);
   }

   if (requiresGuardiansTalkWildEncounterTimeConflictConfirmation(initialResult.errorType)) {
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
            } = applyConflictSelectionToItineraryDraft(
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

   if (requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
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

   if (requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
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

   if (requiresGuardiansTalkLongWaitConfirmation(initialResult.errorType)) {
      return requestSetItineraryConfirmation({
         showConfirmation: showGuardiansTalkLongWaitConfirmation,
         initialResult,
         payload,
         diffBaseline,
         buildConfirmedPayload: () => ({
            ...payload,
            confirmingGuardiansTalkLongWait: true,
         }),
      });
   }

   if (requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
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
   const savePayload = toSetItineraryPayload(itinerary);
   const basePayload = {
      ...savePayload,
      selectedExhibits,
      temp: (await getItineraryDateSearchContext({ date: savePayload.date })).temp,
      overridingConflictingGuardiansTalks,
   };

   const confirmationResult = await requestSetItineraryWithConfirmations(basePayload);

   if (confirmationResult.cancelled) {
      return null;
   }

   const { result, diffBaseline } = confirmationResult;

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error(resolveItineraryErrorMessage(result.errorType));
   }

   const normalizedItinerary = normalizeItineraryFromApiResult(result);
   const saveDiff = buildItineraryDiff(
      normalizeItineraryDraft(diffBaseline ?? itinerary),
      normalizedItinerary,
      {},
      normalizedItinerary.itineraryConfig ?? {}
   );

   normalizedItinerary.saveIssues = result.issues;
   applyItineraryDiffToValidation(
      normalizedItinerary,
      saveDiff,
      { adjustments: result.adjustments ?? [] });
   dispatchItineraryUpdated(normalizedItinerary);

   return normalizedItinerary;
}
