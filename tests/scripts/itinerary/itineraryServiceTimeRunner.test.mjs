import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDiff } from '../../../scripts/itinerary/wizard/itineraryDiff.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { ItineraryServiceTimeRunner } from '../../../scripts/itinerary/itineraryServiceTimeRunner.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { ItineraryValidationResult } from '../../../scripts/itinerary/itineraryValidationResult.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { ShortVisitFragment } from '../../../scripts/itinerary/panel/shortVisitFragment.js';
import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';

test('Test_CreateItineraryTimeChangeCancelledError_TestDefault_ExpectNamedError', () => {
   const error = ItineraryServiceTimeRunner.createItineraryTimeChangeCancelledError();
   assert.equal(error.name, 'ItineraryTimeChangeCancelledError');
   assert.match(error.message, /cancelled/i);
});

test('Test_RequestConfirmedItineraryTimeChange_TestConfirmSuccess_ExpectResolved', async () => {
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const persists = [];

   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async (type) => {
      persists.push(type);
   };
   ItineraryErrorTypes.isItinerarySuccess = () => true;

   try {
      const result = await ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ({ onConfirm }) => onConfirm({ doNotShowAgain: true }),
         requestFn: async (time, options) => ({ errorType: 'SUCCESS', time, options }),
         timeValue: '09:00 AM',
         suppressionType: 'EARLY',
         confirmationOptions: { confirmingEarlyAdmission: true },
      });

      assert.deepEqual(result, {
         errorType: 'SUCCESS',
         time: '09:00 AM',
         options: { confirmingEarlyAdmission: true },
      });
      assert.deepEqual(persists, ['EARLY']);
   } finally {
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
   }
});

test('Test_RequestConfirmedItineraryTimeChange_TestCancelAndFailure_ExpectRejected', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => 'failed';

   await assert.rejects(
      () => ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ({ onCancel }) => onCancel(),
         requestFn: async () => ({}),
         timeValue: '09:00 AM',
         suppressionType: 'EARLY',
         confirmationOptions: {},
      }),
      (error) => error.name === 'ItineraryTimeChangeCancelledError'
   );

   await assert.rejects(
      () => ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ({ onConfirm }) => onConfirm({}),
         requestFn: async () => ({ errorType: 'SAVE_FAILED' }),
         timeValue: '09:00 AM',
         suppressionType: 'EARLY',
         confirmationOptions: {},
      }),
      /failed/
   );

   ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
   ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
});

test('Test_SetItineraryTimeWithConfirmation_TestBranches_ExpectFlows', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalEarly = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation;
   const originalShort = ItineraryErrorTypes.requiresShortVisitConfirmation;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const originalGetTypes = ItineraryErrorTypes.getItineraryErrorTypes;
   const originalRequest = ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange;
   const originalEarlyShow = EarlyAdmissionFragment.showEarlyAdmissionConfirmation;
   const originalShortShow = ShortVisitFragment.showShortVisitConfirmation;
   const requests = [];

   ItineraryErrorTypes.getItineraryErrorTypes = () => ({
      EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'EARLY',
      ARRIVAL_DEPARTURE_TOO_CLOSE: 'SHORT',
   });
   ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = async (options) => {
      requests.push(options);
      return { confirmed: true, via: options.suppressionType };
   };

   try {
      ItineraryErrorTypes.isItinerarySuccess = () => true;
      assert.deepEqual(
         await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(
            async () => ({ errorType: 'SUCCESS' }),
            '10:00 AM'
         ),
         { errorType: 'SUCCESS' }
      );

      ItineraryErrorTypes.isItinerarySuccess = () => false;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = () => true;
      assert.deepEqual(
         await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(async () => ({}), '8:00 AM'),
         { confirmed: true, via: 'EARLY' }
      );
      assert.equal(requests[0].showConfirmation, EarlyAdmissionFragment.showEarlyAdmissionConfirmation);

      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = () => false;
      ItineraryErrorTypes.requiresShortVisitConfirmation = () => true;
      assert.deepEqual(
         await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(async () => ({}), '3:00 PM'),
         { confirmed: true, via: 'SHORT' }
      );
      assert.equal(requests[1].showConfirmation, ShortVisitFragment.showShortVisitConfirmation);

      ItineraryErrorTypes.requiresShortVisitConfirmation = () => false;
      ItineraryErrorTypes.resolveItineraryErrorMessage = () => 'hard fail';
      await assert.rejects(
         () => ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(async () => ({}), '1:00 PM'),
         /hard fail/
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = originalEarly;
      ItineraryErrorTypes.requiresShortVisitConfirmation = originalShort;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
      ItineraryErrorTypes.getItineraryErrorTypes = originalGetTypes;
      ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = originalRequest;
      EarlyAdmissionFragment.showEarlyAdmissionConfirmation = originalEarlyShow;
      ShortVisitFragment.showShortVisitConfirmation = originalShortShow;
   }
});

test('Test_BuildValidatedTimeSetItinerary_TestResult_ExpectNormalizedDiff', () => {
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalShape = ItineraryShape.normalizeItineraryDraft;
   const originalDiff = ItineraryDiff.buildItineraryDiff;
   const originalApply = ItineraryValidationResult.applyItineraryDiffToValidation;
   const applies = [];

   ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({
      animals: [],
      itineraryConfig: { a: 1 },
   });
   ItineraryShape.normalizeItineraryDraft = (draft) => ({ ...draft, shaped: true });
   ItineraryDiff.buildItineraryDiff = () => ({ changed: true });
   ItineraryValidationResult.applyItineraryDiffToValidation = (itinerary, diff) => {
      applies.push({ itinerary, diff });
   };

   try {
      assert.equal(ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary({}, null), null);

      const validated = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(
         { previous: true },
         { itinerary: { animals: [] }, issues: ['warn'] }
      );

      assert.deepEqual(validated.saveIssues, ['warn']);
      assert.deepEqual(applies[0].diff, { changed: true });
   } finally {
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryShape.normalizeItineraryDraft = originalShape;
      ItineraryDiff.buildItineraryDiff = originalDiff;
      ItineraryValidationResult.applyItineraryDiffToValidation = originalApply;
   }
});

test('Test_SetItineraryTimeAndDispatch_TestValidated_ExpectDispatch', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalSet = ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation;
   const originalBuild = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const dispatches = [];

   ItineraryService.getItinerary = async () => ({ previous: true });
   ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = async () => ({ itinerary: { ok: true } });
   ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = () => ({ validated: true });
   ItineraryService.dispatchItineraryUpdated = (itinerary) => dispatches.push(itinerary);

   try {
      assert.deepEqual(
         await ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(async () => ({}), '10:00 AM'),
         { validated: true }
      );
      assert.deepEqual(dispatches, [{ validated: true }]);

      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = () => null;
      assert.deepEqual(
         await ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(async () => ({}), '10:00 AM'),
         { itinerary: { ok: true } }
      );
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = originalSet;
      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = originalBuild;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});
