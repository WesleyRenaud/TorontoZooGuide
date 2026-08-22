import assert from 'node:assert/strict';
import test from 'node:test';

import { normalizeSearchResponse } from '../../scripts/api/searchApi.js';

test('normalizes search response collections before rows are rendered', () => {
   const response = normalizeSearchResponse({
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

test('normalizes missing search response groups to empty arrays', () => {
   assert.deepEqual(normalizeSearchResponse(null), {
      animals: [],
      pavilions: [],
      restaurants: [],
      restrooms: [],
      gift_shops: [],
      attractions: [],
      transportations: [],
      zoomobile_stations: [],
      guardians_talks: [],
      wild_encounters: [],
   });
});
