import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { RegionStorageStore } from '../../../../../scripts/itinerary/selectors/regionSelector/regionStorageStore.js';
import { AnimalIdentity } from '../../../../../scripts/itinerary/animalIdentity.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { StorageKeys } from '../../../../../scripts/itinerary/storageKeys.js';
import { createLocalStorageMock } from '../../../helpers/localStorageMock.mjs';

beforeEach(() => {
   globalThis.localStorage = createLocalStorageMock();
});

afterEach(() => {
   delete globalThis.localStorage;
});


test('Test_LoadSelectedNames_TestWhitespaceAndNonStrings_ExpectTrimmedNames', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';
   const count = 42;
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([` ${savanna} `, '', count, eurasia])
   );

   const names = RegionStorageStore.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY);

   assert.deepEqual(names, [savanna, String(count), eurasia]);
});


test('Test_SaveSelectedNames_TestWhitespaceEntries_ExpectNormalizedPersist', () => {
   const savanna = 'Africa Savanna';
   const eurasia = 'Eurasia Wilds';

   RegionStorageStore.saveSelectedNames(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      new Set([` ${savanna} `, '', eurasia])
   );

   assert.deepEqual(
      JSON.parse(localStorage.getItem(StorageKeys.SELECTED_EXHIBITS_KEY)),
      [savanna, eurasia]
   );
});


test('Test_AddRemovedAnimalKey_TestKeys_ExpectNormalized', () => {
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };

   RegionStorageStore.addRemovedAnimalKey(
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   RegionStorageStore.addRemovedAnimalKey(
      `  ${[giraffe.species, giraffe.exhibit].join(ScheduleItemKeySeparator.VALUE)}  `
   );

   const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();

   assert.equal(removedKeys.size, 2);
   assert.equal(removedKeys.has(AnimalIdentity.buildAnimalIdentityStorageKey(penguin)), true);
});


test('Test_RestoreRemovedAnimalKey_TestKnownKey_ExpectRemoved', () => {
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };
   RegionStorageStore.addRemovedAnimalKey(
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   RegionStorageStore.addRemovedAnimalKey(
      `  ${[giraffe.species, giraffe.exhibit].join(ScheduleItemKeySeparator.VALUE)}  `
   );

   RegionStorageStore.restoreRemovedAnimalKey(
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );

   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()],
      [AnimalIdentity.buildAnimalIdentityStorageKey(giraffe)]
   );
});


test('Test_RestoreRemovedAnimalKey_TestUnknownKey_ExpectUnchanged', () => {
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };
   RegionStorageStore.addRemovedAnimalKey(
      [giraffe.species, giraffe.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );

   RegionStorageStore.restoreRemovedAnimalKey(
      ['unknown', 'nowhere'].join(ScheduleItemKeySeparator.VALUE)
   );

   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()],
      [AnimalIdentity.buildAnimalIdentityStorageKey(giraffe)]
   );
});


test('Test_ClearRemovedAnimalKeys_TestPresent_ExpectEmpty', () => {
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };
   RegionStorageStore.addRemovedAnimalKey(
      [giraffe.species, giraffe.exhibit].join(ScheduleItemKeySeparator.VALUE)
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
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   const giraffe = { species: 'Masai Giraffe', exhibit: 'Africa Savanna' };
   const tiger = { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' };
   RegionStorageStore.addRemovedAnimalKey(
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   RegionStorageStore.addRemovedAnimalKey(
      [giraffe.species, giraffe.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );
   RegionStorageStore.addRemovedAnimalKey(
      [tiger.species, tiger.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );

   RegionStorageStore.clearRemovedAnimalKeysForExhibit(penguin.exhibit);

   assert.deepEqual(
      [...RegionStorageStore.loadRemovedAnimalKeys()].sort(),
      [AnimalIdentity.buildAnimalIdentityStorageKey(tiger)]
   );
});


test('Test_ClearRemovedAnimalKeysForExhibit_TestBlankExhibit_ExpectNoOp', () => {
   const penguin = { species: 'African Penguin', exhibit: 'Africa Savanna' };
   RegionStorageStore.addRemovedAnimalKey(
      [penguin.species, penguin.exhibit].join(ScheduleItemKeySeparator.VALUE)
   );

   RegionStorageStore.clearRemovedAnimalKeysForExhibit('');
   RegionStorageStore.clearRemovedAnimalKeysForExhibit('   ');

   assert.equal(RegionStorageStore.loadRemovedAnimalKeys().size, 1);
});
