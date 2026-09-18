import assert from 'node:assert/strict';
import test from 'node:test';

import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../scripts/strings.js';

test('Test_PersistItineraryWarningSuppression_TestBlankType_ExpectNoOp', async () => {
   const requests = [];

   await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression('', {
      suppressWarning: async (warningType) => {
         requests.push(warningType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});

test('Test_PersistItineraryWarningSuppression_TestSuccess_ExpectResult', async () => {
   const response = { errorType: 'success', suppressed: true };

   const result = await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(
      'arrivalDepartureTooClose',
      {
         suppressWarning: async (warningType) => {
            assert.equal(warningType, 'arrivalDepartureTooClose');
            return response;
         },
         isSuccess: (errorType) => errorType === 'success',
      }
   );

   assert.deepEqual(result, response);
});

test('Test_PersistItineraryWarningSuppression_TestFailure_ExpectThrows', async () => {
   await assert.rejects(
      () => PersistItineraryWarningSuppressor.persistItineraryWarningSuppression('shortVisit', {
         suppressWarning: async () => ({ errorType: ItineraryErrorType.SAVE_FAILED }),
         isSuccess: () => false,
      }),
      { message: Strings.itinerary.errors.saveFailed }
   );
});

test('Test_PersistItineraryWarningUnsuppression_TestBlankType_ExpectNoOp', async () => {
   const requests = [];

   await PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression('', {
      unsuppressWarning: async (warningType) => {
         requests.push(warningType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});

test('Test_PersistItineraryWarningUnsuppression_TestSuccess_ExpectResult', async () => {
   const response = { errorType: 'success', suppressed: false };

   const result = await PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression(
      'arrivalDepartureTooClose',
      {
         unsuppressWarning: async (warningType) => {
            assert.equal(warningType, 'arrivalDepartureTooClose');
            return response;
         },
         isSuccess: (errorType) => errorType === 'success',
      }
   );

   assert.deepEqual(result, response);
});

test('Test_PersistItineraryWarningUnsuppression_TestFailure_ExpectThrows', async () => {
   await assert.rejects(
      () => PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression('shortVisit', {
         unsuppressWarning: async () => ({ errorType: ItineraryErrorType.SAVE_FAILED }),
         isSuccess: () => false,
      }),
      { message: Strings.itinerary.errors.saveFailed }
   );
});
