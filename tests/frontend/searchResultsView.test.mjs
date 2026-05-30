import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { renderSearchResults } from '../../scripts/search/resultsView.js';
import {
   createDomNode,
   installDocument,
   teardownDocument,
} from './helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

function findDescendant(node, className) {
   const stack = [node];

   while (stack.length > 0) {
      const current = stack.pop();

      if (current.className?.split(/\s+/).includes(className)) {
         return current;
      }

      stack.push(...current.children);
   }

   return null;
}

test('renderSearchResults shows thumbnails for animals and attractions', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   renderSearchResults(resultsEl, [
      {
         type: 'animal',
         species: 'African Lion',
         exhibit: 'African Savanna',
      },
      {
         type: 'attraction',
         name: 'Conservation Carousel',
         free_with_admission: true,
      },
   ]);

   assert.equal(resultsEl.children.length, 2);

   const animalRow = resultsEl.children[0];
   const animalContent = findDescendant(animalRow, 'itin-animal-content');
   const animalImg = findDescendant(animalRow, 'itin-animal-thumb-img');

   assert.ok(animalContent);
   assert.equal(
      animalImg.src,
      '../images/details/animals/african-savanna/african-lion.png'
   );

   const attractionRow = resultsEl.children[1];
   const attractionContent = findDescendant(attractionRow, 'itin-animal-content');
   const attractionImg = findDescendant(attractionRow, 'itin-animal-thumb-img');

   assert.ok(attractionContent);
   assert.equal(
      attractionImg.src,
      '../images/details/attractions/conservation-carousel.png'
   );
});

test('renderSearchResults keeps text-only rows for other result types', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   renderSearchResults(resultsEl, [
      { type: 'giftShop', name: 'Zootique', location: 'Africa' },
   ]);

   const row = resultsEl.children[0];

   assert.equal(findDescendant(row, 'itin-animal-content'), null);
   assert.ok(findDescendant(row, 'animal-result-left'));
   assert.ok(findDescendant(row, 'animal-result-map-btn'));
});
