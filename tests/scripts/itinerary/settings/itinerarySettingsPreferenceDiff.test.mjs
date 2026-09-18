import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsPreferenceDiff } from '../../../../scripts/itinerary/settings/itinerarySettingsPreferenceDiff.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

test('Test_ChangesFromCheckboxes_TestToggles_ExpectChangedStatuses', () => {
   const changes = ItinerarySettingsPreferenceDiff.changesFromCheckboxes(
      [
         {
            status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            isSuppressed: false,
         },
         {
            status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            isSuppressed: true,
         },
         {
            status: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            isSuppressed: false,
         },
      ],
      [
         {
            checked: false,
            dataset: { status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE },
         },
         {
            checked: true,
            dataset: { status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY },
         },
         {
            checked: true,
            dataset: { status: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP },
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
      ]
   );

   assert.deepEqual(changes, [
      {
         status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         showWarning: false,
      },
      {
         status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         showWarning: true,
      },
   ]);
   assert.equal(changes[Position.FIRST].showWarning, false);
});

test('Test_ChangesFromCheckboxes_TestDefaults_ExpectEmpty', () => {
   assert.deepEqual(ItinerarySettingsPreferenceDiff.changesFromCheckboxes(), []);
});
