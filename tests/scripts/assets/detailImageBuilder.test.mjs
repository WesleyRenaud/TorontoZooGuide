import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';


test('Test_BuildDetailImageSrc_TestNamedAsset_ExpectNormalizedPath', () => {
   const kind = 'restaurants';
   const name = 'Wolf\'s Den Café';
   const basePath = 'images/details';

   const src = DetailImageBuilder.buildDetailImageSrc(kind, name);

   assert.equal(src, `${basePath}/${kind}/${AssetKeyNormalizer.normalize(name)}.png`);
});


test('Test_BuildDetailImageSrc_TestBlankName_ExpectNull', () => {
   const kind = 'restaurants';
   const name = '   ';

   const src = DetailImageBuilder.buildDetailImageSrc(kind, name);

   assert.equal(src, null);
});


test('Test_BuildDetailImageSrc_TestEmptyName_ExpectNull', () => {
   const kind = 'restaurants';
   const name = '';

   const src = DetailImageBuilder.buildDetailImageSrc(kind, name);

   assert.equal(src, null);
});


test('Test_BuildDetailImageSrc_TestCustomBasePath_ExpectPrefixedPath', () => {
   const kind = 'animals';
   const name = 'African Lion';
   const basePath = 'assets/details';

   const src = DetailImageBuilder.buildDetailImageSrc(kind, name, { basePath });

   assert.equal(src, `${basePath}/${kind}/${AssetKeyNormalizer.normalize(name)}.png`);
});


test('Test_BuildDetailImageSrcFromParts_TestValidSegments_ExpectJoinedPath', () => {
   const parts = ['animals', 'Africa Savanna', 'African Lion'];
   const basePath = 'images/details';

   const src = DetailImageBuilder.buildDetailImageSrcFromParts(parts);

   assert.equal(
      src,
      `${basePath}/${parts.map((part) => AssetKeyNormalizer.normalize(part)).join('/')}.png`
   );
});


test('Test_BuildDetailImageSrcFromParts_TestInvalidSegment_ExpectNull', () => {
   const parts = ['animals', '   ', 'African Lion'];

   const src = DetailImageBuilder.buildDetailImageSrcFromParts(parts);

   assert.equal(src, null);
});
