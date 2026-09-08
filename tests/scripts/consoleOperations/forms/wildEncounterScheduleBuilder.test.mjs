import assert from 'node:assert/strict';
import { test } from 'node:test';

import { WildEncounterScheduleBuilder } from '../../../../scripts/consoleOperations/forms/wildEncounterScheduleBuilder.js';

test('Test_NormalizeWildEncounterScheduleRow_TestTimeAndDays_ExpectFormattedFlags', () => {
   assert.deepEqual(
      WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow({
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

test('Test_ValidateWildEncounterScheduleRows_TestInvalidAndValidRows_ExpectMessagesOrNull', () => {
   assert.match(
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows([]) ?? '',
      /Encounter times/
   );

   assert.match(
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows([
         { time: '', monday: true },
      ]) ?? '',
      /Encounter time/
   );

   assert.match(
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows([
         { time: '11:00 AM', monday: false, tuesday: false },
      ]) ?? '',
      /at least one day/i
   );

   assert.match(
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows([
         { time: '11:00 AM', monday: true },
         { time: '11:00 AM', tuesday: true },
      ]) ?? '',
      /only be added once/i
   );

   assert.equal(
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows([
         { time: '11:00 AM', monday: true },
         { time: '2:30 PM', saturday: true, sunday: true },
      ]),
      null
   );
});
