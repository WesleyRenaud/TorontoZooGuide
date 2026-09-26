import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySelectorClient } from '../../../scripts/api/itinerarySelectorClient.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';
import { ItinerarySelectorApiNormalizer } from '../../../scripts/api/itinerarySelectorApiNormalizer.js';


test('Test_GetExhibitsByRegion_TestResponse_ExpectNormalizedRegions', async () => {
   const month = 'JUN';
   const africa = { name: 'Africa' };
   const unnamed = { name: '' };
   const url = '/get-exhibits-by-region';
   const originalPost = ApiClient.postJson;
   const originalNormalize = ItinerarySelectorApiNormalizer.normalizeRegion;
   ApiClient.postJson = async (postedUrl, payload) => {
      assert.equal(postedUrl, url);
      assert.deepEqual(payload, { month });
      return {
         regions: [africa, unnamed],
      };
   };
   ItinerarySelectorApiNormalizer.normalizeRegion = (region) => region;

   try {
      const regions = await ItinerarySelectorClient.getExhibitsByRegion({ month });

      assert.deepEqual(regions, [africa]);
   } finally {
      ApiClient.postJson = originalPost;
      ItinerarySelectorApiNormalizer.normalizeRegion = originalNormalize;
   }
});


test('Test_GetAnimalsByExhibit_TestResponse_ExpectNormalizedAnimals', async () => {
   const exhibit = 'Savanna';
   const exhibitsToInclude = [exhibit];
   const day = 15;
   const lion = { species: 'Lion' };
   const unnamed = { species: '' };
   const url = '/get-animals-by-exhibit';
   const originalPost = ApiClient.postJson;
   const originalNormalize = ItinerarySelectorApiNormalizer.normalizeAnimal;
   ApiClient.postJson = async (postedUrl, payload) => {
      assert.equal(postedUrl, url);
      assert.deepEqual(payload.exhibitsToInclude, exhibitsToInclude);
      return {
         animals: [lion, unnamed],
      };
   };
   ItinerarySelectorApiNormalizer.normalizeAnimal = (animal) => animal;

   try {
      const animals = await ItinerarySelectorClient.getAnimalsByExhibit(exhibitsToInclude, { day });

      assert.deepEqual(animals, [lion]);
   } finally {
      ApiClient.postJson = originalPost;
      ItinerarySelectorApiNormalizer.normalizeAnimal = originalNormalize;
   }
});
