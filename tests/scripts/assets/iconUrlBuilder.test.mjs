import assert from 'node:assert/strict';
import test from 'node:test';

import { IconUrlBuilder } from '../../../scripts/assets/iconUrlBuilder.js';

test('Test_BuildCssUrl_TestPath_ExpectCssUrl', () => {
   assert.equal(IconUrlBuilder.buildCssUrl('/images/icon.png'), 'url("/images/icon.png")');
});

test('Test_IsOpenIconVariant_TestTokens_ExpectOpenDetection', () => {
   assert.equal(IconUrlBuilder.isOpenIconVariant(''), true);
   assert.equal(IconUrlBuilder.isOpenIconVariant('OPEN'), true);
   assert.equal(IconUrlBuilder.isOpenIconVariant('closed'), false);
});

test('Test_BuildAnimalIconPath_TestParts_ExpectNormalizedPath', () => {
   assert.equal(
      IconUrlBuilder.buildAnimalIconPath('African Savanna', 'African Lion', 'open'),
      '/images/icons/animals/african-savanna/african-lion/african-lion-open.png'
   );
});

test('Test_BuildAttractionIconPath_TestOpenAndVariant_ExpectPaths', () => {
   assert.equal(
      IconUrlBuilder.buildAttractionIconPath('Conservation Carousel', 'open'),
      '/images/icons/attractions/conservation-carousel-open.png'
   );
   assert.equal(
      IconUrlBuilder.buildAttractionIconPath('Conservation Carousel', 'closed'),
      '/images/icons/attractions/conservation-carousel/conservation-carousel-closed.png'
   );
});

test('Test_BuildGenericIconPath_TestVariants_ExpectPaths', () => {
   assert.equal(
      IconUrlBuilder.buildGenericIconPath('restroom', ''),
      '/images/icons/restroom/restroom-open.png'
   );
   assert.equal(
      IconUrlBuilder.buildGenericIconPath('restroom', 'closed'),
      '/images/icons/restroom/restroom-closed.png'
   );
});
