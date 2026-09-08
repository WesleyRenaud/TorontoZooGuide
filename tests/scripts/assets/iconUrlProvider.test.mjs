import assert from 'node:assert/strict';
import test from 'node:test';

import { IconUrlProvider } from '../../../scripts/assets/iconUrlProvider.js';
import { IconUrlBuilder } from '../../../scripts/assets/iconUrlBuilder.js';

test('Test_GetAnimalAndAttractionIconUrl_TestNames_ExpectCssUrl', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalAnimal = IconUrlBuilder.buildAnimalIconPath;
   const originalAttraction = IconUrlBuilder.buildAttractionIconPath;
   IconUrlBuilder.buildCssUrl = (path) => `css:${path}`;
   IconUrlBuilder.buildAnimalIconPath = (...args) => `animal:${args.join('|')}`;
   IconUrlBuilder.buildAttractionIconPath = (...args) => `attraction:${args.join('|')}`;

   try {
      assert.equal(
         IconUrlProvider.getAnimalIconUrl('Savanna', 'Lion', 'green'),
         'css:animal:Savanna|Lion|green'
      );
      assert.equal(
         IconUrlProvider.getAttractionIconUrl('Carousel', 'blue'),
         'css:attraction:Carousel|blue'
      );
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildAnimalIconPath = originalAnimal;
      IconUrlBuilder.buildAttractionIconPath = originalAttraction;
   }
});

test('Test_GetGenericIconUrls_TestVariants_ExpectPaths', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   const originalGeneric = IconUrlBuilder.buildGenericIconPath;
   IconUrlBuilder.buildCssUrl = (path) => path;
   IconUrlBuilder.buildGenericIconPath = (type, colour) => `${type}:${colour}`;

   try {
      assert.equal(IconUrlProvider.getRestaurantIconUrl('open'), 'restaurant:open');
      assert.equal(IconUrlProvider.getGiftShopIconUrl('open'), 'gift-shop:open');
      assert.equal(IconUrlProvider.getRestroomIconUrl('closed'), '/images/icons/restroom/restroom-closed.png');
      assert.equal(IconUrlProvider.getRestroomIconUrl('open'), 'restroom:open');
      assert.equal(
         IconUrlProvider.getDrinkingFountainIconUrl('closed'),
         '/images/icons/drinking-fountain/drinking-fountain-closed.png'
      );
      assert.equal(IconUrlProvider.getDrinkingFountainIconUrl('open'), 'drinking-fountain:open');
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
      IconUrlBuilder.buildGenericIconPath = originalGeneric;
   }
});

test('Test_GetGuestServiceAndEventSiteIconUrl_TestNames_ExpectNormalized', () => {
   const originalCss = IconUrlBuilder.buildCssUrl;
   IconUrlBuilder.buildCssUrl = (path) => path;

   try {
      assert.equal(
         IconUrlProvider.getGuestServiceIconUrl('First Aid'),
         '/images/icons/guest-services/first-aid.png'
      );
      assert.equal(
         IconUrlProvider.getEventSiteIconUrl('Main Stage'),
         '/images/icons/event-center/main-stage.png'
      );
   } finally {
      IconUrlBuilder.buildCssUrl = originalCss;
   }
});
