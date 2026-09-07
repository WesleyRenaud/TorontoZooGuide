import { ItineraryApi } from '../api/itineraryApi.js';
import { ItineraryConfirmationResult } from './itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryShape } from './itineraryShape.js';
import { AttractionWithoutAnimalConfirmation } from './panel/attractionWithoutAnimalConfirmation.js';
import { FixedTimeItemLongWaitConfirmation } from './panel/fixedTimeItemLongWaitConfirmation.js';
import { GuardiansTalkUnscheduleConfirmation } from './panel/guardiansTalkUnscheduleConfirmation.js';
import { GuardiansTalkWithoutAnimalConfirmation } from './panel/guardiansTalkWithoutAnimalConfirmation.js';
import { ItineraryBuildWarningsConfirmation } from './panel/itineraryBuildWarningsConfirmation.js';
import { ScheduleTimeConflictConfirmation } from './panel/scheduleTimeConflictConfirmation.js';
import { WildEncounterUnscheduleConfirmation } from './panel/wildEncounterUnscheduleConfirmation.js';
import { WildEncounterConflictResolution } from './wizard/wildEncounterConflictResolution.js';

export class ItineraryServiceSaveConfirmations {
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
               const confirmedResult = await ItineraryServiceSaveConfirmations.requestSetItineraryWithConfirmations(
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
      const initialResult = await ItineraryApi.setItineraryRequest(payload);

      if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmations.createConfirmedSetItineraryResult(initialResult, diffBaseline);
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkWildEncounterTimeConflictConfirmation(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: ScheduleTimeConflictConfirmation.showScheduleTimeConflictConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: (selectedItems) => {
               const resultPayload = ItineraryServiceSaveConfirmations.getSetItineraryResultPayload(initialResult);
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

      if (ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings(initialResult.issues)) {
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: () => ({
               ...payload,
               ...ItineraryBuildWarningsConfirmation.buildConfirmedOptionsFromBuildWarnings(initialResult.issues),
            }),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: GuardiansTalkUnscheduleConfirmation.showGuardiansTalkUnscheduleConfirmation,
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
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation,
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
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: AttractionWithoutAnimalConfirmation.showAttractionWithoutAnimalConfirmation,
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
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation,
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
         return ItineraryServiceSaveConfirmations.requestSetItineraryConfirmation({
            showConfirmation: WildEncounterUnscheduleConfirmation.showWildEncounterUnscheduleConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: () => ({
               ...payload,
               confirmingWildEncounterUnschedule: true,
            }),
         });
      }

      return ItineraryServiceSaveConfirmations.createConfirmedSetItineraryResult(initialResult, diffBaseline);
   }
}
