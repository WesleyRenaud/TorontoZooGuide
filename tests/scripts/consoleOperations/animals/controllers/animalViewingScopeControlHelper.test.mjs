import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingScopeControlHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControlHelper.js';
import { AnimalViewingModel } from '../../../../../scripts/shared/enums/animalViewingModel.js';

test('Test_AnimalHasIndoorAndOutdoorViewing_TestScopes_ExpectBoolean', () => {
   assert.equal(
      AnimalViewingScopeControlHelper.animalHasIndoorAndOutdoorViewing([
         AnimalViewingModel.INDOOR,
         AnimalViewingModel.OUTDOOR,
      ]),
      true
   );
   assert.equal(
      AnimalViewingScopeControlHelper.animalHasIndoorAndOutdoorViewing([
         AnimalViewingModel.INDOOR,
      ]),
      false
   );
});

test('Test_SingleSpecificViewingScope_TestScopes_ExpectSingleOrEmpty', () => {
   assert.equal(
      AnimalViewingScopeControlHelper.singleSpecificViewingScope([
         AnimalViewingModel.ALL,
         AnimalViewingModel.INDOOR,
      ]),
      AnimalViewingModel.INDOOR
   );
   assert.equal(
      AnimalViewingScopeControlHelper.singleSpecificViewingScope([
         AnimalViewingModel.INDOOR,
         AnimalViewingModel.OUTDOOR,
      ]),
      ''
   );
});
