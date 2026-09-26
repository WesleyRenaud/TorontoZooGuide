import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsWarningCopy } from '../../../../scripts/itinerary/settings/itinerarySettingsWarningCopy.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CopyForStatus_TestShortVisit_ExpectConfirmationCopy', () => {
   const status = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;

   const copy = ItinerarySettingsWarningCopy.copyForStatus(status);

   assert.deepEqual(copy, {
      title: Strings.itinerary.confirmation.shortVisitTitle,
      description: Strings.itinerary.confirmation.shortVisitMessage,
   });
});


test('Test_CopyForStatus_TestEarlyAdmission_ExpectConfirmationCopy', () => {
   const status = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP;

   const copy = ItinerarySettingsWarningCopy.copyForStatus(status);

   assert.deepEqual(copy, {
      title: Strings.itinerary.confirmation.earlyAdmissionTitle,
      description: Strings.itinerary.confirmation.earlyAdmissionMessage,
   });
});


test('Test_CopyForStatus_TestItemNotOnItinerary_ExpectConfirmationCopy', () => {
   const status = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;

   const copy = ItinerarySettingsWarningCopy.copyForStatus(status);

   assert.deepEqual(copy, {
      title: Strings.itinerary.confirmation.scheduleItemNotOnItineraryTitle,
      description: Strings.itinerary.confirmation.scheduleItemNotOnItineraryMessage,
   });
});


test('Test_CopyForStatus_TestUnknownStatus_ExpectStatusTitle', () => {
   const status = 'notARealWarning';

   const copy = ItinerarySettingsWarningCopy.copyForStatus(status);

   assert.deepEqual(copy, {
      title: status,
      description: '',
   });
});


test('Test_SuppressableStatuses_TestMixed_ExpectFilteredAndOrdered', () => {
   const itemStatus = {
      status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      isSuppressable: true,
      isSuppressed: true,
   };
   const arrivalStatus = {
      status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      isSuppressable: true,
      isSuppressed: false,
   };
   const statuses = [
      itemStatus,
      {
         status: ItineraryErrorType.SAVE_FAILED,
         isSuppressable: false,
         isSuppressed: false,
      },
      arrivalStatus,
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
   ];

   const suppressable = ItinerarySettingsWarningCopy.suppressableStatuses({ statuses });

   assert.equal(suppressable.length, 2);
   assert.equal(suppressable[Position.FIRST].status, arrivalStatus.status);
   assert.equal(suppressable[Position.SECOND].status, itemStatus.status);
});


test('Test_SortSuppressableStatuses_TestUnknownStatuses_ExpectOmitted', () => {
   const knownStatus = {
      status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      isSuppressable: true,
      isSuppressed: false,
   };
   const statuses = [
      {
         status: 'zebraWarning',
         isSuppressable: true,
         isSuppressed: false,
      },
      knownStatus,
   ];

   const sorted = ItinerarySettingsWarningCopy.sortSuppressableStatuses(statuses);

   assert.equal(sorted.length, 1);
   assert.equal(sorted[Position.FIRST].status, knownStatus.status);
});


test('Test_SuppressableStatuses_TestMissingStatuses_ExpectEmpty', () => {
   const statuses = ItinerarySettingsWarningCopy.suppressableStatuses();

   assert.deepEqual(statuses, []);
});


test('Test_SuppressableStatuses_TestEmptyObject_ExpectEmpty', () => {
   const statuses = ItinerarySettingsWarningCopy.suppressableStatuses({});

   assert.deepEqual(statuses, []);
});
