import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsWarningCopy } from '../../../../scripts/itinerary/settings/itinerarySettingsWarningCopy.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CopyForStatus_TestKnownWarnings_ExpectConfirmationCopy', () => {
   assert.deepEqual(
      ItinerarySettingsWarningCopy.copyForStatus(
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
      ),
      {
         title: Strings.itinerary.confirmation.shortVisitTitle,
         description: Strings.itinerary.confirmation.shortVisitMessage,
      }
   );
   assert.deepEqual(
      ItinerarySettingsWarningCopy.copyForStatus(
         ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP
      ),
      {
         title: Strings.itinerary.confirmation.earlyAdmissionTitle,
         description: Strings.itinerary.confirmation.earlyAdmissionMessage,
      }
   );
   assert.deepEqual(
      ItinerarySettingsWarningCopy.copyForStatus(ItineraryErrorType.ITEM_NOT_ON_ITINERARY),
      {
         title: Strings.itinerary.confirmation.scheduleItemNotOnItineraryTitle,
         description: Strings.itinerary.confirmation.scheduleItemNotOnItineraryMessage,
      }
   );
});

test('Test_CopyForStatus_TestUnknownStatus_ExpectStatusTitle', () => {
   assert.deepEqual(
      ItinerarySettingsWarningCopy.copyForStatus('notARealWarning'),
      {
         title: 'notARealWarning',
         description: '',
      }
   );
});

test('Test_SuppressableStatuses_TestMixed_ExpectFilteredAndOrdered', () => {
   const statuses = ItinerarySettingsWarningCopy.suppressableStatuses({
      statuses: [
         {
            status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
            isSuppressable: true,
            isSuppressed: true,
         },
         {
            status: ItineraryErrorType.SAVE_FAILED,
            isSuppressable: false,
            isSuppressed: false,
         },
         {
            status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
            isSuppressable: true,
            isSuppressed: false,
         },
         {
            status: ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
            isSuppressable: false,
            isSuppressed: false,
         },
         {
            status: '',
            isSuppressable: true,
            isSuppressed: false,
         },
      ],
   });

   assert.equal(statuses.length, 2);
   assert.equal(
      statuses[Position.FIRST].status,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   );
   assert.equal(
      statuses[Position.SECOND].status,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   );
});

test('Test_SortSuppressableStatuses_TestUnknownStatuses_ExpectOmitted', () => {
   const statuses = ItinerarySettingsWarningCopy.sortSuppressableStatuses([
      {
         status: 'zebraWarning',
         isSuppressable: true,
         isSuppressed: false,
      },
      {
         status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
         isSuppressable: true,
         isSuppressed: false,
      },
   ]);

   assert.equal(statuses.length, 1);
   assert.equal(statuses[Position.FIRST].status, ItineraryErrorType.ITEM_NOT_ON_ITINERARY);
});

test('Test_SuppressableStatuses_TestMissingStatuses_ExpectEmpty', () => {
   assert.deepEqual(ItinerarySettingsWarningCopy.suppressableStatuses(), []);
   assert.deepEqual(ItinerarySettingsWarningCopy.suppressableStatuses({}), []);
});
