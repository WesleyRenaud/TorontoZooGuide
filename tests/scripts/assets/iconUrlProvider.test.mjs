import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { IconUrlBuilder } from '../../../scripts/assets/iconUrlBuilder.js';
import { IconUrlProvider } from '../../../scripts/assets/iconUrlProvider.js';


test('Test_GetAnimalIconUrl_TestNames_ExpectCssUrl', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalAnimal = IconUrlBuilder.buildAnimalIconPath;
   const exhibit = 'Savanna';
   const species = 'Lion';
   const variant = 'green';
   IconUrlBuilder.buildCssUrl = (path) => `css:${path}`;
   IconUrlBuilder.buildAnimalIconPath = (...args) => `animal:${args.join('|')}`;

   try {
      const url = IconUrlProvider.getAnimalIconUrl(exhibit, species, variant);

      assert.equal(url, `css:animal:${exhibit}|${species}|${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildAnimalIconPath = originalAnimal;
   }
});


test('Test_GetAttractionIconUrl_TestNames_ExpectCssUrl', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalAttraction = IconUrlBuilder.buildAttractionIconPath;
   const name = 'Carousel';
   const variant = 'blue';
   IconUrlBuilder.buildCssUrl = (path) => `css:${path}`;
   IconUrlBuilder.buildAttractionIconPath = (...args) => `attraction:${args.join('|')}`;

   try {
      const url = IconUrlProvider.getAttractionIconUrl(name, variant);

      assert.equal(url, `css:attraction:${name}|${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildAttractionIconPath = originalAttraction;
   }
});


test('Test_GetRestaurantIconUrl_TestOpen_ExpectPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalGeneric = IconUrlBuilder.buildGenericIconPath;
   const variant = 'open';
   IconUrlBuilder.buildCssUrl = (path) => path;
   IconUrlBuilder.buildGenericIconPath = (type, colour) => `${type}:${colour}`;

   try {
      const url = IconUrlProvider.getRestaurantIconUrl(variant);

      assert.equal(url, `restaurant:${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildGenericIconPath = originalGeneric;
   }
});


test('Test_GetGiftShopIconUrl_TestOpen_ExpectPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalGeneric = IconUrlBuilder.buildGenericIconPath;
   const variant = 'open';
   IconUrlBuilder.buildCssUrl = (path) => path;
   IconUrlBuilder.buildGenericIconPath = (type, colour) => `${type}:${colour}`;

   try {
      const url = IconUrlProvider.getGiftShopIconUrl(variant);

      assert.equal(url, `gift-shop:${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildGenericIconPath = originalGeneric;
   }
});


test('Test_GetRestroomIconUrl_TestClosed_ExpectClosedPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const variant = 'closed';
   const closedPath = '/images/icons/restroom/restroom-closed.png';
   IconUrlBuilder.buildCssUrl = (path) => path;

   try {
      const url = IconUrlProvider.getRestroomIconUrl(variant);

      assert.equal(url, closedPath);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
   }
});


test('Test_GetRestroomIconUrl_TestOpen_ExpectPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalGeneric = IconUrlBuilder.buildGenericIconPath;
   const variant = 'open';
   IconUrlBuilder.buildCssUrl = (path) => path;
   IconUrlBuilder.buildGenericIconPath = (type, colour) => `${type}:${colour}`;

   try {
      const url = IconUrlProvider.getRestroomIconUrl(variant);

      assert.equal(url, `restroom:${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildGenericIconPath = originalGeneric;
   }
});


test('Test_GetDrinkingFountainIconUrl_TestClosed_ExpectClosedPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const variant = 'closed';
   const closedPath = '/images/icons/drinking-fountain/drinking-fountain-closed.png';
   IconUrlBuilder.buildCssUrl = (path) => path;

   try {
      const url = IconUrlProvider.getDrinkingFountainIconUrl(variant);

      assert.equal(url, closedPath);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
   }
});


test('Test_GetDrinkingFountainIconUrl_TestOpen_ExpectPath', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalGeneric = IconUrlBuilder.buildGenericIconPath;
   const variant = 'open';
   IconUrlBuilder.buildCssUrl = (path) => path;
   IconUrlBuilder.buildGenericIconPath = (type, colour) => `${type}:${colour}`;

   try {
      const url = IconUrlProvider.getDrinkingFountainIconUrl(variant);

      assert.equal(url, `drinking-fountain:${variant}`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildGenericIconPath = originalGeneric;
   }
});


test('Test_GetGuestServiceIconUrl_TestName_ExpectNormalized', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const name = 'First Aid';
   IconUrlBuilder.buildCssUrl = (path) => path;

   try {
      const url = IconUrlProvider.getGuestServiceIconUrl(name);

      assert.equal(url, `/images/icons/guest-services/${AssetKeyNormalizer.normalize(name)}.png`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
   }
});


test('Test_GetEventSiteIconUrl_TestName_ExpectNormalized', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const name = 'Main Stage';
   IconUrlBuilder.buildCssUrl = (path) => path;

   try {
      const url = IconUrlProvider.getEventSiteIconUrl(name);

      assert.equal(url, `/images/icons/event-center/${AssetKeyNormalizer.normalize(name)}.png`);
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
   }
});
