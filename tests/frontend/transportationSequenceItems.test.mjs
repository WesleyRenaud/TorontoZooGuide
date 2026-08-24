import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildTransportationSequenceItems,
   expandTransportationListItems,
} from '../../scripts/itinerary/selectors/transportationSelector/transportationSequenceItems.js';

const DISCONTINUOUS_ZOOMOBILE = {
   name: 'Zoomobile',
   added_as_attraction: false,
   bulk_transit_evaluated: true,
   start_time: '9:00 AM',
   end_time: '11:19 AM',
   legs: [
      {
         from_station: 'Main Zoomobile Station',
         to_station: 'Canadian Domain Zoomobile Station',
         start_time: '9:00 AM',
         end_time: '9:20 AM',
      },
      {
         from_station: 'Canadian Domain Zoomobile Station',
         to_station: 'Africa Zoomobile Station',
         start_time: '9:20 AM',
         end_time: '9:30 AM',
      },
      {
         from_station: 'Canadian Domain Zoomobile Station',
         to_station: 'Africa Zoomobile Station',
         start_time: '10:24 AM',
         end_time: '10:34 AM',
      },
      {
         from_station: 'Africa Zoomobile Station',
         to_station: 'Tundra Zoomobile Station',
         start_time: '10:34 AM',
         end_time: '10:49 AM',
      },
      {
         from_station: 'Tundra Zoomobile Station',
         to_station: 'Eurasia Zoomobile Station',
         start_time: '10:49 AM',
         end_time: '11:04 AM',
      },
      {
         from_station: 'Eurasia Zoomobile Station',
         to_station: 'Main Zoomobile Station',
         start_time: '11:04 AM',
         end_time: '11:19 AM',
      },
   ],
};

test('buildTransportationSequenceItems splits discontinuous rides', () => {
   const sequences = buildTransportationSequenceItems(DISCONTINUOUS_ZOOMOBILE);

   assert.equal(sequences.length, 2);
   assert.equal(sequences[0].start_time, '9:00 AM');
   assert.equal(sequences[0].end_time, '9:30 AM');
   assert.equal(sequences[0].legs.length, 2);
   assert.equal(sequences[1].start_time, '10:24 AM');
   assert.equal(sequences[1].end_time, '11:19 AM');
   assert.equal(sequences[1].legs.length, 4);
});

test('expandTransportationListItems keeps bulk-evaluated rows without legs', () => {
   const transportations = [
      {
         name: 'Zoomobile',
         added_as_attraction: false,
         bulk_transit_evaluated: true,
         legs: [],
      },
   ];

   assert.deepEqual(
      expandTransportationListItems(transportations, { splitSequences: true }),
      transportations
   );
});

test('expandTransportationListItems expands each ride sequence when enabled', () => {
   const expanded = expandTransportationListItems(
      [DISCONTINUOUS_ZOOMOBILE],
      { splitSequences: true }
   );

   assert.equal(expanded.length, 2);
   assert.equal(expanded[0].legs.length, 2);
   assert.equal(expanded[1].legs.length, 4);
});

test('expandTransportationListItems leaves rows unchanged by default', () => {
   assert.deepEqual(
      expandTransportationListItems([DISCONTINUOUS_ZOOMOBILE]),
      [DISCONTINUOUS_ZOOMOBILE]
   );
});
