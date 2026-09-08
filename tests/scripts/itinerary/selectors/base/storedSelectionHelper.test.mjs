import assert from 'node:assert/strict';
import test from 'node:test';

import { StoredSelectionHelper } from '../../../../../scripts/itinerary/selectors/base/storedSelectionHelper.js';

test('Test_NormalizeStoredSelectionItems_TestInputs_ExpectArray', () => {
   assert.deepEqual(StoredSelectionHelper.normalizeStoredSelectionItems(['a']), ['a']);
   assert.deepEqual(StoredSelectionHelper.normalizeStoredSelectionItems(null), []);
});

test('Test_MigrateStoredSelectionItem_TestStringAndObject_ExpectMapped', () => {
   assert.equal(
      StoredSelectionHelper.migrateStoredSelectionItem('Carousel', {
         fromString: (value) => value.toUpperCase(),
      }),
      'CAROUSEL'
   );
   assert.deepEqual(
      StoredSelectionHelper.migrateStoredSelectionItem({ name: 'Zoomobile' }, {
         fromObject: (item) => ({ title: item.name }),
      }),
      { title: 'Zoomobile' }
   );
   assert.equal(StoredSelectionHelper.migrateStoredSelectionItem(42), null);
});
