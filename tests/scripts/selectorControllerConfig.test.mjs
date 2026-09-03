import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildSelectionFingerprint,
   validateSelectorConfig,
} from '../../scripts/itinerary/selectors/selectorControllerConfig.js';

test('buildSelectionFingerprint normalizes ids for stable comparisons', () => {
   assert.equal(
      buildSelectionFingerprint([
         { id: ' zebra ' },
         { id: 'Lion' },
         { id: '' },
      ]),
      'Lion\0zebra'
   );
});

test('validateSelectorConfig requires storageKey, getId, and extractRows', () => {
   assert.throws(
      () => validateSelectorConfig({
         getId: () => 'id',
         extractRows: () => [],
      }),
      /storageKey is required/
   );

   assert.throws(
      () => validateSelectorConfig({
         storageKey: 'tzg.items',
         extractRows: () => [],
      }),
      /getId\(row\) is required/
   );

   assert.throws(
      () => validateSelectorConfig({
         storageKey: 'tzg.items',
         getId: () => 'id',
      }),
      /extractRows\(response\) is required/
   );

   assert.doesNotThrow(() => validateSelectorConfig({
      storageKey: 'tzg.items',
      getId: () => 'id',
      extractRows: () => [],
   }));
});
