import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesSourceNormalizer } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesSourceNormalizer.js';

test('Test_NormalizeSpeciesList_TestDuplicatesAndWhitespace_ExpectUniqueSorted', () => {
   assert.deepEqual(
      SpeciesSourceNormalizer.normalizeSpeciesList([
         '  Amur Tiger  ',
         'African Lion',
         'Amur Tiger',
         '',
         '  ',
         null,
      ]),
      ['African Lion', 'Amur Tiger']
   );
});

test('Test_NormalizeSpeciesList_TestMissingList_ExpectEmpty', () => {
   assert.deepEqual(SpeciesSourceNormalizer.normalizeSpeciesList(null), []);
   assert.deepEqual(SpeciesSourceNormalizer.normalizeSpeciesList(undefined), []);
});
