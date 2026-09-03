import assert from 'node:assert/strict';
import { test } from 'node:test';

import { groupConsecutiveTransportationLegSequences } from '../../scripts/itinerary/selectors/transportationSelector/groupConsecutiveTransportationLegSequences.js';

test('groupConsecutiveTransportationLegSequences splits on time gaps', () => {
   const sequences = groupConsecutiveTransportationLegSequences([
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
   ]);

   assert.equal(sequences.length, 2);
   assert.equal(sequences[0][0].from_station, 'Main Zoomobile Station');
   assert.equal(sequences[0].at(-1).to_station, 'Africa Zoomobile Station');
   assert.equal(sequences[1][0].from_station, 'Canadian Domain Zoomobile Station');
   assert.equal(sequences[1].at(-1).to_station, 'Tundra Zoomobile Station');
});

test('groupConsecutiveTransportationLegSequences splits on station gaps', () => {
   const sequences = groupConsecutiveTransportationLegSequences([
      {
         from_station: 'Main Zoomobile Station',
         to_station: 'Africa Zoomobile Station',
         start_time: '9:00 AM',
         end_time: '9:30 AM',
      },
      {
         from_station: 'Tundra Zoomobile Station',
         to_station: 'Main Zoomobile Station',
         start_time: '9:30 AM',
         end_time: '10:00 AM',
      },
   ]);

   assert.equal(sequences.length, 2);
});
