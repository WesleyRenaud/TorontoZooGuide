import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDiff } from '../../../scripts/itinerary/wizard/itineraryDiff.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { ItineraryServiceTimeRunner } from '../../../scripts/itinerary/itineraryServiceTimeRunner.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { ItineraryValidationResult } from '../../../scripts/itinerary/itineraryValidationResult.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { ShortVisitFragment } from '../../../scripts/itinerary/panel/shortVisitFragment.js';
import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_CreateItineraryTimeChangeCancelledError_TestDefault_ExpectNamedError', () => {
   const error = ItineraryServiceTimeRunner.createItineraryTimeChangeCancelledError();

   assert.equal(error.name, 'ItineraryTimeChangeCancelledError');
   assert.match(error.message, /cancelled/i);
});


test('Test_RequestConfirmedItineraryTimeChange_TestConfirmSuccess_ExpectResolved', async () => {
   const originalPersist = PersistItineraryWarningSuppressor.persistItineraryWarningSuppression;
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const persists = [];
   const timeValue = '09:00 AM';
   const suppressionType = 'EARLY';
   const confirmationOptions = { confirmingEarlyAdmission: true };
   const errorType = 'SUCCESS';
   PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = async (type) => {
      persists.push(type);
   };
   ItineraryErrorTypes.isItinerarySuccess = () => true;

   try {
      const result = await ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ({ onConfirm }) => onConfirm({ doNotShowAgain: true }),
         requestFn: async (time, options) => ({ errorType, time, options }),
         timeValue,
         suppressionType,
         confirmationOptions,
      });

      assert.equal(result.errorType, errorType);
      assert.equal(result.time, timeValue);
      assert.deepEqual(result.options, confirmationOptions);
      assert.deepEqual(persists, [suppressionType]);
   } finally {
      PersistItineraryWarningSuppressor.persistItineraryWarningSuppression = originalPersist;
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
   }
});


test('Test_RequestConfirmedItineraryTimeChange_TestCancel_ExpectRejected', async () => {
   const timeValue = '09:00 AM';

   await assert.rejects(
      () => ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
         showConfirmation: ({ onCancel }) => onCancel(),
         requestFn: async () => ({}),
         timeValue,
         suppressionType: 'EARLY',
         confirmationOptions: {},
      }),
      (error) => error.name === 'ItineraryTimeChangeCancelledError'
   );
});


test('Test_RequestConfirmedItineraryTimeChange_TestFailure_ExpectRejected', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const message = 'failed';
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => message;

   try {
      await assert.rejects(
         () => ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
            showConfirmation: ({ onConfirm }) => onConfirm({}),
            requestFn: async () => ({ errorType: 'SAVE_FAILED' }),
            timeValue: '09:00 AM',
            suppressionType: 'EARLY',
            confirmationOptions: {},
         }),
         new RegExp(message)
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
   }
});


test('Test_RequestConfirmedItineraryTimeChange_TestPersistFailure_ExpectRejected', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const message = 'persist boom';
   ItineraryErrorTypes.isItinerarySuccess = () => false;

   try {
      await assert.rejects(
         () => ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
            showConfirmation: ({ onConfirm }) => onConfirm({}),
            requestFn: async () => {
               throw new Error(message);
            },
            timeValue: '09:00 AM',
            suppressionType: 'EARLY',
            confirmationOptions: {},
         }),
         new RegExp(message)
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
   }
});


test('Test_SetItineraryTimeWithConfirmation_TestSuccess_ExpectResult', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const errorType = 'SUCCESS';
   const timeValue = '10:00 AM';
   ItineraryErrorTypes.isItinerarySuccess = () => true;

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(
         async () => ({ errorType }),
         timeValue
      );

      assert.equal(result.errorType, errorType);
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
   }
});


test('Test_SetItineraryTimeWithConfirmation_TestEarlyAdmission_ExpectConfirmed', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalEarly = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation;
   const originalRequest = ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange;
   const requests = [];
   const timeValue = '8:00 AM';
   const suppressionType = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = () => true;
   ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = async (options) => {
      requests.push(options);
      return { confirmed: true, via: options.suppressionType };
   };

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(
         async () => ({}),
         timeValue
      );

      assert.equal(result.confirmed, true);
      assert.equal(result.via, suppressionType);
      assert.equal(
         requests[Position.FIRST].showConfirmation,
         EarlyAdmissionFragment.showEarlyAdmissionConfirmation
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = originalEarly;
      ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = originalRequest;
   }
});


