import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryTransportationStationRole } from '../../../../scripts/shared/enums/itineraryTransportationStationRole.js';
import itineraryTransportationStationRoleValues from '../../../../shared/enums/itineraryTransportationStationRole.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_OnboardingRoleValues_TestRoles_ExpectOnboardingKinds', () => {
   const roles = ItineraryTransportationStationRole.onboardingRoleValues();

   assert.deepEqual(roles, [
      ItineraryTransportationStationRole.ONBOARDING.kind,
      ItineraryTransportationStationRole.ROUND_TRIP.kind,
   ]);
});


test('Test_OffboardingRoleValues_TestRoles_ExpectOffboardingKinds', () => {
   const roles = ItineraryTransportationStationRole.offboardingRoleValues();

   assert.deepEqual(roles, [
      ItineraryTransportationStationRole.OFFBOARDING.kind,
      ItineraryTransportationStationRole.ROUND_TRIP.kind,
   ]);
});


test('Test_ItineraryTransportationStationRole_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryTransportationStationRole.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itineraryTransportationStationRoleValues).map((key) => [
         key,
         ItineraryTransportationStationRole[key],
      ])
   );

   assert.deepEqual(mapped, itineraryTransportationStationRoleValues);
   assert.deepEqual(itineraryTransportationStationRoleValues, diskValues);
});
