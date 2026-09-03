import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { SearchApi } from '../../../scripts/api/searchApi.js';

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

test('Test_SearchZoo_TestAttractionPayload_ExpectNormalizedResponse', async () => {
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

   assert.deepEqual(await SearchApi.searchZoo({
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
            route_duration_minutes: null,
            info_link: null,
            open_time: '10:00 AM',
            close_time: '4:00 PM',
         },
      ],
      transportations: [],
      transportation_stations: [],
      guardians_talks: [],
      wild_encounters: [],
   });
});

test('Test_SearchItineraryItems_TestUnknownEndpoint_ExpectUnnormalized', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/search-animals');
      assert.deepEqual(JSON.parse(options.body), { query: 'lion' });

      return mockResponse(JSON.stringify({
         animals: [{ species: 'African Lion' }],
      }));
   };

   assert.deepEqual(await SearchApi.searchItineraryItems('/search-animals', {
      query: 'lion',
   }), {
      animals: [{ species: 'African Lion' }],
   });
});

test('Test_NormalizeSearchResponse_TestCollections_ExpectNormalizedRows', () => {
   const response = SearchApi.normalizeSearchResponse({
      animals: [{ species: 'African Lion' }],
      gift_shops: [{ name: 'Zootique' }],
      attractions: [
         {
            name: '  Conservation Carousel  ',
            free_with_admission: true,
            part_of_seasonal_attraction: 1,
            is_closed: false,
            is_also_transportation: true,
            info_link: '  https://www.torontozoo.com/tickets/carousel  ',
         },
      ],
      guardians_talks: [
         {
            name: '  Amur Tiger  ',
            location: '  Eurasia Wilds  ',
            start_time: '  13:30  ',
            maximum_duration: 30,
            linked_animals: [
               {
                  species: '  Amur Tiger  ',
                  exhibit: '  Eurasia Wilds  ',
               },
            ],
         },
      ],
      wild_encounters: [
         {
            name: '  African Rainforest  ',
            meeting_spot: '  Wild Encounter - Africa Meeting Spot  ',
            start_time: '  14:00  ',
            maximum_duration: 45,
            link: '',
         },
      ],
   });

   assert.deepEqual(response.animals, [{ species: 'African Lion' }]);
   assert.deepEqual(response.gift_shops, [{ name: 'Zootique' }]);
   assert.equal(response.attractions[0].name, 'Conservation Carousel');
   assert.equal(response.attractions[0].free_with_admission, true);
   assert.equal(response.attractions[0].part_of_seasonal_attraction, false);
   assert.equal(response.attractions[0].is_closed, false);
   assert.equal(response.attractions[0].is_also_transportation, true);
   assert.equal(response.attractions[0].info_link, 'https://www.torontozoo.com/tickets/carousel');
   assert.deepEqual(response.guardians_talks[0], {
      name: 'Amur Tiger',
      location: 'Eurasia Wilds',
      start_time: '13:30',
      maximum_duration: 30,
      linked_animals: [
         {
            species: 'Amur Tiger',
            exhibit: 'Eurasia Wilds',
         },
      ],
   });
   assert.deepEqual(response.wild_encounters[0], {
      name: 'African Rainforest',
      meeting_spot: 'Wild Encounter - Africa Meeting Spot',
      start_time: '14:00',
      maximum_duration: 45,
      link: null,
   });
});

test('Test_NormalizeSearchResponse_TestMissingGroups_ExpectEmptyArrays', () => {
   assert.deepEqual(SearchApi.normalizeSearchResponse(null), {
      animals: [],
      pavilions: [],
      restaurants: [],
      restrooms: [],
      gift_shops: [],
      attractions: [],
      transportations: [],
      transportation_stations: [],
      guardians_talks: [],
      wild_encounters: [],
   });
});
