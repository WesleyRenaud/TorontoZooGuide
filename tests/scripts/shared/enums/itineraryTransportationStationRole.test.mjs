import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryTransportationStationRole } from '../../../../scripts/shared/enums/itineraryTransportationStationRole.js';
import itineraryTransportationStationRoleValues from '../../../../shared/enums/itineraryTransportationStationRole.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryTransportationStationRole_TestRoleValueHelpers_ExpectKinds', () => {
   assert.deepEqual(
      ItineraryTransportationStationRole.onboardingRoleValues(),
      [
         ItineraryTransportationStationRole.ONBOARDING.kind,
         ItineraryTransportationStationRole.ROUND_TRIP.kind,
      ]
   );
   assert.deepEqual(
      ItineraryTransportationStationRole.offboardingRoleValues(),
      [
         ItineraryTransportationStationRole.OFFBOARDING.kind,
         ItineraryTransportationStationRole.ROUND_TRIP.kind,
      ]
   );
});

test('Test_ItineraryTransportationStationRole_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itineraryTransportationStationRoleValues)) {
      assert.deepEqual(ItineraryTransportationStationRole[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryTransportationStationRole.json'), 'utf8')
   );
   assert.deepEqual(itineraryTransportationStationRoleValues, diskValues);
});
