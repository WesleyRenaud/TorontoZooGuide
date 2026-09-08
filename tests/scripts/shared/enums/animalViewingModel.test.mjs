import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingModel } from '../../../../scripts/shared/enums/animalViewingModel.js';

test('Test_AnimalViewingModel_TestConstants_ExpectStableValues', () => {
   assert.equal(AnimalViewingModel.ALL, 'all');
   assert.equal(AnimalViewingModel.INDOOR, 'indoor');
   assert.equal(AnimalViewingModel.OUTDOOR, 'outdoor');
});
