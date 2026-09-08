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

test('Test_SaveItinerary_TestCancelledConfirmation_ExpectCancelledResult', async () => {
   const originalPayload = ItineraryShape.toSetItineraryPayload;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalConfirm = ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations;
   const cancelled = { cancelled: true };

   ItineraryShape.toSetItineraryPayload = () => ({ date: '2026-06-15' });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: false });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async () => cancelled;

   try {
      assert.equal(
         await ItineraryServiceSaver.saveItinerary({ date: '2026-06-15' }, {
            selectedExhibits: ['Africa'],
            overridingConflictingGuardiansTalks: true,
         }),
         cancelled
      );
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

   ItineraryShape.toSetItineraryPayload = () => ({ date: '2026-06-15' });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async () => ({
      cancelled: false,
      result: { errorType: 'boom' },
      diffBaseline: null,
   });
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => 'save failed';

   try {
      await assert.rejects(
         () => ItineraryServiceSaver.saveItinerary({ date: '2026-06-15' }),
         /save failed/
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
   const dispatches = [];
   const applyCalls = [];
   const normalized = { date: '2026-06-15', itineraryConfig: { a: 1 } };

   ItineraryShape.toSetItineraryPayload = () => ({ date: '2026-06-15' });
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: true });
   ItineraryServiceSaveConfirmer.requestSetItineraryWithConfirmations = async (payload) => {
      assert.deepEqual(payload.selectedExhibits, []);
      assert.equal(payload.temp, true);
      return {
         cancelled: false,
         result: {
            errorType: 'success',
            issues: ['issue'],
            adjustments: [{ kind: 'trim' }],
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
      const result = await ItineraryServiceSaver.saveItinerary({ date: '2026-06-15' });
      assert.equal(result, normalized);
      assert.deepEqual(result.saveIssues, ['issue']);
      assert.equal(dispatches.length, 1);
      assert.deepEqual(applyCalls[0][2], { adjustments: [{ kind: 'trim' }] });
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
