import { ItineraryClient } from '../api/itineraryClient.js';
import { ItineraryConfirmationResult } from './itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from './itineraryErrorTypes.js';
import { ItineraryShape } from './itineraryShape.js';
import { AttractionWithoutAnimalFragment } from './panel/attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from './panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from './panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from './panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsFragment } from './panel/itineraryBuildWarningsFragment.js';
import { ScheduleTimeConflictFragment } from './panel/scheduleTimeConflictFragment.js';
import { WildEncounterUnscheduleFragment } from './panel/wildEncounterUnscheduleFragment.js';
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

      if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation,
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
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation,
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
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: AttractionWithoutAnimalFragment.showAttractionWithoutAnimalConfirmation,
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
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
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
         return ItineraryServiceSaveConfirmer.requestSetItineraryConfirmation({
            showConfirmation: WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation,
            initialResult,
            payload,
            diffBaseline,
            buildConfirmedPayload: () => ({
               ...payload,
               confirmingWildEncounterUnschedule: true,
            }),
         });
      }

      return ItineraryServiceSaveConfirmer.createConfirmedSetItineraryResult(initialResult, diffBaseline);
   }
}
