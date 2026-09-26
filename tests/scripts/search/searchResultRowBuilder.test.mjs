import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchResultRowBuilder } from '../../../scripts/search/searchResultRowBuilder.js';
import { SearchResultPresenter } from '../../../scripts/search/searchResultPresenter.js';
import { AttractionSelectorModel } from '../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { StoredSelectionNormalizer } from '../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { Strings } from '../../../scripts/strings.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetRowTitle_TestPresentation_ExpectCombined', () => {
   const original = SearchResultPresenter.getSearchResultPresentation;
   const title = 'African Lion';
   const suffix = ' (Yard)';
   SearchResultPresenter.getSearchResultPresentation = () => ({
      getTitle: () => title,
      getTitleSuffix: () => suffix,
      getSubtitle: () => 'Savanna',
   });

   try {
      const rowTitle = SearchResultRowBuilder.getRowTitle({});

      assert.equal(rowTitle, `${title}${suffix}`);
   } finally {
      SearchResultPresenter.getSearchResultPresentation = original;
   }
});


test('Test_GetRowSubtitle_TestPresentation_ExpectSubtitle', () => {
   const original = SearchResultPresenter.getSearchResultPresentation;
   const subtitle = 'Savanna';
   SearchResultPresenter.getSearchResultPresentation = () => ({
      getTitle: () => 'African Lion',
      getTitleSuffix: () => '',
      getSubtitle: () => subtitle,
   });

   try {
      const rowSubtitle = SearchResultRowBuilder.getRowSubtitle({});

      assert.equal(rowSubtitle, subtitle);
   } finally {
      SearchResultPresenter.getSearchResultPresentation = original;
   }
});


test('Test_CreateResultText_TestWithSubtitle_ExpectLeftColumn', () => {
   const originalTitle = SearchResultRowBuilder.getRowTitle;
   const originalSubtitle = SearchResultRowBuilder.getRowSubtitle;
   const title = 'Title';
   const subtitle = 'Subtitle';
   SearchResultRowBuilder.getRowTitle = () => title;
   SearchResultRowBuilder.getRowSubtitle = () => subtitle;

   try {
      const left = SearchResultRowBuilder.createResultText({});

      assert.equal(left.className, 'animal-result-left');
      assert.equal(left.children.at(Position.FIRST).textContent, title);
      assert.equal(left.children.at(Position.SECOND).textContent, subtitle);
   } finally {
      SearchResultRowBuilder.getRowTitle = originalTitle;
      SearchResultRowBuilder.getRowSubtitle = originalSubtitle;
   }
});


test('Test_CreateResultContent_TestRenderer_ExpectRendered', () => {
   const originalGet = SearchResultRowBuilder.getRowLeftRenderers;
   const originalText = SearchResultRowBuilder.createResultText;
   const species = 'African Lion';
   SearchResultRowBuilder.getRowLeftRenderers = () => ({
      [ItemType.ANIMAL]: (row) => {
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
      const content = SearchResultRowBuilder.createResultContent({
         type: ItemType.ANIMAL,
         species,
      });

      assert.equal(content.className, 'rendered');
   } finally {
      SearchResultRowBuilder.getRowLeftRenderers = originalGet;
      SearchResultRowBuilder.createResultText = originalText;
   }
});


test('Test_CreateResultContent_TestUnknown_ExpectFallback', () => {
   const originalGet = SearchResultRowBuilder.getRowLeftRenderers;
   const originalText = SearchResultRowBuilder.createResultText;
   SearchResultRowBuilder.getRowLeftRenderers = () => ({});
   SearchResultRowBuilder.createResultText = () => {
      const el = document.createElement('div');
      el.className = 'fallback';
      return el;
   };

   try {
      const content = SearchResultRowBuilder.createResultContent({ type: 'unknown' });

      assert.equal(content.className, 'fallback');
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
   const wildLink = 'https://wild.example';
   const attractionLink = 'https://attraction.example';
   window.open = (...args) => {
      opens.push(args);
   };
   StoredSelectionNormalizer.normalizeStoredLink = () => wildLink;
   AttractionSelectorModel.getAttractionInfoLink = () => attractionLink;

   try {
      SearchResultRowBuilder.openWildEncounterLink({});
      SearchResultRowBuilder.openAttractionInfoLink({});

      assert.deepEqual(opens, [
         [wildLink, '_blank'],
         [attractionLink, '_blank'],
      ]);
   } finally {
      window.open = originalOpen;
      StoredSelectionNormalizer.normalizeStoredLink = originalNormalize;
      AttractionSelectorModel.getAttractionInfoLink = originalAttractionLink;
   }
});


test('Test_CreateSearchResultItem_TestFocusClick_ExpectCallback', () => {
   const originalContent = SearchResultRowBuilder.createResultContent;
   const row = { id: 1 };
   const focused = [];
   SearchResultRowBuilder.createResultContent = () => {
      const el = document.createElement('div');
      el.className = 'content';
      return el;
   };

   try {
      const item = SearchResultRowBuilder.createSearchResultItem(row, (nextRow) => {
         focused.push(nextRow);
      });
      item.children.at(Position.SECOND).listeners.click({ stopPropagation() {} });

      assert.equal(item.className, 'animal-result');
      assert.equal(item.children.at(Position.SECOND).textContent, Strings.common.viewOnMap);
      assert.deepEqual(focused, [row]);
   } finally {
      SearchResultRowBuilder.createResultContent = originalContent;
   }
});


test('Test_CreateSearchResultsFragment_TestRows_ExpectChildren', () => {
   const originalItem = SearchResultRowBuilder.createSearchResultItem;
   const firstId = 'a';
   const rows = [{ id: firstId }, { id: 'b' }];
   SearchResultRowBuilder.createSearchResultItem = (row) => {
      const el = document.createElement('div');
      el.textContent = row.id;
      return el;
   };

   try {
      const fragment = SearchResultRowBuilder.createSearchResultsFragment(rows, () => {});

      assert.equal(fragment.children.length, rows.length);
      assert.equal(fragment.children.at(Position.FIRST).textContent, firstId);
   } finally {
      SearchResultRowBuilder.createSearchResultItem = originalItem;
   }
});
