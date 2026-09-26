import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { SpeciesOverlayView } from '../../../scripts/overlays/speciesOverlayView.js';
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
   const species = 'African Lion';
   const latinName = 'Panthera leo';
   const exhibit = 'Africa Savanna';
   const identification = 'Large cat with a mane';

   const fragment = SpeciesOverlayView.buildSpeciesContent({
      species,
      latin_name: latinName,
      exhibit,
      identification,
   });
   const image = _findByClass(fragment, 'new-animal-image');
   const speciesHeading = _findByClass(fragment, 'animal-species-name');
   const latinHeading = _findByClass(fragment, 'latin-name');
   const exhibitHeading = _findByClass(fragment, 'animal-exhibit');

   assert.equal(
      image?.src,
      DetailImageBuilder.buildDetailImageSrcFromParts(['animals', exhibit, species])
   );
   assert.equal(image?.alt, species);
   assert.equal(speciesHeading?.textContent, species);
   assert.equal(latinHeading?.textContent, latinName);
   assert.equal(exhibitHeading?.textContent, exhibit);
   assert.match(_allText(fragment), /Identification:/i);
   assert.match(_allText(fragment), new RegExp(identification));
});


test('Test_BuildSpeciesContent_TestBlankFields_ExpectOmitted', () => {
   const species = 'African Penguin';
   const exhibit = 'Africa Savanna';

   const fragment = SpeciesOverlayView.buildSpeciesContent({
      species,
      latin_name: '   ',
      exhibit,
      identification: '',
   });

   assert.equal(_findByClass(fragment, 'latin-name'), null);
   assert.doesNotMatch(_allText(fragment), /Identification:/i);
});
