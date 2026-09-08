import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesOverlayContent } from '../../../scripts/overlays/speciesOverlayContent.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

function _allText(node) {
   return [
      node.textContent,
      ...(node.children ?? []).flatMap(_allText),
   ].filter(Boolean).join(' ');
}

function _findByClass(root, className) {
   const stack = [root];

   while (stack.length > 0) {
      const node = stack.shift();

      if (node.className?.split(/\s+/).includes(className)) {
         return node;
      }

      stack.push(...(node.children ?? []));
   }

   return null;
}

installDomTestHooks();

test('Test_BuildSpeciesContent_TestPopulatedAnimal_ExpectSections', () => {
   const fragment = SpeciesOverlayContent.buildSpeciesContent({
      species: 'African Lion',
      latin_name: 'Panthera leo',
      exhibit: 'Africa Savanna',
      identification: 'Large cat with a mane',
   });

   const image = _findByClass(fragment, 'new-animal-image');
   const speciesHeading = _findByClass(fragment, 'animal-species-name');
   const latinHeading = _findByClass(fragment, 'latin-name');
   const exhibitHeading = _findByClass(fragment, 'animal-exhibit');

   assert.equal(image?.src, 'images/details/animals/africa-savanna/african-lion.png');
   assert.equal(image?.alt, 'African Lion');
   assert.equal(speciesHeading?.textContent, 'African Lion');
   assert.equal(latinHeading?.textContent, 'Panthera leo');
   assert.equal(exhibitHeading?.textContent, 'Africa Savanna');
   assert.match(_allText(fragment), /Identification:/i);
   assert.match(_allText(fragment), /Large cat with a mane/);
});

test('Test_BuildSpeciesContent_TestBlankFields_ExpectOmitted', () => {
   const fragment = SpeciesOverlayContent.buildSpeciesContent({
      species: 'African Penguin',
      latin_name: '   ',
      exhibit: 'Africa Savanna',
      identification: '',
   });

   assert.equal(_findByClass(fragment, 'latin-name'), null);
   assert.doesNotMatch(_allText(fragment), /Identification:/i);
});
