import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftSaveNormalizer } from '../../../scripts/itinerary/itineraryDraftSaveNormalizer.js';


test('Test_NormalizeTransportationNameForSave_TestString_ExpectTrimmedName', () => {
   const name = 'Zoomobile';
   const value = `  ${name}  `;

   const normalized = ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(value);

   assert.equal(normalized, name);
});


test('Test_NormalizeTransportationNameForSave_TestObject_ExpectTrimmedName', () => {
   const name = 'Zoomobile';
   const value = { name: `  ${name}  ` };

   const normalized = ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(value);

   assert.equal(normalized, name);
});


test('Test_NormalizeTransportationNameForSave_TestNull_ExpectEmpty', () => {
   const value = null;

   const normalized = ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(value);

   assert.equal(normalized, '');
});


test('Test_GetAttractionDraftName_TestString_ExpectTrimmedName', () => {
   const name = 'Conservation Carousel';
   const value = `  ${name}  `;

   const draftName = ItineraryDraftSaveNormalizer.getAttractionDraftName(value);

   assert.equal(draftName, name);
});


test('Test_GetAttractionDraftName_TestObject_ExpectTrimmedName', () => {
   const name = 'Conservation Carousel';
   const value = { name: `  ${name}  ` };

   const draftName = ItineraryDraftSaveNormalizer.getAttractionDraftName(value);

   assert.equal(draftName, name);
});


test('Test_BuildAttractionNameSet_TestDuplicates_ExpectUniqueNames', () => {
   const carousel = 'Conservation Carousel';
   const zoomobile = 'Zoomobile';
   const values = [
      carousel,
      { name: `  ${carousel}  ` },
      { name: zoomobile, addedAsAttraction: true },
   ];

   const names = [...ItineraryDraftSaveNormalizer.buildAttractionNameSet(values)].sort();

   assert.deepEqual(names, [carousel, zoomobile]);
});


test('Test_IsAttractionAddedAsAttraction_TestTrue_ExpectTrue', () => {
   const addedAsAttraction = true;
   const attraction = { addedAsAttraction };

   const isAdded = ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction(attraction);

   assert.equal(isAdded, addedAsAttraction);
});


test('Test_IsAttractionAddedAsAttraction_TestFalse_ExpectFalse', () => {
   const addedAsAttraction = false;
   const attraction = { addedAsAttraction };

   const isAdded = ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction(attraction);

   assert.equal(isAdded, addedAsAttraction);
});


test('Test_NormalizeGuardiansTalkListForSave_TestTalks_ExpectNamedOnly', () => {
   const name = 'Lion Talk';
   const startTime = '11:00';
   const endTime = '11:30';
   const talks = [
      { name: `  ${name}  `, start_time: startTime, end_time: endTime },
      { name: '', start_time: '12:00' },
   ];

   const normalized = ItineraryDraftSaveNormalizer.normalizeGuardiansTalkListForSave(talks);

   assert.deepEqual(normalized, [{ name, start_time: startTime, end_time: endTime }]);
});


test('Test_NormalizeTransportationsForSave_TestAttractionAndTransport_ExpectDeduped', () => {
   const name = 'Zoomobile';
   const source = {
      attractions: [{ name, addedAsAttraction: true }],
      transportations: [
         { name, added_as_attraction: false },
         { name: '  ' },
      ],
   };

   const normalized = ItineraryDraftSaveNormalizer.normalizeTransportationsForSave(source);

   assert.deepEqual(normalized, [
      { name, added_as_attraction: false },
      { name, added_as_attraction: true },
   ]);
});


test('Test_NormalizeAttractionsForSave_TestSkipsAddedAsAttraction_ExpectNames', () => {
   const carousel = 'Conservation Carousel';
   const splashIsland = 'Splash Island';
   const attractions = [
      carousel,
      { name: 'Zoomobile', addedAsAttraction: true },
      { name: splashIsland },
   ];

   const normalized = ItineraryDraftSaveNormalizer.normalizeAttractionsForSave(attractions);

   assert.deepEqual(normalized, [carousel, splashIsland]);
});
