import assert from 'node:assert/strict';
import { describe, test } from 'node:test';

import {
   normalizeWildEncounterScheduleRow,
   validateWildEncounterScheduleRows,
} from '../../scripts/consoleOperations/forms/wildEncounterScheduleRows.js';

describe('wildEncounterScheduleRows', () => {
   test('normalizeWildEncounterScheduleRow formats time and day flags', () => {
      assert.deepEqual(
         normalizeWildEncounterScheduleRow({
            time: '2:30 PM',
            monday: true,
            tuesday: false,
            wednesday: true,
         }),
         {
            time: '2:30 PM',
            monday: true,
            tuesday: false,
            wednesday: true,
            thursday: false,
            friday: false,
            saturday: false,
            sunday: false,
         }
      );
   });

   test('validateWildEncounterScheduleRows requires rows, times, days, and unique times', () => {
      assert.match(
         validateWildEncounterScheduleRows([]) ?? '',
         /Encounter times/
      );

      assert.match(
         validateWildEncounterScheduleRows([
            { time: '', monday: true },
         ]) ?? '',
         /Encounter time/
      );

      assert.match(
         validateWildEncounterScheduleRows([
            { time: '11:00 AM', monday: false, tuesday: false },
         ]) ?? '',
         /at least one day/i
      );

      assert.match(
         validateWildEncounterScheduleRows([
            { time: '11:00 AM', monday: true },
            { time: '11:00 AM', tuesday: true },
         ]) ?? '',
         /only be added once/i
      );

      assert.equal(
         validateWildEncounterScheduleRows([
            { time: '11:00 AM', monday: true },
            { time: '2:30 PM', saturday: true, sunday: true },
         ]),
         null
      );
   });
});
