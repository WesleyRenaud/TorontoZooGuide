import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { searchItineraryItems, searchZoo } from '../../scripts/api/searchApi.js';

function mockResponse(text = '{}') {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => text,
   };
}

afterEach(() => {
   delete globalThis.fetch;
});

test('searchZoo normalizes search responses', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/search');
      assert.deepEqual(JSON.parse(options.body), {
         query: 'lion',
         includeAnimals: true,
      });

      return mockResponse(JSON.stringify({
         animals: [{ species: 'African Lion' }],
         attractions: [
            {
               name: '  Conservation Carousel  ',
               free_with_admission: true,
               part_of_seasonal_attraction: false,
               is_closed: false,
               info_link: null,
               open_time: ' 10:00 AM ',
               close_time: ' 4:00 PM ',
            },
         ],
      }));
   };

   assert.deepEqual(await searchZoo({
      query: 'lion',
      includeAnimals: true,
   }), {
      animals: [{ species: 'African Lion' }],
      pavilions: [],
      restaurants: [],
      restrooms: [],
      gift_shops: [],
      attractions: [
         {
            name: 'Conservation Carousel',
            free_with_admission: true,
            part_of_seasonal_attraction: false,
            is_closed: false,
            is_also_transportation: false,
            info_link: null,
            open_time: '10:00 AM',
            close_time: '4:00 PM',
         },
      ],
      zoomobile_stations: [],
      guardians_talks: [],
      wild_encounters: [],
   });
});

test('searchItineraryItems leaves unknown endpoints unnormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/search-animals');
      assert.deepEqual(JSON.parse(options.body), { query: 'lion' });

      return mockResponse(JSON.stringify({
         animals: [{ species: 'African Lion' }],
      }));
   };

   assert.deepEqual(await searchItineraryItems('/search-animals', {
      query: 'lion',
   }), {
      animals: [{ species: 'African Lion' }],
   });
});
