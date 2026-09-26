import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDiff } from '../../../scripts/itinerary/wizard/itineraryDiff.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { ItinerarySearchContext } from '../../../scripts/itinerary/itinerarySearchContext.js';
import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { ItineraryServiceSaveConfirmer } from '../../../scripts/itinerary/itineraryServiceSaveConfirmer.js';
import { ItineraryServiceSaver } from '../../../scripts/itinerary/itineraryServiceSaver.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { ItineraryValidationResult } from '../../../scripts/itinerary/itineraryValidationResult.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_SaveItinerary_TestCancelledConfirmation_ExpectCancelledResult', async () => {
   const originalPayload = ItineraryShape.toSetItineraryPayload;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const date = '2026-06-15';
   const selectedExhibits = ['Africa'];
   const cancelled = { cancelled: true };
   ItineraryShape.toSetItineraryPayload = () => ({ date });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: false });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async () => cancelled;

   try {
      const result = await ItineraryServiceSaver.saveItinerary({ date }, {
         selectedExhibits,
         overridingConflictingGuardiansTalks: true,
      });

      assert.equal(result, cancelled);
   } finally {
      ItineraryShape.toSetItineraryPayload = originalPayload;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalConfirm;
   }
});


test('Test_SaveItinerary_TestVisitTimeConfirmations_ExpectPayloadFlags', async () => {
   const originalPayload = ItineraryShape.toSetItineraryPayload;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const date = '2026-06-15';
   const confirmingShortVisit = true;
   const confirmingEarlyAdmission = true;
   const payloads = [];
   ItineraryShape.toSetItineraryPayload = () => ({ date });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: false });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async (payload) => {
      payloads.push(payload);
      return { cancelled: true };
   };

   try {
      await ItineraryServiceSaver.saveItinerary({ date }, {
         confirmingShortVisit,
         confirmingEarlyAdmission,
      });

      assert.equal(payloads[Position.FIRST].confirmingShortVisit, confirmingShortVisit);
      assert.equal(payloads[Position.FIRST].confirmingEarlyAdmission, confirmingEarlyAdmission);
   } finally {
      ItineraryShape.toSetItineraryPayload = originalPayload;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalConfirm;
   }
});


test('Test_SaveItinerary_TestErrorType_ExpectThrowsResolvedMessage', async () => {
   const originalPayload = ItineraryShape.toSetItineraryPayload;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const date = '2026-06-15';
   const message = 'save failed';
   ItineraryShape.toSetItineraryPayload = () => ({ date });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async () => ({
      cancelled: false,
      result: { errorType: 'boom' },
      diffBaseline: null,
   });
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => message;

   try {
      await assert.rejects(
         () => ItineraryServiceSaver.saveItinerary({ date }),
         new RegExp(message)
      );
   } finally {
      ItineraryShape.toSetItineraryPayload = originalPayload;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalConfirm;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
   }
});


test('Test_SaveItinerary_TestSuccess_ExpectNormalizedDispatch', async () => {
   const originalPayload = ItineraryShape.toSetItineraryPayload;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDraft = ItineraryShape.normalizeItineraryDraft;
   const originalDiff = ItineraryDiff.buildItineraryDiff;
   const originalApply = ItineraryValidationResult.applyItineraryDiffToValidation;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const date = '2026-06-15';
   const issues = ['issue'];
   const adjustment = { kind: 'trim' };
   const dispatches = [];
   const applyCalls = [];
   const normalized = { date, itineraryConfig: { a: 1 } };
   ItineraryShape.toSetItineraryPayload = () => ({ date });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: true });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async (payload) => {
      assert.deepEqual(payload.selectedExhibits, []);
      assert.equal(payload.temp, true);
      return {
         cancelled: false,
         result: {
            errorType: 'success',
            issues,
            adjustments: [adjustment],
         },
         diffBaseline: { date: '2026-06-14' },
      };
   };
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;
   ItineraryShape.normalizeItineraryDraft = (draft) => draft;
   ItineraryDiff.buildItineraryDiff = () => ({ removed: [] });
   ItineraryValidationResult.applyItineraryDiffToValidation = (...args) => {
      applyCalls.push(args);
   };
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };

   try {
      const result = await ItineraryServiceSaver.saveItinerary({ date });

      assert.equal(result, normalized);
      assert.deepEqual(result.saveIssues, issues);
      assert.equal(dispatches.length, 1);
      assert.deepEqual(applyCalls[Position.FIRST][Position.THIRD], { adjustments: [adjustment] });
   } finally {
      ItineraryShape.toSetItineraryPayload = originalPayload;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = originalConfirm;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryShape.normalizeItineraryDraft = originalDraft;
      ItineraryDiff.buildItineraryDiff = originalDiff;
      ItineraryValidationResult.applyItineraryDiffToValidation = originalApply;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});
