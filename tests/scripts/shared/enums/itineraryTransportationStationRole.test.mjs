import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryTransportationStationRole } from '../../../../scripts/shared/enums/itineraryTransportationStationRole.js';
import itineraryTransportationStationRoleValues from '../../../../shared/enums/itineraryTransportationStationRole.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryTransportationStationRole_TestConstants_ExpectObjectMembers', () => {
   assert.deepEqual(ItineraryTransportationStationRole.ONBOARDING, {
      kind: 'onboarding_station',
      onboarding: true,
      offboarding: false,
   });
   assert.deepEqual(ItineraryTransportationStationRole.OFFBOARDING, {
      kind: 'offboarding_station',
      onboarding: false,
      offboarding: true,
   });
   assert.deepEqual(ItineraryTransportationStationRole.ROUND_TRIP, {
      kind: 'round_trip',
      onboarding: true,
      offboarding: true,
   });
});

test('Test_ItineraryTransportationStationRole_TestRoleValueHelpers_ExpectKinds', () => {
   assert.deepEqual(
      ItineraryTransportationStationRole.onboardingRoleValues(),
      ['onboarding_station', 'round_trip']
   );
   assert.deepEqual(
      ItineraryTransportationStationRole.offboardingRoleValues(),
      ['offboarding_station', 'round_trip']
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
