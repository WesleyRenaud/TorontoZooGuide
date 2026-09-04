import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorControllerConfig } from '../../../../scripts/itinerary/selectors/selectorControllerConfig.js';

test('Test_BuildSelectionFingerprint_TestIds_ExpectNormalized', () => {
   assert.equal(
      SelectorControllerConfig.buildSelectionFingerprint([
         { id: ' zebra ' },
         { id: 'Lion' },
         { id: '' },
      ]),
      'Lion\0zebra'
   );
});

test('Test_ValidateSelectorConfig_TestRequiredFields_ExpectThrowsOrPasses', () => {
   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig({
         getId: () => 'id',
         extractRows: () => [],
      }),
      /storageKey is required/
   );

   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig({
         storageKey: 'tzg.items',
         extractRows: () => [],
      }),
      /getId\(row\) is required/
   );

   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig({
         storageKey: 'tzg.items',
         getId: () => 'id',
      }),
      /extractRows\(response\) is required/
   );

   assert.doesNotThrow(() => SelectorControllerConfig.validateSelectorConfig({
      storageKey: 'tzg.items',
      getId: () => 'id',
      extractRows: () => [],
   }));
});
