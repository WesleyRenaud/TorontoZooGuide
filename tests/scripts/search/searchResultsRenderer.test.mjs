import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { SearchResultsRenderer } from '../../../scripts/search/searchResultsRenderer.js';
import { createDomNode, installDocument, installTestWindow, teardownDocument } from '../helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

function _findDescendant(node, className) {
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

test('Test_ResultsView_TestResultsViewRenderSearchResultsShowsThumbnailsForAnimalsAndAttractions_ExpectOk', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
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
   const animalContent = _findDescendant(animalRow, 'itin-animal-content');
   const animalImg = _findDescendant(animalRow, 'itin-animal-thumb-img');

   assert.ok(animalContent);
   assert.equal(
      animalImg.src,
      '../images/details/animals/african-savanna/african-lion.png'
   );

   assert.ok(_findDescendant(animalRow, 'species-link'));

   const attractionRow = resultsEl.children[1];
   const attractionContent = _findDescendant(attractionRow, 'itin-animal-content');
   const attractionImg = _findDescendant(attractionRow, 'itin-animal-thumb-img');

   assert.ok(attractionContent);
   assert.equal(
      attractionImg.src,
      '../images/details/attractions/conservation-carousel.png'
   );

   const attractionTitle = _findDescendant(attractionRow, 'animal-result-species');
   assert.equal(attractionTitle?.querySelector('.species-link'), null);
});

test('Test_ResultsView_TestResultsViewRenderSearchResultsLinksAttractionTitlesWhenInfoLink_ExpectOk', () => {
   installDocument();
   installTestWindow();

   const opened = [];
   globalThis.window.open = (url) => {
      opened.push(url);
   };

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: 'attraction',
         name: 'Conservation Carousel',
         free_with_admission: true,
         info_link: 'https://www.torontozoo.com/tickets/carousel',
      },
   ]);

   const row = resultsEl.children[0];
   const title = _findDescendant(row, 'animal-result-species');
   const titleLink = title?.querySelector('.species-link');

   assert.ok(titleLink);
   assert.equal(titleLink.textContent, 'Conservation Carousel');
   assert.equal(_findDescendant(row, 'tooltip-link'), null);

   titleLink.click();
   assert.deepEqual(opened, ['https://www.torontozoo.com/tickets/carousel']);
});

test('Test_ResultsView_TestResultsViewRenderSearchResultsLinksWildEncounterTitlesWhenUrl_ExpectOk', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: 'wildEncounter',
         name: 'African Rainforest',
         meeting_spot: 'Wild Encounter - Africa Meeting Spot',
         link: 'https://www.torontozoo.com/wildencounters/african-rainforest',
      },
   ]);

   const row = resultsEl.children[0];
   const title = _findDescendant(row, 'animal-result-species');
   const img = _findDescendant(row, 'itin-animal-thumb-img');

   assert.ok(_findDescendant(row, 'species-link'));
   assert.equal(title?.textContent, 'African Rainforest Wild Encounter');
   assert.equal(
      title?.querySelector('.species-link')?.textContent,
      'African Rainforest'
   );
   assert.equal(
      _findDescendant(row, 'animal-result-exhibit')?.textContent,
      'Wild Encounter - Africa Meeting Spot'
   );
   assert.equal(
      img?.src,
      '../images/details/wild-encounters/african-rainforest.png'
   );
   assert.equal(_findDescendant(row, 'tooltip-link'), null);
});

test('Test_ResultsView_TestResultsViewRenderSearchResultsFormatsWildEncounterSubtitlesLikeSchedule_ExpectOk', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: 'wildEncounter',
         name: 'From Howls to Honks',
         meeting_spot: 'Wild Encounter – Mayan Temple Meeting Spot',
         start_time: '13:00',
         end_time: '13:30',
      },
   ]);

   const subtitle = _findDescendant(
      resultsEl.children[0],
      'animal-result-exhibit'
   );

   assert.equal(
      subtitle?.textContent,
      'Wild Encounter – Mayan Temple Meeting Spot  •  1:00 PM - 1:30 PM'
   );
});

test('Test_ResultsView_TestResultsViewRenderSearchResultsKeepsTextOnlyRowsForRestrooms_ExpectOk', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      { type: 'restroom', title: 'Americas Pavilion Restroom' },
   ]);

   const row = resultsEl.children[0];

   assert.equal(_findDescendant(row, 'itin-animal-content'), null);
   assert.ok(_findDescendant(row, 'animal-result-left'));
   assert.ok(_findDescendant(row, 'animal-result-map-btn'));
});

test('Test_ResultsView_TestResultsViewRenderSearchResultsShowsThumbnailsForNamedMapDetail_ExpectOk', () => {
   installDocument();

   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      { type: 'restaurant', name: 'Beavertails Pastry', location: 'Front Courtyard' },
      { type: 'giftShop', name: 'Zootique', location: 'Africa' },
      { type: 'guardiansTalk', name: 'Amur Tiger', location: 'Eurasia Wilds' },
      { type: 'pavilion', name: 'Americas Pavilion', region: 'Americas' },
      { type: 'transportationStation', name: 'Zoomobile Station 1' },
   ]);

   assert.equal(resultsEl.children.length, 5);

   const expectedImageSrcs = [
      '../images/details/restaurants/beavertails-pastry.png',
      '../images/details/gift-shops/zootique.png',
      '../images/details/guardians-talks/amur-tiger.png',
      '../images/details/pavilions/americas-pavilion.png',
      '../images/details/transportation-stations/zoomobile-station-1.png',
   ];

   resultsEl.children.forEach((row, index) => {
      assert.ok(_findDescendant(row, 'itin-animal-content'));
      assert.equal(
         _findDescendant(row, 'itin-animal-thumb-img')?.src,
         expectedImageSrcs[index]
      );
   });

   const guardiansTalkTitle = _findDescendant(
      resultsEl.children[2],
      'animal-result-species'
   );

   assert.equal(
      guardiansTalkTitle?.textContent,
      'Amur Tiger Meet The Guardians Talk'
   );
   assert.equal(
      guardiansTalkTitle?.querySelector('.species-link'),
      null
   );
   assert.equal(
      _findDescendant(resultsEl.children[2], 'animal-result-exhibit')?.textContent,
      'Eurasia Wilds'
   );
});
