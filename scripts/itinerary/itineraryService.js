import {
   acceptItineraryRequest,
   bulkScheduleAnimalsRequest,
   clearItineraryRequest,
   getItineraryDateRequest,
   getItineraryRequest,
   getZooHoursRequest,
   setItineraryArrivalTimeRequest,
   setItineraryDepartureTimeRequest,
   setItineraryRequest,
} from '../api/itineraryApi.js';
import { setStoredItineraryDate } from './draftStorage.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
   requiresEarlyAdmissionConfirmation,
   requiresGuardiansTalkUnscheduleConfirmation,
   requiresGuardiansTalkWildEncounterTimeConflictConfirmation,
   requiresShortVisitConfirmation,
   requiresWildEncounterUnscheduleConfirmation,
   resolveItineraryErrorMessage,
} from './itineraryErrorTypes.js';
import { getItineraryDateSearchContext } from './itinerarySearchContext.js';
import {
   createEmptyItineraryDraft,
   isItineraryEmptyDraft,
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from './itineraryShape.js';
import { buildItineraryValidationState } from './itineraryValidation.js';
import { showEarlyAdmissionConfirmation } from './panel/earlyAdmissionConfirmation.js';
import { showGuardiansTalkUnscheduleConfirmation } from './panel/guardiansTalkUnscheduleConfirmation.js';
import { showScheduleTimeConflictConfirmation } from './panel/scheduleTimeConflictConfirmation.js';
import { showShortVisitConfirmation } from './panel/shortVisitConfirmation.js';
import { showWildEncounterUnscheduleConfirmation } from './panel/wildEncounterUnscheduleConfirmation.js';
import { persistItineraryWarningSuppression } from './persistItineraryWarningSuppression.js';
import {
   getDay,
   getMonth,
   getYear,
} from '../visitDates/visitDateRules.js';
import {
   buildItineraryDiff,
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
   mergeRemovedValidationState,
} from './wizard/itineraryDiff.js';
import { applyConflictSelectionToItineraryDraft } from './wizard/wildEncounterConflictResolution.js';

function createEmptyItinerary() {
   return {
      ...createEmptyItineraryDraft(),
      isActive: false,
   };
}

function normalizeItineraryItems(items) {
   return Array.isArray(items) ? items : [];
}

function normalizeItinerarySource(itinerary) {
   const source = itinerary && typeof itinerary === 'object'
      ? itinerary
      : {};

   return {
      date: source.date,
      arrivalTime: source.arrivalTime,
      departureTime: source.departureTime,
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
      events: normalizeItineraryItems(source.events),
   };
}

function dispatchItineraryUpdated(itinerary) {
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated', {
      detail: { itinerary },
   }));
}

export function isItineraryEmpty(itinerary) {
   return isItineraryEmptyDraft(
      normalizeItinerarySource(itinerary)
   );
}

export function normalizeItinerary(itinerary) {
   const normalizedDraft = normalizeItineraryDraft(
      normalizeItinerarySource(itinerary)
   );

   return {
      ...normalizedDraft,
      itineraryConfig: itinerary?.itineraryConfig ?? null,
      validation: buildItineraryValidationState(
         normalizedDraft,
         itinerary?.itineraryConfig ?? {}
      ),
      isActive: !isItineraryEmptyDraft(normalizedDraft),
   };
}

async function fetchSavedItineraryVisitDate() {
   const { date } = await getItineraryDateRequest();

   if (date) {
      setStoredItineraryDate(date);
   }

   return date;
}

export async function getItinerary() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await getItineraryRequest(temp);
   return normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
}

export async function getZooHours(date) {
   if (!date) {
      return null;
   }

   const month = getMonth(date);
   const day = getDay(date);
   const year = getYear(date);

   if (month == null || day == null || year == null) {
      return null;
   }

   const result = await getZooHoursRequest({ day, month, year });
   return result?.hours || null;
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

   const {
      result,
      diffBaseline,
   } = await requestSetItineraryWithConfirmations(basePayload);

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error(resolveItineraryErrorMessage(result.errorType));
   }

   const normalizedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
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
            resolve(createConfirmedSetItineraryResult(
               initialResult,
               diffBaseline,
            ));
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

function applyItineraryDiffToValidation(normalizedItinerary, diff, { adjustments = [] } = {}) {
   const validation = normalizedItinerary.validation;

   validation.unscheduled = diff.unscheduled;
   validation.removed = mergeRemovedValidationState(
      validation.removed,
      diff.removed);
   validation.adjustments = adjustments;
   validation.hasChanges = (
      hasAddedItems(validation.added)
      || hasRemovedItems(validation.removed)
      || hasUnscheduledItems(validation.unscheduled)
      || hasReducedVisibility(validation.reducedVisibility)
      || hasImprovedVisibility(validation.improvedVisibility)
      || validation.adjustments.length > 0
   );
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

export async function clearItinerary() {
   const result = await clearItineraryRequest();
   const clearedItinerary = createEmptyItinerary();

   window.dispatchEvent(new CustomEvent('tzg:itineraryCleared'));
   dispatchItineraryUpdated(clearedItinerary);

   return result;
}

export async function bulkScheduleAnimals() {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await bulkScheduleAnimalsRequest(temp);

   if (!isItinerarySuccess(result.errorType)) {
      throw new Error(resolveItineraryErrorMessage(result.errorType));
   }

   const normalizedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });
   dispatchItineraryUpdated(normalizedItinerary);

   return {
      itinerary: normalizedItinerary,
      issues: result.issues ?? [],
   };
}

export async function acceptItinerary({
   animalsToKeep = [],
   attractionsToKeep = [],
} = {}) {
   const date = await fetchSavedItineraryVisitDate();
   const { temp } = await getItineraryDateSearchContext({ date });
   const result = await acceptItineraryRequest(
      temp,
      { animalsToKeep, attractionsToKeep }
   );
   const acceptedItinerary = normalizeItinerary({
      ...result?.itinerary,
      itineraryConfig: result?.itineraryConfig,
   });

   dispatchItineraryUpdated(acceptedItinerary);

   return acceptedItinerary;
}

export async function hasActiveItinerary() {
   const itin = await getItinerary();
   return Boolean(itin.isActive) && !isItineraryEmpty(itin);
}
