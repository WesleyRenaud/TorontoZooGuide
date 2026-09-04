import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   addRemovedAnimalKey,
   clearRemovedAnimalKeys,
   clearRemovedAnimalKeysForExhibit,
   loadRemovedAnimalKeys,
   loadSelectedNames,
   restoreRemovedAnimalKey,
   saveSelectedNames,
} from '../../scripts/itinerary/selectors/regionSelector/regionStorage.js';
import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from './helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});

test('loadSelectedNames trims and drops empty entries', () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([' Africa Savanna ', '', 42, 'Eurasia Wilds'])
   );

   assert.deepEqual(loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY), [
      'Africa Savanna',
      'Eurasia Wilds',
   ]);
});

test('saveSelectedNames normalizes exhibit names before persisting', () => {
   saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, new Set([' Africa Savanna ', '', 'Eurasia Wilds']));

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      ['Africa Savanna', 'Eurasia Wilds']
   );
});

test('removed animal keys round-trip through add, restore, and clear helpers', () => {
   addRemovedAnimalKey('African Penguin||Africa Savanna');
   addRemovedAnimalKey('  Masai Giraffe||Africa Savanna  ');

   const removedKeys = loadRemovedAnimalKeys();
   assert.equal(removedKeys.size, 2);
   assert.equal(removedKeys.has('african penguin||africa savanna'), true);

   restoreRemovedAnimalKey('African Penguin||Africa Savanna');
   assert.deepEqual(
      [...loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   restoreRemovedAnimalKey('unknown||nowhere');
   assert.deepEqual(
      [...loadRemovedAnimalKeys()],
      ['masai giraffe||africa savanna']
   );

   clearRemovedAnimalKeys();
   assert.equal(loadRemovedAnimalKeys().size, 0);
});

test('addRemovedAnimalKey ignores blank keys', () => {
   addRemovedAnimalKey('');
   addRemovedAnimalKey('   ');

   assert.equal(loadRemovedAnimalKeys().size, 0);
   assert.equal(localStorage.getItem(StorageKeys.REMOVED_ANIMALS_KEY), null);
});

test('clearRemovedAnimalKeysForExhibit drops keys for one exhibit only', () => {
   addRemovedAnimalKey('African Penguin||Africa Savanna');
   addRemovedAnimalKey('Masai Giraffe||Africa Savanna');
   addRemovedAnimalKey('Amur Tiger||Eurasia Wilds');

   clearRemovedAnimalKeysForExhibit('Africa Savanna');

   assert.deepEqual(
      [...loadRemovedAnimalKeys()].sort(),
      ['amur tiger||eurasia wilds']
   );
});

test('clearRemovedAnimalKeysForExhibit is a no-op for blank exhibit names', () => {
   addRemovedAnimalKey('African Penguin||Africa Savanna');

   clearRemovedAnimalKeysForExhibit('');
   clearRemovedAnimalKeysForExhibit('   ');

   assert.equal(loadRemovedAnimalKeys().size, 1);
});
