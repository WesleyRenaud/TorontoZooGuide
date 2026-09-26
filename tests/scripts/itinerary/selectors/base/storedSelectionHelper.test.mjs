import assert from 'node:assert/strict';
import test from 'node:test';

import { StoredSelectionHelper } from '../../../../../scripts/itinerary/selectors/base/storedSelectionHelper.js';


test('Test_NormalizeStoredSelectionItems_TestArray_ExpectSameItems', () => {
   const items = ['a'];

   const normalized = StoredSelectionHelper.normalizeStoredSelectionItems(items);

   assert.deepEqual(normalized, items);
});


test('Test_NormalizeStoredSelectionItems_TestNull_ExpectEmpty', () => {
   const value = null;

   const normalized = StoredSelectionHelper.normalizeStoredSelectionItems(value);

   assert.deepEqual(normalized, []);
});


test('Test_MigrateStoredSelectionItem_TestString_ExpectMapped', () => {
   const name = 'Carousel';

   const migrated = StoredSelectionHelper.migrateStoredSelectionItem(name, {
      fromString: (value) => value.toUpperCase(),
   });

   assert.equal(migrated, name.toUpperCase());
});


test('Test_MigrateStoredSelectionItem_TestObject_ExpectMapped', () => {
   const name = 'Zoomobile';
   const item = { name };

   const migrated = StoredSelectionHelper.migrateStoredSelectionItem(item, {
      fromObject: (value) => ({ title: value.name }),
   });

   assert.equal(migrated.title, name);
});


test('Test_MigrateStoredSelectionItem_TestNumber_ExpectNull', () => {
   const value = 42;

   const migrated = StoredSelectionHelper.migrateStoredSelectionItem(value);

   assert.equal(migrated, null);
});
