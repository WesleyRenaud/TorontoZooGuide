import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { ItineraryServiceTimeRunner } from '../../../scripts/itinerary/itineraryServiceTimeRunner.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { EarlyAdmissionFragment } from '../../../scripts/itinerary/panel/earlyAdmissionFragment.js';
import { ShortVisitFragment } from '../../../scripts/itinerary/panel/shortVisitFragment.js';
import { VisitWindowOverflowFragment } from '../../../scripts/itinerary/panel/visitWindowOverflowFragment.js';
import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_CreateItineraryTimeChangeCancelledError_TestDefault_ExpectNamedError', () => {
   const error = ItineraryServiceTimeRunner.createItineraryTimeChangeCancelledError();

   assert.equal(error.name, 'ItineraryTimeChangeCancelledError');
   assert.match(error.message, /cancelled/i);
});


test('Test_RequestConfirmedItineraryTimeChange_TestBuildConfirmationOptions_ExpectMerged', async () => {
   const timeValue = '09:00 AM';
   const confirmationOptions = { confirmingShortVisit: false };
   const confirmingVisitWindowOverflow = true;
   const keptVisitWindowOverflowItems = [{ name: 'African Lion' }];
   const errorType = ItineraryErrorType.SUCCESS;

   const result = await ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange({
      showConfirmation: ({ onConfirm }) => onConfirm({
         keptVisitWindowOverflowItems,
      }),
      requestFn: async (time, options) => ({ errorType, time, options }),
      timeValue,
      confirmationOptions,
      buildConfirmationOptions: (confirmArg) => ({
         confirmingVisitWindowOverflow,
         keptVisitWindowOverflowItems: confirmArg.keptVisitWindowOverflowItems,
      }),
   });

   assert.equal(result.time, timeValue);
   assert.deepEqual(result.options, {
      ...confirmationOptions,
      confirmingVisitWindowOverflow,
      keptVisitWindowOverflowItems,
   });
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


test('Test_SetItineraryTimeWithConfirmation_TestOverflow_ExpectConfirmed', async () => {
   const originalIsSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalOverflow = ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation;
   const originalRequest = ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange;
   const requests = [];
   const timeValue = '11:00 AM';
   const issues = [{ type: ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS }];
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation = () => true;
   ItineraryServiceTimeRunner.requestConfirmedItineraryTimeChange = async (options) => {
      requests.push(options);
      return { confirmed: true };
   };

   try {
      const result = await ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation(
         async () => ({ issues }),
         timeValue
      );

      assert.equal(result.confirmed, true);
      assert.equal(
         requests[Position.FIRST].showConfirmation,
         VisitWindowOverflowFragment.showVisitWindowOverflowConfirmation
      );
      assert.deepEqual(requests[Position.FIRST].issues, issues);
   } finally {
      ItineraryErrorTypes.isItinerarySuccess = originalIsSuccess;
      ItineraryErrorTypes.requiresVisitWindowOverflowConfirmation = originalOverflow;
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
   const result = null;

   const validated = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(result);

   assert.equal(validated, null);
});


test('Test_BuildValidatedTimeSetItinerary_TestResult_ExpectNormalizedWithIssues', (t) => {
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   t.after(() => {
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
   });
   const issues = ['warn'];
   const normalized = { animals: [] };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;

   const validated = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary(
      { itinerary: { animals: [] }, issues }
   );

   assert.equal(validated, normalized);
   assert.deepEqual(validated.saveIssues, issues);
});


test('Test_SetItineraryTimeAndDispatch_TestValidated_ExpectDispatch', async () => {
   const originalSet = ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation;
   const originalBuild = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const dispatches = [];
   const validated = { validated: true };
   const timeValue = '10:00 AM';
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
      ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = originalSet;
      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = originalBuild;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});


test('Test_SetItineraryTimeAndDispatch_TestUnvalidated_ExpectRawResult', async () => {
   const originalSet = ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation;
   const originalBuild = ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const rawResult = { itinerary: { ok: true } };
   const timeValue = '10:00 AM';
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
      ItineraryServiceTimeRunner.setItineraryTimeWithConfirmation = originalSet;
      ItineraryServiceTimeRunner.buildValidatedTimeSetItinerary = originalBuild;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});
