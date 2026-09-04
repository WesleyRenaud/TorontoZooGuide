import assert from 'node:assert/strict';
import test from 'node:test';

import { StoredSelection } from '../../../../../scripts/itinerary/selectors/base/storedSelection.js';

test('Test_NormalizeStoredString_TestTrimAndReject_ExpectTrimmedOrEmpty', () => {
   assert.equal(StoredSelection.normalizeStoredString('  African Lion  '), 'African Lion');
   assert.equal(StoredSelection.normalizeStoredString(42), '');
   assert.equal(StoredSelection.normalizeStoredString(null), '');
});

test('Test_NormalizeStoredBoolean_TestStrictTrue_ExpectOnlyTrue', () => {
   assert.equal(StoredSelection.normalizeStoredBoolean(true), true);
   assert.equal(StoredSelection.normalizeStoredBoolean(1), false);
   assert.equal(StoredSelection.normalizeStoredBoolean('true'), false);
});

test('Test_NormalizeStoredLink_TestBlankLinks_ExpectNull', () => {
   assert.equal(StoredSelection.normalizeStoredLink('  https://example.com  '), 'https://example.com');
   assert.equal(StoredSelection.normalizeStoredLink('   '), null);
   assert.equal(StoredSelection.normalizeStoredLink(null), null);
});

test('Test_NormalizeStoredId_TestBlankPrimary_ExpectFallback', () => {
   assert.equal(StoredSelection.normalizeStoredId('  row-1  ', 'fallback'), 'row-1');
   assert.equal(StoredSelection.normalizeStoredId(' ', 'fallback'), 'fallback');
   assert.equal(StoredSelection.normalizeStoredId(null, '  fallback  '), 'fallback');
});

test('Test_MigrateStoredSelectionItems_TestStringsAndObjects_ExpectNormalized', () => {
   const migrated = StoredSelection.migrateStoredSelectionItems(
      [
         '  African Lion  ',
         { name: '  Carousel  ', id: '' },
         42,
         null,
      ],
      {
         fromString: (value) => ({ id: value, name: value }),
         fromObject: (value) => (
            value.name
               ? { id: value.name, name: value.name }
               : null
         ),
      }
   );

   assert.deepEqual(migrated, [
      { id: '  African Lion  ', name: '  African Lion  ' },
      { id: '  Carousel  ', name: '  Carousel  ' },
   ]);
});

test('Test_MigrateStoredSelectionItems_TestNonArray_ExpectEmpty', () => {
   assert.deepEqual(
      StoredSelection.migrateStoredSelectionItems(null, {
         fromString: (value) => ({ id: value }),
      }),
      []
   );
});
