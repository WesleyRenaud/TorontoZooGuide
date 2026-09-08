import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionStorageStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { StorageKeys } from '../../../../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('Test_LoadSelectedNames_TestWhitespaceAndNonStrings_ExpectTrimmedNames', () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([' Africa Savanna ', '', 42, 'Eurasia Wilds'])
   );

   assert.deepEqual(RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY), [
      'Africa Savanna',
      '42',
      'Eurasia Wilds',
   ]);
});

test('Test_SaveSelectedNames_TestWhitespaceEntries_ExpectNormalizedPersist', () => {
   RegionStorageStore.saveSelectedNames(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      new Set([' Africa Savanna ', '', 'Eurasia Wilds'])
   );

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna', 'Eurasia Wilds']
   );
});

test('Test_RemovedAnimalKeys_TestAddRestoreClear_ExpectRoundTrip', () => {
   RegionStorageStore.addRemovedAnimalKey('African Penguin||Africa Savanna');
   RegionStorageStore.addRemovedAnimalKey('  Masai Giraffe||Africa Savanna  ');

   const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();
   assert.equal(removedKeys.size, 2);
   assert.equal(removedKeys.has('african penguin||africa savanna'), true);

   RegionStorageStore.restoreRemovedAnimalKey('African Penguin||Africa Savanna');
   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   RegionStorageStore.restoreRemovedAnimalKey('unknown||nowhere');
   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   RegionStorageStore.clearRemovedAnimalKeys();
   assert.equal(RegionStorageStore.loadRemovedAnimalKeys().size, 0);
});

test('Test_AddRemovedAnimalKey_TestBlankKeys_ExpectIgnored', () => {
   RegionStorageStore.addRemovedAnimalKey('');
   RegionStorageStore.addRemovedAnimalKey('   ');

   assert.equal(RegionStorageStore.loadRemovedAnimalKeys().size, 0);
   assert.equal(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY), null);
});

test('Test_ClearRemovedAnimalKeysForExhibit_TestMixedExhibits_ExpectOnlyTargetDropped', () => {
   RegionStorageStore.addRemovedAnimalKey('African Penguin||Africa Savanna');
   RegionStorageStore.addRemovedAnimalKey('Masai Giraffe||Africa Savanna');
   RegionStorageStore.addRemovedAnimalKey('Amur Tiger||Eurasia Wilds');

   RegionStorageStore.clearRemovedAnimalKeysForExhibit('Africa Savanna');

   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()].sort(),
      ['amur tiger||eurasia wilds']
   );
});

test('Test_ClearRemovedAnimalKeysForExhibit_TestBlankExhibit_ExpectNoOp', () => {
   RegionStorageStore.addRemovedAnimalKey('African Penguin||Africa Savanna');

   RegionStorageStore.clearRemovedAnimalKeysForExhibit('');
   RegionStorageStore.clearRemovedAnimalKeysForExhibit('   ');

   assert.equal(RegionStorageStore.loadRemovedAnimalKeys().size, 1);
});
