import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { SelectionStore } from '../../../../scripts/itinerary/selectors/base/selectionStore.js';
import { CreateScheduledOccurrenceSelector } from '../../../../scripts/itinerary/selectors/createScheduledOccurrenceSelector.js';
import { GuardiansTalkScheduleItemKey } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { GuardiansTalkSelectorModel } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { StorageKeys } from '../../../../scripts/itinerary/storageKeys.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';

const STORAGE_KEY = StorageKeys.GUARDIANS_KEY;

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


test('Test_IsSelected_TestTalkWithoutId_ExpectCatalogWireId', () => {
   const name = 'New World Primates';
   const location = 'Americas Pavilion';
   const startTime = '11:30 AM';
   const endTime = '12:00 PM';
   const storedTalk = {
      name,
      location,
      start_time: startTime,
      end_time: endTime,
   };
   localStorage.setItem(STORAGE_KEY, JSON.stringify([storedTalk]));
   const catalogRow = {
      name,
      location,
      start_time: startTime,
      end_time: endTime,
   };
   const state = _createGuardiansTalkSelectionState();
   const catalogId = GuardiansTalkSelectorModel.getGuardiansTalkId(catalogRow);

   const isSelected = state.isSelected(catalogId);

   assert.equal(catalogId, GuardiansTalkScheduleItemKey.fromRow(catalogRow).toWire());
   assert.equal(isSelected, true);
   assert.equal(state.getSelectedSnapshot().at(Position.FIRST).id, catalogId);
});


test('Test_IsSelected_TestNameOnlyStoredId_ExpectUpgradedWire', () => {
   const name = 'New World Primates';
   const location = 'Americas Pavilion';
   const startTime = '11:30 AM';
   const endTime = '12:00 PM';
   localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify([
         {
            id: name,
            name,
            location,
            start_time: startTime,
            end_time: endTime,
         },
      ])
   );
   const state = _createGuardiansTalkSelectionState();
   const upgradedWire = new GuardiansTalkScheduleItemKey(name, startTime, endTime).toWire();

   const isSelected = state.isSelected(upgradedWire);

   assert.equal(isSelected, true);
   assert.equal(state.isSelected(name), false);
});
