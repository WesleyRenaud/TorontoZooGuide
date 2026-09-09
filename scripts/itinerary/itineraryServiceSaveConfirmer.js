import { ItineraryClient } from '../api/itineraryClient.js';
import { ItineraryConfirmationRegistry } from './itineraryConfirmationRegistry.js';
import { ItineraryConfirmationResult } from './itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryBuildWarningsFragment } from './panel/itineraryBuildWarningsFragment.js';
import { ScheduleTimeConflictFragment } from './panel/scheduleTimeConflictFragment.js';
import { WildEncounterConflictResolver } from './wizard/wildEncounterConflictResolver.js';

export class ItineraryServiceSaveConfirmer {
   static createConfirmedSetItineraryResult(result, diffBaseline = null) {
      return {
         result,
         diffBaseline,
      };
   }

   static getSetItineraryResultPayload(result) {
      return result?.itinerary
         ? ItineraryShape.toSetItineraryPayload(result.itinerary)
         : {};
   }

   static requestSetItineraryConfirmation({
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
               const confirmedResult = await ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations(
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

   static async requestSetItineraryWithConfirmations(
      payload,
      diffBaseline = null,
   ) {
      const initialResult = await ItineraryClient.setItineraryRequest(payload);

      if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmer.createConfirmedSetItineraryResult(initialResult, diffBaseline);
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: (selectedItems) => {
               const resultPayload = ItineraryServiceSaveConfirmer.getSetItineraryResultPayload(initialResult);
               const {
                  guardiansTalks,
                  wildEncounters,
               } = WildEncounterConflictResolver.applyConflictSelectionToItineraryDraft(
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

      if (ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(initialResult.issues)) {
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: () => ({
               ...payload,
               ...ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings(initialResult.issues),
            }),
         });
      }

      for (const entry of ItineraryConfirmationRegistry.getSetItineraryConfirmationEntries()) {
         if (ItineraryErrorTypes[entry.requiresMethod](initialResult.errorType)) {
            return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
               showConfirmation: entry.showConfirmation,
               initialResult,
               payload,
               diffBaseline,
               buildConfirmedPayload: ItineraryConfirmationRegistry.buildConfirmedPayload(entry, payload),
            });
         }
      }

      return ItineraryServiceSaveConfirmer.createConfirmedSetItineraryResult(initialResult, diffBaseline);
   }
}
