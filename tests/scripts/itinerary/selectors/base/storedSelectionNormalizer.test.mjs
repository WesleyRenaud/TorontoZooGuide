import assert from 'node:assert/strict';
import test from 'node:test';

import { StoredSelectionNormalizer } from '../../../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';

test('Test_NormalizeStoredString_TestTrimAndReject_ExpectTrimmedOrEmpty', () => {
   assert.equal(StoredSelectionNormalizer.normalizeStoredString('  African Lion  '), 'African Lion');
   assert.equal(StoredSelectionNormalizer.normalizeStoredString(42), '');
   assert.equal(StoredSelectionNormalizer.normalizeStoredString(null), '');
});

test('Test_NormalizeStoredBoolean_TestStrictTrue_ExpectOnlyTrue', () => {
   assert.equal(StoredSelectionNormalizer.normalizeStoredBoolean(true), true);
   assert.equal(StoredSelectionNormalizer.normalizeStoredBoolean(1), false);
   assert.equal(StoredSelectionNormalizer.normalizeStoredBoolean('true'), false);
});

test('Test_NormalizeStoredLink_TestBlankLinks_ExpectNull', () => {
   assert.equal(StoredSelectionNormalizer.normalizeStoredLink('  https://example.com  '), 'https://example.com');
   assert.equal(StoredSelectionNormalizer.normalizeStoredLink('   '), null);
   assert.equal(StoredSelectionNormalizer.normalizeStoredLink(null), null);
});

test('Test_NormalizeStoredId_TestBlankPrimary_ExpectFallback', () => {
   assert.equal(StoredSelectionNormalizer.normalizeStoredId('  row-1  ', 'fallback'), 'row-1');
   assert.equal(StoredSelectionNormalizer.normalizeStoredId(' ', 'fallback'), 'fallback');
   assert.equal(StoredSelectionNormalizer.normalizeStoredId(null, '  fallback  '), 'fallback');
});

test('Test_MigrateStoredSelectionItems_TestStringsAndObjects_ExpectNormalized', () => {
   const migrated = StoredSelectionNormalizer.migrateStoredSelectionItems(
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
      StoredSelectionNormalizer.migrateStoredSelectionItems(null, {
         fromString: (value) => ({ id: value }),
      }),
      []
   );
});