test('Test_SetItineraryTimeWithConfirmation_TestShortVisit_ExpectConfirmed', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalEarly = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation;
   const originalShort = ItineraryErrorTypes.requiresShortVisitConfirmation;
   const originalRequest = ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange;
   const requests = [];
   const timeValue = '3:00 PM';
   const suppressionType = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = () => false;
   ItineraryErrorTypes.requiresShortVisitConfirmation = () => true;
   ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = async (options) => {
      requests.push(options);
      return { confirmed: true, via: options.suppressionType };
   };

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(
         async () => ({}),
         timeValue
      );

      assert.equal(result.confirmed, true);
      assert.equal(result.via, suppressionType);
      assert.equal(
         requests[Position.FIRST].showConfirmation,
         ShortVisitFragment.showShortVisitConfirmation
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = originalEarly;
      ItineraryErrorTypes.requiresShortVisitConfirmation = originalShort;
      ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = originalRequest;
   }
});


test('Test_SetItineraryTimeWithConfirmation_TestHardFail_ExpectRejected', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalEarly = ItineraryErrorTypes.requiresEarlyAdmissionConfirmation;
   const originalShort = ItineraryErrorTypes.requiresShortVisitConfirmation;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const message = 'hard fail';
   const timeValue = '1:00 PM';
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = () => false;
   ItineraryErrorTypes.requiresShortVisitConfirmation = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => message;

   try {
      await assert.rejects(
         () => ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(async () => ({}), timeValue),
         new RegExp(message)
      );
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresEarlyAdmissionConfirmation = originalEarly;
      ItineraryErrorTypes.requiresShortVisitConfirmation = originalShort;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
   }
});


test('Test_BuildValidatedTimeSetItinerary_TestNullResult_ExpectNull', () => {
   const previousItinerary = {};
   const result = null;

   const validated = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(
      previousItinerary,
      result
   );

   assert.equal(validated, null);
});


test('Test_BuildValidatedTimeSetItinerary_TestResult_ExpectNormalizedDiff', () => {
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalShape = ItineraryShape.normalizeItineraryDraft;
   const originalDiff = ItineraryDiff.buildItineraryDiff;
   const originalApply = ItineraryValidationResult.applyItineraryDiffToValidation;
   const applies = [];
   const issues = ['warn'];
   const diff = { changed: true };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({
      animals: [],
      itineraryConfig: { a: 1 },
   });
   ItineraryShape.normalizeItineraryDraft = (draft) => ({ ...draft, shaped: true });
   ItineraryDiff.buildItineraryDiff = () => diff;
   ItineraryValidationResult.applyItineraryDiffToValidation = (itinerary, nextDiff) => {
      applies.push({ itinerary, diff: nextDiff });
   };

   try {
      const validated = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(
         { previous: true },
         { itinerary: { animals: [] }, issues }
      );

      assert.deepEqual(validated.saveIssues, issues);
      assert.deepEqual(applies[Position.FIRST].diff, diff);
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
   const validated = { validated: true };
   const timeValue = '10:00 AM';
   ItineraryService.getItinerary = async () => ({ previous: true });
   ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = async () => ({ itinerary: { ok: true } });
   ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = () => validated;
   ItineraryService.dispatchItineraryUpdated = (itinerary) => dispatches.push(itinerary);

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         async () => ({}),
         timeValue
      );

      assert.equal(result, validated);
      assert.deepEqual(dispatches, [validated]);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = originalSet;
      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = originalBuild;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});


test('Test_SetItineraryTimeAndDispatch_TestUnvalidated_ExpectRawResult', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalSet = ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation;
   const originalBuild = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const rawResult = { itinerary: { ok: true } };
   const timeValue = '10:00 AM';
   ItineraryService.getItinerary = async () => ({ previous: true });
   ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = async () => rawResult;
   ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = () => null;
   ItineraryService.dispatchItineraryUpdated = () => {};

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeAndDispatch(
         async () => ({}),
         timeValue
      );

      assert.equal(result, rawResult);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = originalSet;
      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = originalBuild;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});
