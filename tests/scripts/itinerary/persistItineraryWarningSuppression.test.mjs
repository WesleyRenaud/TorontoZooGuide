import assert from 'node:assert/strict';
import test from 'node:test';

import { PersistItineraryWarningSuppression } from '../../../scripts/itinerary/persistItineraryWarningSuppression.js';

test('Test_PersistItineraryWarningSuppression_TestBlankType_ExpectNoOp', async () => {
   const requests = [];

   await PersistItineraryWarningSuppression.persistItineraryWarningSuppression('', {
      suppressWarning: async (warningType) => {
         requests.push(warningType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});

test('Test_PersistItineraryWarningSuppression_TestSuccess_ExpectResult', async () => {
   const response = { errorType: 'success', suppressed: true };

   const result = await PersistItineraryWarningSuppression.persistItineraryWarningSuppression(
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
      () => PersistItineraryWarningSuppression.persistItineraryWarningSuppression('shortVisit', {
         suppressWarning: async () => ({ errorType: 'error' }),
         isSuccess: () => false,
      }),
      /Could not save itinerary warning preference/
   );
});
