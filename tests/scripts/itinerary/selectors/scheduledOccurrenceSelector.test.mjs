import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledOccurrenceSorter } from '../../../../scripts/itinerary/scheduledOccurrenceSorter.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_SortScheduledOccurrencesByStartTime_TestSelectorRows_ExpectSortedByStart', () => {
   const kangaroo = { name: 'Kangaroo', start_time: '3:30 PM' };
   const rhinos = { name: 'Guardians of White Rhinos', start_time: '2:00 PM' };
   const capybara = { name: 'Capybara', start_time: '1:30 PM' };
   const armadillos = { name: 'Ballin\' with the Armadillos', start_time: '11:00 AM' };
   const howls = { name: 'From Howls to Honks', start_time: '1:00 PM' };
   const rows = [kangaroo, rhinos, capybara, armadillos, howls];

   const sorted = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(rows);

   assert.equal(sorted.at(Position.FIRST).name, armadillos.name);
   assert.equal(sorted.at(Position.SECOND).name, howls.name);
   assert.equal(sorted.at(Position.THIRD).name, capybara.name);
   assert.equal(sorted.at(Position.FOURTH).name, rhinos.name);
   assert.equal(sorted.at(Position.LAST).name, kangaroo.name);
});


test('Test_SortScheduledOccurrencesByStartTime_TestCustomTimeField_ExpectSortedAndUnparsedLast', () => {
   const missing = { name: 'Missing Time' };
   const morning = { name: 'Morning', time: '10:00' };
   const badTime = { name: 'Bad Time', time: 'soon' };
   const afternoon = { name: 'Afternoon', time: '14:00' };
   const rows = [missing, morning, badTime, afternoon];

   const sorted = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(
      rows,
      (row) => row.time
   );

   assert.equal(sorted.at(Position.FIRST).name, morning.name);
   assert.equal(sorted.at(Position.SECOND).name, afternoon.name);
   assert.equal(sorted.at(Position.THIRD).name, missing.name);
   assert.equal(sorted.at(Position.LAST).name, badTime.name);
});
