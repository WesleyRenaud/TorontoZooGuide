import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorControllerConfig } from '../../../../scripts/itinerary/selectors/selectorControllerConfig.js';


test('Test_BuildSelectionFingerprint_TestIds_ExpectNormalized', () => {
   const zebra = 'zebra';
   const lion = 'Lion';
   const items = [
      { id: ` ${zebra} ` },
      { id: lion },
      { id: '' },
   ];

   const fingerprint = SelectorControllerConfig.buildSelectionFingerprint(items);

   assert.equal(fingerprint, [lion, zebra].join('\0'));
});


test('Test_ValidateSelectorConfig_TestMissingStorageKey_ExpectThrows', () => {
   const config = {
      getId: () => 'id',
      extractRows: () => [],
   };

   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig(config),
      /storageKey is required/
   );
});


test('Test_ValidateSelectorConfig_TestMissingGetId_ExpectThrows', () => {
   const config = {
      storageKey: 'tzg.items',
      extractRows: () => [],
   };

   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig(config),
      /getId\(row\) is required/
   );
});


test('Test_ValidateSelectorConfig_TestMissingExtractRows_ExpectThrows', () => {
   const config = {
      storageKey: 'tzg.items',
      getId: () => 'id',
   };

   assert.throws(
      () => SelectorControllerConfig.validateSelectorConfig(config),
      /extractRows\(response\) is required/
   );
});


test('Test_ValidateSelectorConfig_TestRequiredFields_ExpectPasses', () => {
   const config = {
      storageKey: 'tzg.items',
      getId: () => 'id',
      extractRows: () => [],
   };

   assert.doesNotThrow(() => SelectorControllerConfig.validateSelectorConfig(config));
});
