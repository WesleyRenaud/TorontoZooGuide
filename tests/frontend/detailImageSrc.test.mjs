import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildDetailImageSrc,
   buildDetailImageSrcFromParts,
} from '../../scripts/assets/detailImageSrc.js';

test('buildDetailImageSrc normalizes the name and builds the asset path', () => {
   assert.equal(
      buildDetailImageSrc('restaurants', 'Wolf\'s Den'),
      'images/details/restaurants/wolfs-den.png'
   );
});

test('buildDetailImageSrc returns null for blank names', () => {
   assert.equal(buildDetailImageSrc('restaurants', '   '), null);
   assert.equal(buildDetailImageSrc('restaurants', ''), null);
});

test('buildDetailImageSrc supports a custom base path', () => {
   assert.equal(
      buildDetailImageSrc('animals', 'African Lion', { basePath: 'assets/details' }),
      'assets/details/animals/african-lion.png'
   );
});

test('buildDetailImageSrcFromParts joins normalized path segments', () => {
   assert.equal(
      buildDetailImageSrcFromParts(['animals', 'Africa Savanna', 'African Lion']),
      'images/details/animals/africa-savanna/african-lion.png'
   );
});

test('buildDetailImageSrcFromParts returns null when any segment is invalid', () => {
   assert.equal(
      buildDetailImageSrcFromParts(['animals', '   ', 'African Lion']),
      null
   );
});
