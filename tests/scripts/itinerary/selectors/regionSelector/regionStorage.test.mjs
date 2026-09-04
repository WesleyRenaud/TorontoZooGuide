import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionStorage } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStorage.js';
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

   assert.deepEqual(RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY), [
      'Africa Savanna',
      'Eurasia Wilds',
   ]);
});

test('Test_SaveSelectedNames_TestWhitespaceEntries_ExpectNormalizedPersist', () => {
   RegionStorage.saveSelectedNames(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      new Set([' Africa Savanna ', '', 'Eurasia Wilds'])
   );

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna', 'Eurasia Wilds']
   );
});

test('Test_RemovedAnimalKeys_TestAddRestoreClear_ExpectRoundTrip', () => {
   RegionStorage.addRemovedAnimalKey('African Penguin||Africa Savanna');
   RegionStorage.addRemovedAnimalKey('  Masai Giraffe||Africa Savanna  ');

   const removedKeys = RegionStorage.loadRemovedAnimalKeys();
   assert.equal(removedKeys.size, 2);
   assert.equal(removedKeys.has('african penguin||africa savanna'), true);

   RegionStorage.restoreRemovedAnimalKey('African Penguin||Africa Savanna');
   assert.deepEqual(
      [...RegionStorage.loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   RegionStorage.restoreRemovedAnimalKey('unknown||nowhere');
   assert.deepEqual(
      [...RegionStorage.loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   RegionStorage.clearRemovedAnimalKeys();
   assert.equal(RegionStorage.loadRemovedAnimalKeys().size, 0);
});

test('Test_AddRemovedAnimalKey_TestBlankKeys_ExpectIgnored', () => {
   RegionStorage.addRemovedAnimalKey('');
   RegionStorage.addRemovedAnimalKey('   ');

   assert.equal(RegionStorage.loadRemovedAnimalKeys().size, 0);
   assert.equal(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY), null);
});

test('Test_ClearRemovedAnimalKeysForExhibit_TestMixedExhibits_ExpectOnlyTargetDropped', () => {
   RegionStorage.addRemovedAnimalKey('African Penguin||Africa Savanna');
   RegionStorage.addRemovedAnimalKey('Masai Giraffe||Africa Savanna');
   RegionStorage.addRemovedAnimalKey('Amur Tiger||Eurasia Wilds');

   RegionStorage.clearRemovedAnimalKeysForExhibit('Africa Savanna');

   assert.deepEqual(
      [...RegionStorage.loadRemovedAnimalKeys()].sort(),
      ['amur tiger||eurasia wilds']
   );
});

test('Test_ClearRemovedAnimalKeysForExhibit_TestBlankExhibit_ExpectNoOp', () => {
   RegionStorage.addRemovedAnimalKey('African Penguin||Africa Savanna');

   RegionStorage.clearRemovedAnimalKeysForExhibit('');
   RegionStorage.clearRemovedAnimalKeysForExhibit('   ');

   assert.equal(RegionStorage.loadRemovedAnimalKeys().size, 1);
});
