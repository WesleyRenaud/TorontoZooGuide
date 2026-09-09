import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { AnimalViewingScope } from '../../../../scripts/shared/enums/animalViewingScope.js';
import animalViewingScopeValues from '../../../../shared/enums/animalViewingScope.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_AnimalViewingScope_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(animalViewingScopeValues)) {
      assert.equal(AnimalViewingScope[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/animalViewingScope.json'), 'utf8')
   );
   assert.deepEqual(animalViewingScopeValues, diskValues);
   assert.deepEqual(AnimalViewingScope.wireValues().sort(), Object.values(diskValues).sort());
});
