import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';

test('Test_BuildDetailImageSrc_TestNamedAsset_ExpectNormalizedPath', () => {
   assert.equal(
      DetailImageBuilder.buildDetailImageSrc('restaurants', 'Wolf\'s Den Café'),
      'images/details/restaurants/wolfs-den-cafe.png'
   );
});

test('Test_BuildDetailImageSrc_TestBlankName_ExpectNull', () => {
   assert.equal(DetailImageBuilder.buildDetailImageSrc('restaurants', '   '), null);
   assert.equal(DetailImageBuilder.buildDetailImageSrc('restaurants', ''), null);
});

test('Test_BuildDetailImageSrc_TestCustomBasePath_ExpectPrefixedPath', () => {
   assert.equal(
      DetailImageBuilder.buildDetailImageSrc('animals', 'African Lion', { basePath: 'assets/details' }),
      'assets/details/animals/african-lion.png'
   );
});

test('Test_BuildDetailImageSrcFromParts_TestValidSegments_ExpectJoinedPath', () => {
   assert.equal(
      DetailImageBuilder.buildDetailImageSrcFromParts(['animals', 'Africa Savanna', 'African Lion']),
      'images/details/animals/africa-savanna/african-lion.png'
   );
});

test('Test_BuildDetailImageSrcFromParts_TestInvalidSegment_ExpectNull', () => {
   assert.equal(
      DetailImageBuilder.buildDetailImageSrcFromParts(['animals', '   ', 'African Lion']),
      null
   );
});
