import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { SearchResultsRenderer } from '../../../scripts/search/searchResultsRenderer.js';
import { SearchResultPresenter } from '../../../scripts/search/searchResultPresenter.js';
import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const attraction = 'Conservation Carousel';
   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: ItemType.ANIMAL,
         species,
         exhibit,
      },
      {
         type: ItemType.ATTRACTION,
         name: attraction,
         free_with_admission: true,
      },
   ]);
   const animalRow = resultsEl.children.at(Position.FIRST);
   const attractionRow = resultsEl.children.at(Position.SECOND);

   assert.equal(resultsEl.children.length, 2);
   assert.ok(_findDescendant(animalRow, 'itin-animal-content'));
   assert.equal(
      _findDescendant(animalRow, 'itin-animal-thumb-img').src,
      `${SearchResultPresenter.SEARCH_DETAIL_IMAGE_BASE_PATH}/animals/${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(species)}.png`
   );
   assert.ok(_findDescendant(animalRow, 'species-link'));
   assert.ok(_findDescendant(attractionRow, 'itin-animal-content'));
   assert.equal(
      _findDescendant(attractionRow, 'itin-animal-thumb-img').src,
      SearchResultPresenter.buildSearchDetailImageSrc('attractions', attraction)
   );
   assert.equal(
      _findDescendant(attractionRow, 'animal-result-species')?.querySelector('.species-link'),
      null
   );
});


test('Test_ResultsView_TestResultsViewRenderSearchResultsLinksAttractionTitlesWhenInfoLink_ExpectOk', () => {
   installDocument();
   installTestWindow();
   const opened = [];
   const name = 'Conservation Carousel';
   const infoLink = 'https://www.torontozoo.com/tickets/carousel';
   globalThis.window.open = (url) => {
      opened.push(url);
   };
   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: ItemType.ATTRACTION,
         name,
         free_with_admission: true,
         info_link: infoLink,
      },
   ]);
   const titleLink = _findDescendant(resultsEl.children.at(Position.FIRST), 'animal-result-species')
      ?.querySelector('.species-link');
   titleLink.click();

   assert.ok(titleLink);
   assert.equal(titleLink.textContent, name);
   assert.equal(_findDescendant(resultsEl.children.at(Position.FIRST), 'tooltip-link'), null);
   assert.deepEqual(opened, [infoLink]);
});


test('Test_ResultsView_TestResultsViewRenderSearchResultsLinksWildEncounterTitlesWhenUrl_ExpectOk', () => {
   installDocument();
   const name = 'African Rainforest';
   const meetingSpot = 'Wild Encounter - Africa Meeting Spot';
   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: ItemType.WILD_ENCOUNTER,
         name,
         meeting_spot: meetingSpot,
         link: 'https://www.torontozoo.com/wildencounters/african-rainforest',
      },
   ]);
   const row = resultsEl.children.at(Position.FIRST);
   const title = _findDescendant(row, 'animal-result-species');

   assert.ok(_findDescendant(row, 'species-link'));
   assert.equal(title?.textContent, `${name} ${Strings.entityLabels.wildEncounter}`);
   assert.equal(title?.querySelector('.species-link')?.textContent, name);
   assert.equal(_findDescendant(row, 'animal-result-exhibit')?.textContent, meetingSpot);
   assert.equal(
      _findDescendant(row, 'itin-animal-thumb-img')?.src,
      SearchResultPresenter.buildSearchDetailImageSrc('wild-encounters', name)
   );
   assert.equal(_findDescendant(row, 'tooltip-link'), null);
});


test('Test_ResultsView_TestResultsViewRenderSearchResultsFormatsWildEncounterSubtitlesLikeSchedule_ExpectOk', () => {
   installDocument();
   const meetingSpot = 'Wild Encounter – Mayan Temple Meeting Spot';
   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      {
         type: ItemType.WILD_ENCOUNTER,
         name: 'From Howls to Honks',
         meeting_spot: meetingSpot,
         start_time: '13:00',
         end_time: '13:30',
      },
   ]);
   const subtitle = _findDescendant(
      resultsEl.children.at(Position.FIRST),
      'animal-result-exhibit'
   );

   assert.equal(subtitle?.textContent, `${meetingSpot}  •  1:00 PM - 1:30 PM`);
});


