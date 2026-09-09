import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryTransportationStationRole } from '../../../../scripts/shared/enums/itineraryTransportationStationRole.js';
import itineraryTransportationStationRoleValues from '../../../../shared/enums/itineraryTransportationStationRole.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryTransportationStationRole_TestConstants_ExpectWireValues', () => {
   assert.equal(ItineraryTransportationStationRole.ONBOARDING, 'onboarding_station');
   assert.equal(ItineraryTransportationStationRole.OFFBOARDING, 'offboarding_station');
   assert.equal(ItineraryTransportationStationRole.ROUND_TRIP, 'round_trip');
});

test('Test_ItineraryTransportationStationRole_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itineraryTransportationStationRoleValues)) {
      assert.equal(ItineraryTransportationStationRole[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryTransportationStationRole.json'), 'utf8')
   );
   assert.deepEqual(itineraryTransportationStationRoleValues, diskValues);
});
