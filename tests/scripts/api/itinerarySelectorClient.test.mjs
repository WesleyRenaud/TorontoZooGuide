import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySelectorClient } from '../../../scripts/api/itinerarySelectorClient.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';
import { ItinerarySelectorApiNormalizer } from '../../../scripts/api/itinerarySelectorApiNormalizer.js';

test('Test_GetExhibitsByRegion_TestResponse_ExpectNormalizedRegions', async () => {
   const originalPost = ApiClient.postJson;
   const originalNormalize = ItinerarySelectorApiNormalizer.normalizeRegion;
   ApiClient.postJson = async (url, payload) => {
      assert.equal(url, '/get-exhibits-by-region');
      assert.deepEqual(payload, { month: 'JUN' });
      return {
         regions: [{ name: 'Africa' }, { name: '' }],
      };
   };
   ItinerarySelectorApiNormalizer.normalizeRegion = (region) => region;

   try {
      assert.deepEqual(await ItinerarySelectorClient.getExhibitsByRegion({ month: 'JUN' }), [
         { name: 'Africa' },
      ]);
   } finally {
      ApiClient.postJson = originalPost;
      ItinerarySelectorApiNormalizer.normalizeRegion = originalNormalize;
   }
});

test('Test_GetAnimalsByExhibit_TestResponse_ExpectNormalizedAnimals', async () => {
   const originalPost = ApiClient.postJson;
   const originalNormalize = ItinerarySelectorApiNormalizer.normalizeAnimal;
   ApiClient.postJson = async (url, payload) => {
      assert.equal(url, '/get-animals-by-exhibit');
      assert.deepEqual(payload.exhibitsToInclude, ['Savanna']);
      return {
         animals: [{ species: 'Lion' }, { species: '' }],
      };
   };
   ItinerarySelectorApiNormalizer.normalizeAnimal = (animal) => animal;

   try {
      assert.deepEqual(
         await ItinerarySelectorClient.getAnimalsByExhibit(['Savanna'], { day: 15 }),
         [{ species: 'Lion' }]
      );
   } finally {
      ApiClient.postJson = originalPost;
      ItinerarySelectorApiNormalizer.normalizeAnimal = originalNormalize;
   }
});
