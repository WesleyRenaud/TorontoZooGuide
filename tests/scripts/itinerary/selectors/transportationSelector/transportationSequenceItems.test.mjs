import assert from 'node:assert/strict';
import { test } from 'node:test';

import { TransportationSequenceItems } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSequenceItems.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';

const firstStart = '9:00 AM';
const firstEnd = '9:30 AM';
const secondStart = '10:24 AM';
const secondEnd = '11:19 AM';

const DISCONTINUOUS_ZOOMOBILE = {
   name: 'Zoomobile',
   added_as_attraction: false,
   bulk_transit_evaluated: true,
   start_time: firstStart,
   end_time: secondEnd,
   legs: [
      {
         from_station: 'Main Zoomobile Station',
         to_station: 'Canadian Domain Zoomobile Station',
         start_time: firstStart,
         end_time: '9:20 AM',
      },
      {
         from_station: 'Canadian Domain Zoomobile Station',
         to_station: 'Africa Zoomobile Station',
         start_time: '9:20 AM',
         end_time: firstEnd,
      },
      {
         from_station: 'Canadian Domain Zoomobile Station',
         to_station: 'Africa Zoomobile Station',
         start_time: secondStart,
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
         end_time: secondEnd,
      },
   ],
};


test('Test_BuildTransportationSequenceItems_TestDiscontinuous_ExpectSplit', () => {
   const sequences = TransportationSequenceItems.buildTransportationSequenceItems(DISCONTINUOUS_ZOOMOBILE);

   assert.equal(sequences.at(Position.FIRST).start_time, firstStart);
   assert.equal(sequences.at(Position.FIRST).end_time, firstEnd);
   assert.equal(
      sequences.at(Position.FIRST).legs.length,
      2
   );
   assert.equal(sequences.at(Position.LAST).start_time, secondStart);
   assert.equal(sequences.at(Position.LAST).end_time, secondEnd);
   assert.equal(sequences.at(Position.LAST).legs.length, 4);
});


test('Test_ExpandTransportationListItems_TestNoLegs_ExpectUnchanged', () => {
   const transportations = [
      {
         name: 'Zoomobile',
         added_as_attraction: false,
         bulk_transit_evaluated: true,
         legs: [],
      },
   ];

   const expanded = TransportationSequenceItems.expandTransportationListItems(
      transportations,
      { splitSequences: true }
   );

   assert.deepEqual(expanded, transportations);
});


test('Test_ExpandTransportationListItems_TestSplitEnabled_ExpectExpanded', () => {
   const expanded = TransportationSequenceItems.expandTransportationListItems(
      [DISCONTINUOUS_ZOOMOBILE],
      { splitSequences: true }
   );

   assert.equal(expanded.at(Position.FIRST).legs.length, 2);
   assert.equal(expanded.at(Position.LAST).legs.length, 4);
});


test('Test_ExpandTransportationListItems_TestDefault_ExpectUnchanged', () => {
   const items = [DISCONTINUOUS_ZOOMOBILE];

   const expanded = TransportationSequenceItems.expandTransportationListItems(items);

   assert.deepEqual(expanded, items);
});
