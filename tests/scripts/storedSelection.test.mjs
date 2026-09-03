import assert from 'node:assert/strict';
import test from 'node:test';

import {
   migrateStoredSelectionItems,
   normalizeStoredBoolean,
   normalizeStoredId,
   normalizeStoredLink,
   normalizeStoredString,
} from '../../scripts/itinerary/selectors/base/storedSelection.js';

test('normalizeStoredString trims strings and rejects other values', () => {
   assert.equal(normalizeStoredString('  African Lion  '), 'African Lion');
   assert.equal(normalizeStoredString(42), '');
   assert.equal(normalizeStoredString(null), '');
});

test('normalizeStoredBoolean accepts only strict true', () => {
   assert.equal(normalizeStoredBoolean(true), true);
   assert.equal(normalizeStoredBoolean(1), false);
   assert.equal(normalizeStoredBoolean('true'), false);
});

test('normalizeStoredLink returns null for blank links', () => {
   assert.equal(normalizeStoredLink('  https://example.com  '), 'https://example.com');
   assert.equal(normalizeStoredLink('   '), null);
   assert.equal(normalizeStoredLink(null), null);
});

test('normalizeStoredId falls back when the primary id is blank', () => {
   assert.equal(normalizeStoredId('  row-1  ', 'fallback'), 'row-1');
   assert.equal(normalizeStoredId(' ', 'fallback'), 'fallback');
   assert.equal(normalizeStoredId(null, '  fallback  '), 'fallback');
});

test('migrateStoredSelectionItems normalizes strings and objects', () => {
   const migrated = migrateStoredSelectionItems(
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

test('migrateStoredSelectionItems treats non-array input as empty', () => {
   assert.deepEqual(
      migrateStoredSelectionItems(null, {
         fromString: (value) => ({ id: value }),
      }),
      []
   );
});
