import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsPreferenceDiff } from '../../../../scripts/itinerary/settings/itinerarySettingsPreferenceDiff.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_ChangesFromCheckboxes_TestToggles_ExpectChangedStatuses', () => {
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const itemStatus = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;
   const membershipStatus = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;
   const statuses = [
      {
         status: arrivalStatus,
         isSuppressed: false,
      },
      {
         status: itemStatus,
         isSuppressed: true,
      },
      {
         status: membershipStatus,
         isSuppressed: false,
      },
   ];
   const checkboxes = [
      {
         checked: false,
         dataset: { status: arrivalStatus },
      },
      {
         checked: true,
         dataset: { status: itemStatus },
      },
      {
         checked: true,
         dataset: { status: membershipStatus },
      },
      {
         checked: false,
         dataset: { status: 'unknownStatus' },
      },
      {
         checked: false,
         dataset: {},
      },
      null,
   ];

   const changes = ItinerarySettingsPreferenceDiff.changesFromCheckboxes(
      statuses,
      checkboxes
   );

   assert.deepEqual(changes, [
      {
         status: arrivalStatus,
         showWarning: false,
      },
      {
         status: itemStatus,
         showWarning: true,
      },
   ]);
   assert.equal(changes[Position.FIRST].showWarning, false);
});


test('Test_ChangesFromCheckboxes_TestDefaults_ExpectEmpty', () => {
   const changes = ItinerarySettingsPreferenceDiff.changesFromCheckboxes();

   assert.deepEqual(changes, []);
});
