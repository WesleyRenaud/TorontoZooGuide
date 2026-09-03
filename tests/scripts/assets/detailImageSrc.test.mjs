import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageSrc } from '../../../scripts/assets/detailImageSrc.js';

test('Test_BuildDetailImageSrc_TestNamedAsset_ExpectNormalizedPath', () => {
   assert.equal(
      DetailImageSrc.buildDetailImageSrc('restaurants', 'Wolf\'s Den'),
      'images/details/restaurants/wolfs-den.png'
   );
});

test('Test_BuildDetailImageSrc_TestBlankName_ExpectNull', () => {
   assert.equal(DetailImageSrc.buildDetailImageSrc('restaurants', '   '), null);
   assert.equal(DetailImageSrc.buildDetailImageSrc('restaurants', ''), null);
});

test('Test_BuildDetailImageSrc_TestCustomBasePath_ExpectPrefixedPath', () => {
   assert.equal(
      DetailImageSrc.buildDetailImageSrc('animals', 'African Lion', { basePath: 'assets/details' }),
      'assets/details/animals/african-lion.png'
   );
});

test('Test_BuildDetailImageSrcFromParts_TestValidSegments_ExpectJoinedPath', () => {
   assert.equal(
      DetailImageSrc.buildDetailImageSrcFromParts(['animals', 'Africa Savanna', 'African Lion']),
      'images/details/animals/africa-savanna/african-lion.png'
   );
});

test('Test_BuildDetailImageSrcFromParts_TestInvalidSegment_ExpectNull', () => {
   assert.equal(
      DetailImageSrc.buildDetailImageSrcFromParts(['animals', '   ', 'African Lion']),
      null
   );
});
