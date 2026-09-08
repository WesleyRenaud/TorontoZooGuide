import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesOverlayContentBuilder } from '../../../scripts/overlays/speciesOverlayContentBuilder.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTextElement_TestContent_ExpectNode', () => {
   const el = SpeciesOverlayContentBuilder.createTextElement('p', 'detail', 'African Lion');
   assert.equal(el.tagName, 'p');
   assert.equal(el.className, 'detail');
   assert.equal(el.textContent, 'African Lion');
});

test('Test_CreateSpeciesImage_TestAnimal_ExpectSrcAndAlt', () => {
   const image = SpeciesOverlayContentBuilder.createSpeciesImage({
      species: 'African Lion',
      exhibit: 'African Savanna',
   });

   assert.equal(image.className, 'new-animal-image');
   assert.equal(image.alt, 'African Lion');
   assert.match(image.src, /images\/details\/animals\/african-savanna\/african-lion\.png/);
});

test('Test_CreateDetailSection_TestEmpty_ExpectNull', () => {
   assert.equal(SpeciesOverlayContentBuilder.createDetailSection('Habitat', '  '), null);
});

test('Test_CreateDetailSection_TestValue_ExpectSection', () => {
   const section = SpeciesOverlayContentBuilder.createDetailSection('Habitat', 'Savanna');
   assert.equal(section.className, 'section');
   assert.match(section.textContent, /Habitat:/);
   assert.match(section.textContent, /Savanna/);
});

test('Test_AppendIfPresent_TestChild_ExpectAppendedOrSkipped', () => {
   const parent = document.createElement('div');
   SpeciesOverlayContentBuilder.appendIfPresent(parent, null);
   assert.equal(parent.children.length, 0);

   const child = document.createElement('span');
   SpeciesOverlayContentBuilder.appendIfPresent(parent, child);
   assert.equal(parent.children.length, 1);
});
