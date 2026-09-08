import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryDraftSaveNormalizer } from '../../../scripts/itinerary/itineraryDraftSaveNormalizer.js';

test('Test_NormalizeTransportationNameForSave_TestInputs_ExpectTrimmedName', () => {
   assert.equal(
      ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave('  Zoomobile  '),
      'Zoomobile'
   );
   assert.equal(
      ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave({ name: '  Zoomobile  ' }),
      'Zoomobile'
   );
   assert.equal(ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(null), '');
});

test('Test_GetAttractionDraftName_TestInputs_ExpectTrimmedName', () => {
   assert.equal(
      ItineraryDraftSaveNormalizer.getAttractionDraftName('  Carousel  '),
      'Carousel'
   );
   assert.equal(
      ItineraryDraftSaveNormalizer.getAttractionDraftName({ name: '  Carousel  ' }),
      'Carousel'
   );
});

test('Test_BuildAttractionNameSet_TestDuplicates_ExpectUniqueNames', () => {
   assert.deepEqual(
      [...ItineraryDraftSaveNormalizer.buildAttractionNameSet([
         'Carousel',
         { name: '  Carousel  ' },
         { name: 'Zoomobile', addedAsAttraction: true },
      ])].sort(),
      ['Carousel', 'Zoomobile']
   );
});

test('Test_IsAttractionAddedAsAttraction_TestFlag_ExpectBoolean', () => {
   assert.equal(
      ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction({ addedAsAttraction: true }),
      true
   );
   assert.equal(
      ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction({ addedAsAttraction: false }),
      false
   );
});

test('Test_NormalizeGuardiansTalkListForSave_TestTalks_ExpectNamedOnly', () => {
   assert.deepEqual(
      ItineraryDraftSaveNormalizer.normalizeGuardiansTalkListForSave([
         { name: '  Lion Talk  ', start_time: '11:00', end_time: '11:30' },
         { name: '', start_time: '12:00' },
      ]),
      [{ name: 'Lion Talk', start_time: '11:00', end_time: '11:30' }]
   );
});

test('Test_NormalizeTransportationsForSave_TestAttractionAndTransport_ExpectDeduped', () => {
   assert.deepEqual(
      ItineraryDraftSaveNormalizer.normalizeTransportationsForSave({
         attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
         transportations: [
            { name: 'Zoomobile', added_as_attraction: false },
            { name: '  ' },
         ],
      }),
      [
         { name: 'Zoomobile', added_as_attraction: false },
         { name: 'Zoomobile', added_as_attraction: true },
      ]
   );
});

test('Test_NormalizeAttractionsForSave_TestSkipsAddedAsAttraction_ExpectNames', () => {
   assert.deepEqual(
      ItineraryDraftSaveNormalizer.normalizeAttractionsForSave([
         'Carousel',
         { name: 'Zoomobile', addedAsAttraction: true },
         { name: 'Splash Island' },
      ]),
      ['Carousel', 'Splash Island']
   );
});
