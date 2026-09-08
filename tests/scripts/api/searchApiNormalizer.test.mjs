import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchApiNormalizer } from '../../../scripts/api/searchApiNormalizer.js';

test('Test_NormalizeAttractionRow_TestFlagsAndTimes_ExpectNormalized', () => {
   assert.deepEqual(
      SearchApiNormalizer.normalizeAttractionRow({
         name: '  Conservation Carousel  ',
         free_with_admission: true,
         part_of_seasonal_attraction: 1,
         is_closed: false,
         is_also_transportation: true,
         route_duration_minutes: '12',
         info_link: '  https://example.com  ',
         open_time: '  10:00  ',
         close_time: '  ',
         region: 'Canada',
      }),
      {
         name: 'Conservation Carousel',
         free_with_admission: true,
         part_of_seasonal_attraction: false,
         is_closed: false,
         is_also_transportation: true,
         route_duration_minutes: 12,
         info_link: 'https://example.com',
         open_time: '10:00',
         close_time: null,
         region: 'Canada',
      }
   );
});

test('Test_NormalizeGuardiansTalkRow_TestLinkedAnimals_ExpectNormalized', () => {
   assert.deepEqual(
      SearchApiNormalizer.normalizeGuardiansTalkRow({
         name: '  Lion Talk  ',
         location: '  Theatre  ',
         start_time: '  11:00  ',
         linked_animals: [{ species: '  African Lion  ', exhibit: '  African Savanna  ' }],
      }),
      {
         name: 'Lion Talk',
         location: 'Theatre',
         start_time: '11:00',
         linked_animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
      }
   );
});

test('Test_NormalizeWildEncounterRow_TestFields_ExpectNormalized', () => {
   assert.deepEqual(
      SearchApiNormalizer.normalizeWildEncounterRow({
         name: '  Red Panda  ',
         meeting_spot: '  Pavilion  ',
         start_time: '  13:00  ',
         link: '  ',
      }),
      {
         name: 'Red Panda',
         meeting_spot: 'Pavilion',
         start_time: '13:00',
         link: null,
      }
   );
});

test('Test_NormalizeTransportationRow_TestFlags_ExpectNormalized', () => {
   assert.deepEqual(
      SearchApiNormalizer.normalizeTransportationRow({
         name: '  Zoomobile  ',
         free_with_admission: true,
         is_also_attraction: false,
         info_link: null,
         open_time: '09:00',
         close_time: '17:00',
      }),
      {
         name: 'Zoomobile',
         free_with_admission: true,
         is_also_attraction: false,
         info_link: null,
         open_time: '09:00',
         close_time: '17:00',
      }
   );
});

test('Test_NormalizeSearchEndpointResponse_TestOtherEndpoint_ExpectPassthrough', () => {
   const response = { ok: true };

   assert.equal(
      SearchApiNormalizer.normalizeSearchEndpointResponse('/other', response),
      response
   );
});
