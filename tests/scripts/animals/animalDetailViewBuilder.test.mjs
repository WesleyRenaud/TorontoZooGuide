import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDetailViewBuilder } from '../../../scripts/animals/animalDetailViewBuilder.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildBackButton_TestClick_ExpectCallback', () => {
   const clicks = [];
   const button = AnimalDetailViewBuilder.buildBackButton(() => { clicks.push(true); });
   assert.equal(button.className, 'animal-info-back-button');
   assert.equal(button.textContent, Strings.animalsPage.backWithArrow);
   button.listeners.click();
   assert.deepEqual(clicks, [true]);
});

test('Test_BuildDetailSectionAndHeading_TestEmpty_ExpectNull', () => {
   assert.equal(AnimalDetailViewBuilder.buildDetailSection('Habitat', '  '), null);
   assert.equal(AnimalDetailViewBuilder.buildHeading('h2', 'name', ''), null);

   const section = AnimalDetailViewBuilder.buildDetailSection('Habitat', 'Savanna');
   assert.match(section.textContent, /Habitat:/);
   assert.match(section.textContent, /Savanna/);
});

test('Test_BuildAnimalImage_TestAnimal_ExpectSrcOrNull', () => {
   assert.equal(AnimalDetailViewBuilder.buildAnimalImage({ species: 'Lion' }), null);
   const image = AnimalDetailViewBuilder.buildAnimalImage({
      species: 'African Lion',
      exhibit: 'African Savanna',
   });
   assert.match(image.src, /african-savanna\/african-lion\.png/);
   assert.equal(image.alt, 'African Lion');
});

test('Test_BuildViewOnMapButton_TestClick_ExpectNavigation', () => {
   const hrefs = [];
   const originalLocation = window.location;
   Object.defineProperty(window, 'location', {
      configurable: true,
      value: {
         get href() {
            return 'https://example.test/animals.html';
         },
         set href(value) {
            hrefs.push(value);
         },
      },
   });

   try {
      const button = AnimalDetailViewBuilder.buildViewOnMapButton(
         { species: 'African Lion', exhibit: 'Savanna' },
         'African Savanna'
      );
      button.listeners.click();
      assert.equal(hrefs.length, 1);
      assert.match(hrefs[0], /map\.html/);
      assert.match(hrefs[0], /focus=/);
      assert.match(hrefs[0], /exhibit=/);
   } finally {
      Object.defineProperty(window, 'location', {
         configurable: true,
         value: originalLocation,
      });
   }
});

test('Test_BuildAnimalDetailContent_TestAnimal_ExpectFragmentChildren', () => {
   const fragment = AnimalDetailViewBuilder.buildAnimalDetailContent({
      species: 'African Lion',
      latin_name: 'Panthera leo',
      exhibit: 'African Savanna',
      habitat: 'Grassland',
      habitat_and_range: 'Africa',
      identification: 'Mane',
   }, { exhibitName: 'African Savanna' });

   assert.ok(fragment.children.length >= 4);
   assert.match(fragment.textContent, /Identification:/);
   assert.match(fragment.textContent, /Habitat And Range:/);
});
