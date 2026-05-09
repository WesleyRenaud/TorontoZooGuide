import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildHoverText } from '../../scripts/markers/markerHoverText.js';

test('formats Meet the Guardians talk marker hover text', () => {
   assert.equal(
      buildHoverText([
         {
            type: 'guardiansTalk',
            name: 'Amur Tiger',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk'
   );
});

test('formats counted Meet the Guardians talk marker hover text', () => {
   assert.equal(
      buildHoverText([
         {
            type: 'guardiansTalk',
            name: 'Amur Tiger',
         },
         {
            type: 'guardiansTalk',
            name: 'African Lion',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk + 1'
   );
});
