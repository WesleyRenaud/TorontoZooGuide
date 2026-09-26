import assert from 'node:assert/strict';
import { test } from 'node:test';

import { GroupConsecutiveTransportationLegGrouper } from '../../../../../scripts/itinerary/selectors/transportationSelector/groupConsecutiveTransportationLegGrouper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_GroupConsecutiveTransportationLegSequences_TestTimeGaps_ExpectSplit', () => {
   const mainStation = 'Main Zoomobile Station';
   const canadianDomain = 'Canadian Domain Zoomobile Station';
   const africaStation = 'Africa Zoomobile Station';
   const tundraStation = 'Tundra Zoomobile Station';
   const firstLeg = {
      from_station: mainStation,
      to_station: canadianDomain,
      start_time: '9:00 AM',
      end_time: '9:20 AM',
   };
   const secondLeg = {
      from_station: canadianDomain,
      to_station: africaStation,
      start_time: '9:20 AM',
      end_time: '9:30 AM',
   };
   const thirdLeg = {
      from_station: canadianDomain,
      to_station: africaStation,
      start_time: '10:24 AM',
      end_time: '10:34 AM',
   };
   const fourthLeg = {
      from_station: africaStation,
      to_station: tundraStation,
      start_time: '10:34 AM',
      end_time: '10:49 AM',
   };

   const sequences = GroupConsecutiveTransportationLegGrouper.groupConsecutiveTransportationLegSequences([
      firstLeg,
      secondLeg,
      thirdLeg,
      fourthLeg,
   ]);

   assert.equal(sequences.at(Position.FIRST).at(Position.FIRST), firstLeg);
   assert.equal(sequences.at(Position.FIRST).at(Position.LAST), secondLeg);
   assert.equal(sequences.at(Position.LAST).at(Position.FIRST), thirdLeg);
   assert.equal(sequences.at(Position.LAST).at(Position.LAST), fourthLeg);
});


test('Test_GroupConsecutiveTransportationLegSequences_TestStationGaps_ExpectSplit', () => {
   const mainStation = 'Main Zoomobile Station';
   const africaStation = 'Africa Zoomobile Station';
   const tundraStation = 'Tundra Zoomobile Station';
   const firstLeg = {
      from_station: mainStation,
      to_station: africaStation,
      start_time: '9:00 AM',
      end_time: '9:30 AM',
   };
   const secondLeg = {
      from_station: tundraStation,
      to_station: mainStation,
      start_time: '9:30 AM',
      end_time: '10:00 AM',
   };

   const sequences = GroupConsecutiveTransportationLegGrouper.groupConsecutiveTransportationLegSequences([
      firstLeg,
      secondLeg,
   ]);

   assert.equal(sequences.at(Position.FIRST).at(Position.FIRST), firstLeg);
   assert.equal(sequences.at(Position.LAST).at(Position.FIRST), secondLeg);
});
