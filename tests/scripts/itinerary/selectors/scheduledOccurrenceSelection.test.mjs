import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { SelectionStore } from '../../../../scripts/itinerary/selectors/base/selectionStore.js';
import { CreateScheduledOccurrenceSelector } from '../../../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import { GuardiansTalkScheduleItemKey } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { GuardiansTalkSelectorModel } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function _createGuardiansTalkSelectionState() {
   return SelectionStore.createSelectorSelectionState({
      storageKey: STORAGE_KEY,
      getId: GuardiansTalkSelectorModel.getGuardiansTalkId,
      migrateSelected: CreateScheduledOccurrenceSelector.createScheduledOccurrenceMigration({
         emptyStoredFields: {
            location: '',
            start_time: '',
            end_time: '',
         },
         buildImageSrc: () => '',
         readStoredFields: GuardiansTalkSelectorModel.readGuardiansTalkStoredFields,
         getId: GuardiansTalkSelectorModel.getGuardiansTalkId,
      }),
      makeSelection: (row) => ({
         id: GuardiansTalkSelectorModel.getGuardiansTalkId(row),
         name: row.name,
         location: row.location ?? '',
         start_time: row.start_time ?? '',
         end_time: row.end_time ?? '',
      }),
   });
}

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('Test_API_TestAPITalkWithoutIdMatchesCatalogWireId_ExpectOk', () => {
   localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify([
         {
            name: 'New World Primates',
            location: 'Americas Pavilion',
            start_time: '11:30 AM',
            end_time: '12:00 PM',
         },
      ])
   );

   const state = _createGuardiansTalkSelectionState();
   const catalogRow = {
      name: 'New World Primates',
      location: 'Americas Pavilion',
      start_time: '11:30 AM',
      end_time: '12:00 PM',
   };
   const catalogId = GuardiansTalkSelectorModel.getGuardiansTalkId(catalogRow);

   assert.equal(catalogId, GuardiansTalkScheduleItemKey.fromRow(catalogRow).toWire());
   assert.equal(state.isSelected(catalogId), true);
   assert.equal(state.getSelectedSnapshot()[Position.FIRST].id, catalogId);
});

test('Test_Name_TestNameOnlyStoredIdIsUpgradedWhenStart_ExpectOk', () => {
   localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify([
         {
            id: 'New World Primates',
            name: 'New World Primates',
            location: 'Americas Pavilion',
            start_time: '11:30 AM',
            end_time: '12:00 PM',
         },
      ])
   );

   const state = _createGuardiansTalkSelectionState();
   const upgradedWire = new GuardiansTalkScheduleItemKey(
      'New World Primates',
      '11:30 AM',
      '12:00 PM'
   ).toWire();

   assert.equal(
      state.isSelected(upgradedWire),
      true
   );
   assert.equal(state.isSelected('New World Primates'), false);
});
