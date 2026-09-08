import assert from 'node:assert/strict';
import test from 'node:test';

import { PersistItineraryWarningSuppressor } from '../../../scripts/itinerary/persistItineraryWarningSuppressor.js';

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
         suppressWarning: async () => ({ errorType: 'error' }),
         isSuccess: () => false,
      }),
      /Could not save itinerary warning preference/
   );
});
