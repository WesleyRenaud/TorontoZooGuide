import assert from 'node:assert/strict';
import test from 'node:test';

import { StoredSelectionNormalizer } from '../../../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_NormalizeStoredBoolean_TestTrue_ExpectTrue', () => {
   const value = true;

   const flag = StoredSelectionNormalizer.normalizeStoredBoolean(value);

   assert.equal(flag, value);
});


test('Test_NormalizeStoredBoolean_TestOne_ExpectFalse', () => {
   const value = 1;

   const flag = StoredSelectionNormalizer.normalizeStoredBoolean(value);

   assert.equal(flag, false);
});


test('Test_NormalizeStoredBoolean_TestTrueString_ExpectFalse', () => {
   const value = 'true';

   const flag = StoredSelectionNormalizer.normalizeStoredBoolean(value);

   assert.equal(flag, false);
});


test('Test_NormalizeStoredLink_TestWhitespace_ExpectTrimmed', () => {
   const link = 'https://example.com';
   const value = `  ${link}  `;

   const normalized = StoredSelectionNormalizer.normalizeStoredLink(value);

   assert.equal(normalized, link);
});


test('Test_NormalizeStoredLink_TestBlank_ExpectNull', () => {
   const value = '   ';

   const normalized = StoredSelectionNormalizer.normalizeStoredLink(value);

   assert.equal(normalized, null);
});


test('Test_NormalizeStoredLink_TestNull_ExpectNull', () => {
   const value = null;

   const normalized = StoredSelectionNormalizer.normalizeStoredLink(value);

   assert.equal(normalized, null);
});


test('Test_NormalizeStoredId_TestWhitespace_ExpectTrimmed', () => {
   const id = 'row-1';
   const value = `  ${id}  `;
   const fallback = 'fallback';

   const normalized = StoredSelectionNormalizer.normalizeStoredId(value, fallback);

   assert.equal(normalized, id);
});


test('Test_NormalizeStoredId_TestBlankPrimary_ExpectFallback', () => {
   const value = ' ';
   const fallback = 'fallback';

   const normalized = StoredSelectionNormalizer.normalizeStoredId(value, fallback);

   assert.equal(normalized, fallback);
});


test('Test_NormalizeStoredId_TestNullPrimary_ExpectTrimmedFallback', () => {
   const value = null;
   const fallback = 'fallback';
   const paddedFallback = `  ${fallback}  `;

   const normalized = StoredSelectionNormalizer.normalizeStoredId(value, paddedFallback);

   assert.equal(normalized, fallback);
});


test('Test_MigrateStoredSelectionItems_TestStringsAndObjects_ExpectNormalized', () => {
   const lion = 'African Lion';
   const carousel = 'Carousel';
   const paddedLion = `  ${lion}  `;
   const paddedCarousel = `  ${carousel}  `;
   const items = [
      paddedLion,
      { name: paddedCarousel, id: '' },
      42,
      null,
   ];

   const migrated = StoredSelectionNormalizer.migrateStoredSelectionItems(
      items,
      {
         fromString: (value) => ({ id: value, name: value }),
         fromObject: (value) => (
            value.name
               ? { id: value.name, name: value.name }
               : null
         ),
      }
   );

   assert.equal(migrated.length, 2);
   assert.deepEqual(migrated.at(Position.FIRST), { id: paddedLion, name: paddedLion });
   assert.deepEqual(migrated.at(Position.SECOND), {
      id: paddedCarousel,
      name: paddedCarousel,
   });
});


test('Test_MigrateStoredSelectionItems_TestNonArray_ExpectEmpty', () => {
   const value = null;

   const migrated = StoredSelectionNormalizer.migrateStoredSelectionItems(value, {
      fromString: (item) => ({ id: item }),
   });

   assert.deepEqual(migrated, []);
});
