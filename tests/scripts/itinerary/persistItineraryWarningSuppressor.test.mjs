import assert from 'node:assert/strict';
import test from 'node:test';

import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_PersistItineraryWarningSuppression_TestBlankType_ExpectNoOp', async () => {
   const requests = [];
   const warningType = '';

   await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(warningType, {
      suppressWarning: async (nextType) => {
         requests.push(nextType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});


test('Test_PersistItineraryWarningSuppression_TestSuccess_ExpectResult', async () => {
   const warningType = 'arrivalDepartureTooClose';
   const response = { errorType: 'success', suppressed: true };

   const result = await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(
      warningType,
      {
         suppressWarning: async (nextType) => {
            assert.equal(nextType, warningType);
            return response;
         },
         isSuccess: (errorType) => errorType === response.errorType,
      }
   );

   assert.deepEqual(result, response);
});


test('Test_PersistItineraryWarningSuppression_TestFailure_ExpectThrows', async () => {
   const warningType = 'shortVisit';

   await assert.rejects(
      () => PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(warningType, {
         suppressWarning: async () => ({ errorType: ItineraryErrorType.SAVE_FAILED }),
         isSuccess: () => false,
      }),
      { message: Strings.itinerary.errors.saveFailed }
   );
});


test('Test_PersistItineraryWarningUnsuppression_TestBlankType_ExpectNoOp', async () => {
   const requests = [];
   const warningType = '';

   await PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression(warningType, {
      unsuppressWarning: async (nextType) => {
         requests.push(nextType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});


test('Test_PersistItineraryWarningUnsuppression_TestSuccess_ExpectResult', async () => {
   const warningType = 'arrivalDepartureTooClose';
   const response = { errorType: 'success', suppressed: false };

   const result = await PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression(
      warningType,
      {
         unsuppressWarning: async (nextType) => {
            assert.equal(nextType, warningType);
            return response;
         },
         isSuccess: (errorType) => errorType === response.errorType,
      }
   );

   assert.deepEqual(result, response);
});


test('Test_PersistItineraryWarningUnsuppression_TestFailure_ExpectThrows', async () => {
   const warningType = 'shortVisit';

   await assert.rejects(
      () => PersistItineraryWarningSuppressor.persistItineraryWarningUnsuppression(warningType, {
         unsuppressWarning: async () => ({ errorType: ItineraryErrorType.SAVE_FAILED }),
         isSuccess: () => false,
      }),
      { message: Strings.itinerary.errors.saveFailed }
   );
});
