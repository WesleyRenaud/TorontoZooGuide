import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesOverlayContent } from '../../../scripts/overlays/speciesOverlayContent.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

function allText(node) {
   return [
      node.textContent,
      ...(node.children ?? []).flatMap(allText),
   ].filter(Boolean).join(' ');
}

function findByClass(root, className) {
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

test.describe('SpeciesOverlayContent.buildSpeciesContent', () => {
   installDomTestHooks();

   test('Test_BuildSpeciesContent_TestPopulatedAnimal_ExpectSections', () => {
      const fragment = SpeciesOverlayContent.buildSpeciesContent({
         species: 'African Lion',
         latin_name: 'Panthera leo',
         exhibit: 'Africa Savanna',
         identification: 'Large cat with a mane',
      });

      const image = findByClass(fragment, 'new-animal-image');
      const speciesHeading = findByClass(fragment, 'animal-species-name');
      const latinHeading = findByClass(fragment, 'latin-name');
      const exhibitHeading = findByClass(fragment, 'animal-exhibit');

      assert.equal(image?.src, 'images/details/animals/africa-savanna/african-lion.png');
      assert.equal(image?.alt, 'African Lion');
      assert.equal(speciesHeading?.textContent, 'African Lion');
      assert.equal(latinHeading?.textContent, 'Panthera leo');
      assert.equal(exhibitHeading?.textContent, 'Africa Savanna');
      assert.match(allText(fragment), /Identification:/i);
      assert.match(allText(fragment), /Large cat with a mane/);
   });

   test('Test_BuildSpeciesContent_TestBlankFields_ExpectOmitted', () => {
      const fragment = SpeciesOverlayContent.buildSpeciesContent({
         species: 'African Penguin',
         latin_name: '   ',
         exhibit: 'Africa Savanna',
         identification: '',
      });

      assert.equal(findByClass(fragment, 'latin-name'), null);
      assert.doesNotMatch(allText(fragment), /Identification:/i);
   });
});