test('Test_ResultsView_TestResultsViewRenderSearchResultsKeepsTextOnlyRowsForRestrooms_ExpectOk', () => {
   installDocument();
   const resultsEl = createDomNode('div', 'animal-search-results');

   SearchResultsRenderer.renderSearchResults(resultsEl, [
      { type: ItemType.RESTROOM, title: 'Americas Pavilion Restroom' },
   ]);
   const row = resultsEl.children.at(Position.FIRST);

   assert.equal(_findDescendant(row, 'itin-animal-content'), null);
   assert.ok(_findDescendant(row, 'animal-result-left'));
   assert.ok(_findDescendant(row, 'animal-result-map-btn'));
});


test('Test_ResultsView_TestResultsViewRenderSearchResultsShowsThumbnailsForNamedMapDetail_ExpectOk', () => {
   installDocument();
   const pastry = 'Beavertails Pastry';
   const zootique = 'Zootique';
   const talkName = 'Amur Tiger';
   const pavilion = 'Americas Pavilion';
   const station = 'Zoomobile Station 1';
   const location = 'Eurasia Wilds';
   const resultsEl = createDomNode('div', 'animal-search-results');
   const rows = [
      { type: ItemType.RESTAURANT, name: pastry, location: 'Front Courtyard' },
      { type: ItemType.GIFT_SHOP, name: zootique, location: 'Africa' },
      { type: ItemType.GUARDIANS_TALK, name: talkName, location },
      { type: ItemType.PAVILION, name: pavilion, region: 'Americas' },
      { type: ItemType.TRANSPORTATION_STATION, name: station },
   ];
   const expectedImageSrcs = [
      SearchResultPresenter.buildSearchDetailImageSrc('restaurants', pastry),
      SearchResultPresenter.buildSearchDetailImageSrc('gift-shops', zootique),
      SearchResultPresenter.buildSearchDetailImageSrc('guardians-talks', talkName),
      SearchResultPresenter.buildSearchDetailImageSrc('pavilions', pavilion),
      SearchResultPresenter.buildSearchDetailImageSrc('transportation-stations', station),
   ];

   SearchResultsRenderer.renderSearchResults(resultsEl, rows);
   const talkTitle = _findDescendant(
      resultsEl.children.at(Position.THIRD),
      'animal-result-species'
   );

   assert.equal(resultsEl.children.length, rows.length);
   resultsEl.children.forEach((row, index) => {
      assert.ok(_findDescendant(row, 'itin-animal-content'));
      assert.equal(_findDescendant(row, 'itin-animal-thumb-img')?.src, expectedImageSrcs[index]);
   });
   assert.equal(talkTitle?.textContent, Strings.map.hover.guardiansTalkWithName(talkName));
   assert.equal(talkTitle?.querySelector('.species-link'), null);
   assert.equal(
      _findDescendant(resultsEl.children.at(Position.THIRD), 'animal-result-exhibit')?.textContent,
      location
   );
});


test('Test_RenderSearchResults_TestEmpty_ExpectCleared', () => {
   installDocument();
   const resultsEl = createDomNode('div', 'animal-search-results');
   resultsEl.appendChild(createDomNode('div', 'stale'));

   SearchResultsRenderer.renderSearchResults(resultsEl, []);

   assert.equal(resultsEl.children.length, Position.FIRST);
});


test('Test_RenderSearchResults_TestInvalid_ExpectCleared', () => {
   installDocument();
   const resultsEl = createDomNode('div', 'animal-search-results');
   resultsEl.appendChild(createDomNode('div', 'stale'));

   SearchResultsRenderer.renderSearchResults(resultsEl, null);

   assert.equal(resultsEl.children.length, Position.FIRST);
});
