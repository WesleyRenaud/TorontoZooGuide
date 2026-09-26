import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchApiNormalizer } from '../../../scripts/api/searchApiNormalizer.js';
import { ValueNormalizer } from '../../../scripts/api/valueNormalizer.js';


test('Test_NormalizeAttractionRow_TestFlagsAndTimes_ExpectNormalized', () => {
   const name = 'Conservation Carousel';
   const freeWithAdmission = true;
   const isClosed = false;
   const isAlsoTransportation = true;
   const routeDurationMinutes = '12';
   const infoLink = 'https://example.com';
   const openTime = '10:00';
   const region = 'Canada';
   const row = {
      name: `  ${name}  `,
      free_with_admission: freeWithAdmission,
      part_of_seasonal_attraction: 1,
      is_closed: isClosed,
      is_also_transportation: isAlsoTransportation,
      route_duration_minutes: routeDurationMinutes,
      info_link: `  ${infoLink}  `,
      open_time: `  ${openTime}  `,
      close_time: '  ',
      region,
   };

   const attraction = SearchApiNormalizer.normalizeAttractionRow(row);

   assert.deepEqual(attraction, {
      name,
      free_with_admission: freeWithAdmission,
      part_of_seasonal_attraction: ValueNormalizer.asBoolean(row.part_of_seasonal_attraction),
      is_closed: isClosed,
      is_also_transportation: isAlsoTransportation,
      route_duration_minutes: Number(routeDurationMinutes),
      info_link: infoLink,
      open_time: openTime,
      close_time: null,
      region,
   });
});


test('Test_NormalizeGuardiansTalkRow_TestLinkedAnimals_ExpectNormalized', () => {
   const name = 'Lion Talk';
   const location = 'Theatre';
   const startTime = '11:00';
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = {
      name: `  ${name}  `,
      location: `  ${location}  `,
      start_time: `  ${startTime}  `,
      linked_animals: [{ species: `  ${species}  `, exhibit: `  ${exhibit}  ` }],
   };

   const talk = SearchApiNormalizer.normalizeGuardiansTalkRow(row);

   assert.deepEqual(talk, {
      name,
      location,
      start_time: startTime,
      linked_animals: [{ species, exhibit }],
   });
});


test('Test_NormalizeWildEncounterRow_TestFields_ExpectNormalized', () => {
   const name = 'Red Panda';
   const meetingSpot = 'Pavilion';
   const startTime = '13:00';
   const row = {
      name: `  ${name}  `,
      meeting_spot: `  ${meetingSpot}  `,
      start_time: `  ${startTime}  `,
      link: '  ',
   };

   const encounter = SearchApiNormalizer.normalizeWildEncounterRow(row);

   assert.deepEqual(encounter, {
      name,
      meeting_spot: meetingSpot,
      start_time: startTime,
      link: null,
   });
});


test('Test_NormalizeTransportationRow_TestFlags_ExpectNormalized', () => {
   const name = 'Zoomobile';
   const freeWithAdmission = true;
   const isAlsoAttraction = false;
   const infoLink = null;
   const openTime = '09:00';
   const closeTime = '17:00';
   const row = {
      name: `  ${name}  `,
      free_with_admission: freeWithAdmission,
      is_also_attraction: isAlsoAttraction,
      info_link: infoLink,
      open_time: openTime,
      close_time: closeTime,
   };

   const transportation = SearchApiNormalizer.normalizeTransportationRow(row);

   assert.deepEqual(transportation, {
      name,
      free_with_admission: freeWithAdmission,
      is_also_attraction: isAlsoAttraction,
      info_link: infoLink,
      open_time: openTime,
      close_time: closeTime,
   });
});


test('Test_NormalizeSearchEndpointResponse_TestOtherEndpoint_ExpectPassthrough', () => {
   const endpoint = '/other';
   const response = { ok: true };

   const normalized = SearchApiNormalizer.normalizeSearchEndpointResponse(endpoint, response);

   assert.equal(normalized, response);
});
