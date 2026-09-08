import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchResultRowBuilder } from '../../../scripts/search/searchResultRowBuilder.js';
import { SearchResultPresenter } from '../../../scripts/search/searchResultPresenter.js';
import { AttractionSelectorModel } from '../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { StoredSelectionNormalizer } from '../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetRowTitleAndSubtitle_TestPresentation_ExpectCombined', () => {
   const original = SearchResultPresenter.getSearchResultPresentation;
   SearchResultPresenter.getSearchResultPresentation = () => ({
      getTitle: () => 'Lion',
      getTitleSuffix: () => ' (Yard)',
      getSubtitle: () => 'Savanna',
   });
   try {
      assert.equal(SearchResultRowBuilder.getRowTitle({}), 'Lion (Yard)');
      assert.equal(SearchResultRowBuilder.getRowSubtitle({}), 'Savanna');
   } finally {
      SearchResultPresenter.getSearchResultPresentation = original;
   }
});

test('Test_CreateResultText_TestWithSubtitle_ExpectLeftColumn', () => {
   const originalTitle = SearchResultRowBuilder.getRowTitle;
   const originalSubtitle = SearchResultRowBuilder.getRowSubtitle;
   SearchResultRowBuilder.getRowTitle = () => 'Title';
   SearchResultRowBuilder.getRowSubtitle = () => 'Subtitle';
   try {
      const left = SearchResultRowBuilder.createResultText({});
      assert.equal(left.className, 'animal-result-left');
      assert.equal(left.children[0].textContent, 'Title');
      assert.equal(left.children[1].textContent, 'Subtitle');
   } finally {
      SearchResultRowBuilder.getRowTitle = originalTitle;
      SearchResultRowBuilder.getRowSubtitle = originalSubtitle;
   }
});

test('Test_CreateResultContent_TestFallbackAndRenderer_ExpectContent', () => {
   const originalGet = SearchResultRowBuilder.getRowLeftRenderers;
   const originalText = SearchResultRowBuilder.createResultText;
   SearchResultRowBuilder.getRowLeftRenderers = () => ({
      animal: (row) => {
         const el = document.createElement('div');
         el.className = 'rendered';
         el.textContent = row.species;
         return el;
      },
   });
   SearchResultRowBuilder.createResultText = () => {
      const el = document.createElement('div');
      el.className = 'fallback';
      return el;
   };

   try {
      assert.equal(
         SearchResultRowBuilder.createResultContent({ type: 'animal', species: 'Lion' }).className,
         'rendered'
      );
      assert.equal(
         SearchResultRowBuilder.createResultContent({ type: 'unknown' }).className,
         'fallback'
      );
   } finally {
      SearchResultRowBuilder.getRowLeftRenderers = originalGet;
      SearchResultRowBuilder.createResultText = originalText;
   }
});

test('Test_OpenLinks_TestPresence_ExpectWindowOpen', () => {
   const opens = [];
   const originalOpen = window.open;
   const originalNormalize = StoredSelectionNormalizer.normalizeStoredLink;
   const originalAttractionLink = AttractionSelectorModel.getAttractionInfoLink;
   window.open = (...args) => { opens.push(args); };
   StoredSelectionNormalizer.normalizeStoredLink = () => 'https://wild.example';
   AttractionSelectorModel.getAttractionInfoLink = () => 'https://attraction.example';

   try {
      SearchResultRowBuilder.openWildEncounterLink({});
      SearchResultRowBuilder.openAttractionInfoLink({});
      assert.deepEqual(opens, [
         ['https://wild.example', '_blank'],
         ['https://attraction.example', '_blank'],
      ]);
   } finally {
      window.open = originalOpen;
      StoredSelectionNormalizer.normalizeStoredLink = originalNormalize;
      AttractionSelectorModel.getAttractionInfoLink = originalAttractionLink;
   }
});

test('Test_CreateSearchResultItem_TestFocusClick_ExpectCallback', () => {
   const originalContent = SearchResultRowBuilder.createResultContent;
   SearchResultRowBuilder.createResultContent = () => {
      const el = document.createElement('div');
      el.className = 'content';
      return el;
   };
   const focused = [];

   try {
      const item = SearchResultRowBuilder.createSearchResultItem({ id: 1 }, (row) => {
         focused.push(row);
      });
      assert.equal(item.className, 'animal-result');
      assert.equal(item.children[1].textContent, Strings.common.viewOnMap);
      item.children[1].listeners.click({ stopPropagation() {} });
      assert.deepEqual(focused, [{ id: 1 }]);
   } finally {
      SearchResultRowBuilder.createResultContent = originalContent;
   }
});

test('Test_CreateSearchResultsFragment_TestRows_ExpectChildren', () => {
   const originalItem = SearchResultRowBuilder.createSearchResultItem;
   SearchResultRowBuilder.createSearchResultItem = (row) => {
      const el = document.createElement('div');
      el.textContent = row.id;
      return el;
   };
   try {
      const fragment = SearchResultRowBuilder.createSearchResultsFragment(
         [{ id: 'a' }, { id: 'b' }],
         () => {}
      );
      assert.equal(fragment.children.length, 2);
      assert.equal(fragment.children[0].textContent, 'a');
   } finally {
      SearchResultRowBuilder.createSearchResultItem = originalItem;
   }
});
