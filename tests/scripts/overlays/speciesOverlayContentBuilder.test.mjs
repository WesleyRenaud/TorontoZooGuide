import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { SpeciesOverlayContentBuilder } from '../../../scripts/overlays/speciesOverlayContentBuilder.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateTextElement_TestContent_ExpectNode', () => {
   const tagName = 'p';
   const className = 'detail';
   const text = 'African Lion';

   const el = SpeciesOverlayContentBuilder.createTextElement(tagName, className, text);

   assert.equal(el.tagName, tagName);
   assert.equal(el.className, className);
   assert.equal(el.textContent, text);
});


test('Test_CreateSpeciesImage_TestAnimal_ExpectSrcAndAlt', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';

   const image = SpeciesOverlayContentBuilder.createSpeciesImage({
      species,
      exhibit,
   });

   assert.equal(image.className, 'new-animal-image');
   assert.equal(image.alt, species);
   assert.match(
      image.src,
      new RegExp(DetailImageBuilder.buildDetailImageSrcFromParts(['animals', exhibit, species]))
   );
});


test('Test_CreateDetailSection_TestEmpty_ExpectNull', () => {
   const title = 'Habitat';
   const value = '  ';

   const section = SpeciesOverlayContentBuilder.createDetailSection(title, value);

   assert.equal(section, null);
});


test('Test_CreateDetailSection_TestValue_ExpectSection', () => {
   const title = 'Habitat';
   const value = 'Savanna';

   const section = SpeciesOverlayContentBuilder.createDetailSection(title, value);

   assert.equal(section.className, 'section');
   assert.match(section.textContent, new RegExp(`${title}:`));
   assert.match(section.textContent, new RegExp(value));
});


test('Test_AppendIfPresent_TestNull_ExpectSkipped', () => {
   const parent = document.createElement('div');

   SpeciesOverlayContentBuilder.appendIfPresent(parent, null);

   assert.equal(parent.children.length, 0);
});


test('Test_AppendIfPresent_TestChild_ExpectAppended', () => {
   const parent = document.createElement('div');
   const child = document.createElement('span');

   SpeciesOverlayContentBuilder.appendIfPresent(parent, child);

   assert.equal(parent.children.length, Position.SECOND);
});
