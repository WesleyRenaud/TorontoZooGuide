import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import positionValues from '../../../../shared/enums/position.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_Position_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/position.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(positionValues).map((key) => [key, Position[key]])
   );

   assert.deepEqual(mapped, positionValues);
   assert.deepEqual(positionValues, diskValues);
});


test('Test_Position_TestFirst_ExpectFirstItem', () => {
   const first = 'African Lion';
   const items = [first, 'Amur Tiger', 'Snow Leopard', 'Komodo Dragon'];

   const item = items[Position.FIRST];

   assert.equal(item, first);
});


test('Test_Position_TestSecond_ExpectSecondItem', () => {
   const second = 'Amur Tiger';
   const items = ['African Lion', second, 'Snow Leopard', 'Komodo Dragon'];

   const item = items[Position.SECOND];

   assert.equal(item, second);
});


test('Test_Position_TestThird_ExpectThirdItem', () => {
   const third = 'Snow Leopard';
   const items = ['African Lion', 'Amur Tiger', third, 'Komodo Dragon'];

   const item = items[Position.THIRD];

   assert.equal(item, third);
});


test('Test_Position_TestFourth_ExpectFourthItem', () => {
   const fourth = 'Komodo Dragon';
   const items = ['African Lion', 'Amur Tiger', 'Snow Leopard', fourth];

   const item = items[Position.FOURTH];

   assert.equal(item, fourth);
});


test('Test_Position_TestLast_ExpectLastItem', () => {
   const last = 'Komodo Dragon';
   const items = ['African Lion', 'Amur Tiger', 'Snow Leopard', last];

   const item = items.at(Position.LAST);

   assert.equal(item, last);
});
