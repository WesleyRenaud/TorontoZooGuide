import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryNormalizerHelper } from '../../../scripts/itinerary/itineraryNormalizerHelper.js';

test('Test_NormalizeItinerarySource_TestMissing_ExpectEmptyCollections', () => {
   assert.deepEqual(ItineraryNormalizerHelper.normalizeItinerarySource(null), {
      date: undefined,
      arrivalTime: undefined,
      departureTime: undefined,
      selectedExhibits: undefined,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
      transportationStations: [],
      events: [],
   });
});

test('Test_NormalizeItinerarySource_TestCollections_ExpectNormalizedItems', () => {
   const source = ItineraryNormalizerHelper.normalizeItinerarySource({
      date: '2026-09-08',
      arrivalTime: '09:00',
      departureTime: '17:00',
      selectedExhibits: ['African Savanna'],
      animals: [{ species: 'African Lion', exhibit: 'African Savanna' }],
      attractions: ['Conservation Carousel'],
      guardiansTalks: [{ name: 'Lion Talk' }],
      wildEncounters: ['Red Panda'],
      transportations: [{ name: 'Zoomobile' }],
      transportationStations: [{ name: 'Main Station' }],
      events: [{ event_type: 'arrival' }],
   });

   assert.equal(source.date, '2026-09-08');
   assert.equal(source.animals.length, 1);
   assert.equal(source.attractions[0], 'Conservation Carousel');
   assert.equal(source.guardiansTalks[0].name, 'Lion Talk');
});
