import assert from 'node:assert/strict';
import test from 'node:test';

import { persistItineraryWarningSuppression } from '../../scripts/itinerary/persistItineraryWarningSuppression.js';

test('persistItineraryWarningSuppression no-ops for blank warning types', async () => {
   const requests = [];

   await persistItineraryWarningSuppression('', {
      suppressWarning: async (warningType) => {
         requests.push(warningType);
         return { errorType: 'success' };
      },
   });

   assert.equal(requests.length, 0);
});

test('persistItineraryWarningSuppression returns the API result on success', async () => {
   const response = { errorType: 'success', suppressed: true };

   const result = await persistItineraryWarningSuppression(
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

test('persistItineraryWarningSuppression throws when the API reports failure', async () => {
   await assert.rejects(
      () => persistItineraryWarningSuppression('shortVisit', {
         suppressWarning: async () => ({ errorType: 'error' }),
         isSuccess: () => false,
      }),
      /Could not save itinerary warning preference/
   );
});
