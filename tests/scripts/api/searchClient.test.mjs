import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { SearchApiNormalizer } from '../../../scripts/api/searchApiNormalizer.js';
import { SearchClient } from '../../../scripts/api/searchClient.js';
import { Position } from '../../../scripts/shared/enums/position.js';

function _mockResponse(text = '{}') {
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
   const query = 'lion';
   const includeAnimals = true;
   const species = 'African Lion';
   const attractionName = 'Conservation Carousel';
   const freeWithAdmission = true;
   const partOfSeasonalAttraction = false;
   const isClosed = false;
   const infoLink = null;
   const openTime = '10:00 AM';
   const closeTime = '4:00 PM';
   const url = '/search';
   const payload = {
      query,
      includeAnimals,
   };
   const attractionRow = {
      name: `  ${attractionName}  `,
      free_with_admission: freeWithAdmission,
      part_of_seasonal_attraction: partOfSeasonalAttraction,
      is_closed: isClosed,
      info_link: infoLink,
      open_time: ` ${openTime} `,
      close_time: ` ${closeTime} `,
   };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, url);
      assert.deepEqual(JSON.parse(options.body), payload);

      return _mockResponse(JSON.stringify({
         animals: [{ species }],
         attractions: [attractionRow],
      }));
   };

   const response = await SearchClient.searchZoo(payload);

   assert.deepEqual(response, {
      animals: [{ species }],
      pavilions: [],
      restaurants: [],
      restrooms: [],
      gift_shops: [],
      attractions: [SearchApiNormalizer.normalizeAttractionRow(attractionRow)],
      transportations: [],
      transportation_stations: [],
      guardians_talks: [],
      wild_encounters: [],
   });
});


test('Test_SearchItineraryItems_TestUnknownEndpoint_ExpectUnnormalized', async () => {
   const endpoint = '/search-animals';
   const query = 'lion';
   const species = 'African Lion';
   const payload = { query };
   globalThis.fetch = async (requestedUrl, options) => {
      assert.equal(requestedUrl, endpoint);
      assert.deepEqual(JSON.parse(options.body), payload);

      return _mockResponse(JSON.stringify({
         animals: [{ species }],
      }));
   };

   const response = await SearchClient.searchItineraryItems(endpoint, payload);

   assert.deepEqual(response, {
      animals: [{ species }],
   });
});


test('Test_NormalizeSearchResponse_TestCollections_ExpectNormalizedRows', () => {
   const species = 'African Lion';
   const giftShopName = 'Zootique';
   const attractionName = 'Conservation Carousel';
   const freeWithAdmission = true;
   const isClosed = false;
   const isAlsoTransportation = true;
   const infoLink = 'https://www.torontozoo.com/tickets/carousel';
   const talkName = 'Amur Tiger';
   const talkLocation = 'Eurasia Wilds';
   const talkStartTime = '13:30';
   const talkDuration = 30;
   const encounterName = 'African Rainforest';
   const meetingSpot = 'Wild Encounter - Africa Meeting Spot';
   const encounterStartTime = '14:00';
   const encounterDuration = 45;
   const animal = { species };
   const giftShop = { name: giftShopName };
   const attractionRow = {
      name: `  ${attractionName}  `,
      free_with_admission: freeWithAdmission,
      part_of_seasonal_attraction: 1,
      is_closed: isClosed,
      is_also_transportation: isAlsoTransportation,
      info_link: `  ${infoLink}  `,
   };
   const talkRow = {
      name: `  ${talkName}  `,
      location: `  ${talkLocation}  `,
      start_time: `  ${talkStartTime}  `,
      maximum_duration: talkDuration,
      linked_animals: [
         {
            species: `  ${talkName}  `,
            exhibit: `  ${talkLocation}  `,
         },
      ],
   };
   const encounterRow = {
      name: `  ${encounterName}  `,
      meeting_spot: `  ${meetingSpot}  `,
      start_time: `  ${encounterStartTime}  `,
      maximum_duration: encounterDuration,
      link: '',
   };

   const response = SearchClient.normalizeSearchResponse({
      animals: [animal],
      gift_shops: [giftShop],
      attractions: [attractionRow],
      guardians_talks: [talkRow],
      wild_encounters: [encounterRow],
   });

   assert.deepEqual(response.animals, [animal]);
   assert.deepEqual(response.gift_shops, [giftShop]);
   assert.deepEqual(
      response.attractions[Position.FIRST],
      SearchApiNormalizer.normalizeAttractionRow(attractionRow)
   );
   assert.deepEqual(
      response.guardians_talks[Position.FIRST],
      SearchApiNormalizer.normalizeGuardiansTalkRow(talkRow)
   );
   assert.deepEqual(
      response.wild_encounters[Position.FIRST],
      SearchApiNormalizer.normalizeWildEncounterRow(encounterRow)
   );
});


test('Test_NormalizeSearchResponse_TestMissingGroups_ExpectEmptyArrays', () => {
   const response = SearchClient.normalizeSearchResponse(null);

   assert.deepEqual(response, {
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
