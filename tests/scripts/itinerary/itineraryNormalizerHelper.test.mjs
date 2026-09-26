import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryNormalizerHelper } from '../../../scripts/itinerary/itineraryNormalizerHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_NormalizeItinerarySource_TestMissing_ExpectEmptyCollections', () => {
   const source = null;

   const normalized = ItineraryNormalizerHelper.normalizeItinerarySource(source);

   assert.deepEqual(normalized, {
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
   const date = '2026-09-08';
   const arrivalTime = '09:00';
   const departureTime = '17:00';
   const exhibit = 'African Savanna';
   const species = 'African Lion';
   const attraction = 'Conservation Carousel';
   const talkName = 'Lion Talk';
   const wildEncounter = 'Red Panda';
   const transportation = 'Zoomobile';
   const station = 'Main Station';
   const eventType = 'arrival';
   const source = {
      date,
      arrivalTime,
      departureTime,
      selectedExhibits: [exhibit],
      animals: [{ species, exhibit }],
      attractions: [attraction],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [wildEncounter],
      transportations: [{ name: transportation }],
      transportationStations: [{ name: station }],
      events: [{ event_type: eventType }],
   };

   const normalized = ItineraryNormalizerHelper.normalizeItinerarySource(source);

   assert.equal(normalized.date, date);
   assert.equal(normalized.animals.length, source.animals.length);
   assert.equal(normalized.attractions[Position.FIRST], attraction);
   assert.equal(normalized.guardiansTalks[Position.FIRST].name, talkName);
});
