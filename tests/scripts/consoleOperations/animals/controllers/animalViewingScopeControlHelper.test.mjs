import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingScopeControlHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControlHelper.js';
import { AnimalViewingScope } from '../../../../../scripts/shared/enums/animalViewingScope.js';

test('Test_AnimalHasIndoorAndOutdoorViewing_TestScopes_ExpectBoolean', () => {
   assert.equal(
      AnimalViewingScopeControlHelper.animalHasIndoorAndOutdoorViewing([
         AnimalViewingScope.INDOOR,
         AnimalViewingScope.OUTDOOR,
      ]),
      true
   );
   assert.equal(
      AnimalViewingScopeControlHelper.animalHasIndoorAndOutdoorViewing([
         AnimalViewingScope.INDOOR,
      ]),
      false
   );
});

test('Test_SingleSpecificViewingScope_TestScopes_ExpectSingleOrEmpty', () => {
   assert.equal(
      AnimalViewingScopeControlHelper.singleSpecificViewingScope([
         AnimalViewingScope.ALL,
         AnimalViewingScope.INDOOR,
      ]),
      AnimalViewingScope.INDOOR
   );
   assert.equal(
      AnimalViewingScopeControlHelper.singleSpecificViewingScope([
         AnimalViewingScope.INDOOR,
         AnimalViewingScope.OUTDOOR,
      ]),
      ''
   );
});
