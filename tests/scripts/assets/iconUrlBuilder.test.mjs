import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { IconUrlBuilder } from '../../../scripts/assets/iconUrlBuilder.js';


test('Test_BuildCssUrl_TestPath_ExpectCssUrl', () => {
   const path = '/images/icon.png';

   const cssUrl = IconUrlBuilder.buildCssUrl(path);

   assert.equal(cssUrl, `url("${path}")`);
});


test('Test_IsOpenIconVariant_TestEmpty_ExpectTrue', () => {
   const token = '';

   const isOpen = IconUrlBuilder.isOpenIconVariant(token);

   assert.equal(isOpen, true);
});


test('Test_IsOpenIconVariant_TestOpen_ExpectTrue', () => {
   const token = 'OPEN';

   const isOpen = IconUrlBuilder.isOpenIconVariant(token);

   assert.equal(isOpen, true);
});


test('Test_IsOpenIconVariant_TestClosed_ExpectFalse', () => {
   const token = 'closed';

   const isOpen = IconUrlBuilder.isOpenIconVariant(token);

   assert.equal(isOpen, false);
});


test('Test_BuildAnimalIconPath_TestParts_ExpectNormalizedPath', () => {
   const exhibit = 'African Savanna';
   const species = 'African Lion';
   const variant = 'open';

   const path = IconUrlBuilder.buildAnimalIconPath(exhibit, species, variant);

   assert.equal(
      path,
      `/images/icons/animals/${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(species)}/${AssetKeyNormalizer.normalize(species)}-${variant}.png`
   );
});


test('Test_BuildAttractionIconPath_TestOpen_ExpectOpenPath', () => {
   const name = 'Conservation Carousel';
   const variant = 'open';

   const path = IconUrlBuilder.buildAttractionIconPath(name, variant);

   assert.equal(path, `/images/icons/attractions/${AssetKeyNormalizer.normalize(name)}-${variant}.png`);
});


test('Test_BuildAttractionIconPath_TestClosed_ExpectVariantPath', () => {
   const name = 'Conservation Carousel';
   const variant = 'closed';

   const path = IconUrlBuilder.buildAttractionIconPath(name, variant);

   assert.equal(
      path,
      `/images/icons/attractions/${AssetKeyNormalizer.normalize(name)}/${AssetKeyNormalizer.normalize(name)}-${variant}.png`
   );
});


test('Test_BuildGenericIconPath_TestOpen_ExpectOpenPath', () => {
   const iconName = 'restroom';
   const variant = '';

   const path = IconUrlBuilder.buildGenericIconPath(iconName, variant);

   assert.equal(path, `/images/icons/${iconName}/${iconName}-open.png`);
});


test('Test_BuildGenericIconPath_TestClosed_ExpectClosedPath', () => {
   const iconName = 'restroom';
   const variant = 'closed';

   const path = IconUrlBuilder.buildGenericIconPath(iconName, variant);

   assert.equal(path, `/images/icons/${iconName}/${iconName}-${variant}.png`);
});
