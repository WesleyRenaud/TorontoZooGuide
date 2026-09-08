import assert from 'node:assert/strict';
import test from 'node:test';

import { StorageKeys } from '../../../scripts/itinerary/storageKeys.js';

test('Test_StorageKeys_TestConstants_ExpectPrefixedValues', () => {
   assert.equal(StorageKeys.ITIN_KEY, 'tzg.itinerary');
   assert.equal(StorageKeys.DATE_KEY, 'tzg.itineraryDate');
   assert.equal(StorageKeys.ANIMALS_KEY, 'tzg.itineraryAnimals');
   assert.equal(StorageKeys.ATTRACTIONS_KEY, 'tzg.itineraryAttractions');
   assert.equal(StorageKeys.GUARDIANS_KEY, 'tzg.itineraryGuardiansTalks');
   assert.equal(StorageKeys.WILD_KEY, 'tzg.itineraryWildEncounters');
   assert.equal(StorageKeys.TRANSPORTATIONS_KEY, 'tzg.itineraryTransportations');
   assert.equal(StorageKeys.SELECTED_EXHIBITS_KEY, 'tzg.itinerarySelectedExhibits');
   assert.equal(StorageKeys.SELECTED_REGIONS_KEY, 'tzg.itinerarySelectedRegions');
   assert.equal(StorageKeys.REMOVED_ANIMALS_KEY, 'tzg.itineraryRemovedAnimals');
});
