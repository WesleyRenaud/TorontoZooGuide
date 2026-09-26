import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalDetailViewBuilder } from '../../../scripts/animals/animalDetailViewBuilder.js';
import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BuildBackButton_TestClick_ExpectCallback', () => {
   const clicks = [];

   const button = AnimalDetailViewBuilder.buildBackButton(() => { clicks.push(true); });
   button.listeners.click();

   assert.equal(button.className, 'animal-info-back-button');
   assert.equal(button.textContent, Strings.animalsPage.backWithArrow);
   assert.deepEqual(clicks, [true]);
});


test('Test_BuildDetailSection_TestBlank_ExpectNull', () => {
   const title = 'Habitat';
   const value = '  ';

   const section = AnimalDetailViewBuilder.buildDetailSection(title, value);

   assert.equal(section, null);
});


test('Test_BuildHeading_TestEmpty_ExpectNull', () => {
   const tagName = 'h2';
   const className = 'name';
   const text = '';

   const heading = AnimalDetailViewBuilder.buildHeading(tagName, className, text);

   assert.equal(heading, null);
});


test('Test_BuildDetailSection_TestValue_ExpectSection', () => {
   const title = 'Habitat';
   const value = 'Savanna';

   const section = AnimalDetailViewBuilder.buildDetailSection(title, value);

   assert.match(section.textContent, new RegExp(`${title}:`));
   assert.match(section.textContent, new RegExp(value));
});


test('Test_BuildAnimalImage_TestMissingExhibit_ExpectNull', () => {
   const animal = { species: 'Lion' };

   const image = AnimalDetailViewBuilder.buildAnimalImage(animal);

   assert.equal(image, null);
});


test('Test_BuildAnimalImage_TestAnimal_ExpectSrc', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';

   const image = AnimalDetailViewBuilder.buildAnimalImage({
      species,
      exhibit,
   });

   assert.match(
      image.src,
      new RegExp(`${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(species)}\\.png`)
   );
   assert.equal(image.alt, species);
});


test('Test_BuildViewOnMapButton_TestClick_ExpectNavigation', () => {
   const hrefs = [];
   const species = 'African Lion';
   const exhibit = 'African Savanna';
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
         { species, exhibit: 'Savanna' },
         exhibit
      );
      button.listeners.click();
      const href = hrefs.at(Position.FIRST);

      const query = new URL(href).searchParams;

      assert.equal(hrefs.length, Position.SECOND);
      assert.match(href, /map\.html/);
      assert.equal(query.get('focus'), species);
      assert.equal(query.get('exhibit'), exhibit);
   } finally {
      Object.defineProperty(window, 'location', {
         configurable: true,
         value: originalLocation,
      });
   }
});


test('Test_BuildAnimalDetailContent_TestAnimal_ExpectFragmentChildren', () => {
   const exhibit = 'African Savanna';

   const fragment = AnimalDetailViewBuilder.buildAnimalDetailContent({
      species: 'African Lion',
      latin_name: 'Panthera leo',
      exhibit,
      habitat: 'Grassland',
      habitat_and_range: 'Africa',
      identification: 'Mane',
   }, { exhibitName: exhibit });

   const minChildren = 4;

   assert.ok(fragment.children.length >= minChildren);
   assert.match(fragment.textContent, new RegExp(Strings.format.labelWithColon('Identification')));
   assert.match(fragment.textContent, /Habitat And Range:/);
});
