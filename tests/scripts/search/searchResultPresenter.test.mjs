import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { ResultRenderer } from '../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { StoredSelectionNormalizer } from '../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { SearchResultPresenter } from '../../../scripts/search/searchResultPresenter.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildSearchDetailImageSrc_TestDirectory_ExpectDetailBuilder', () => {
   const original = DetailImageBuilder.buildDetailImageSrc;
   DetailImageBuilder.buildDetailImageSrc = (directory, name, options) => ({
      directory,
      name,
      options,
   });

   try {
      assert.deepEqual(
         SearchResultPresenter.buildSearchDetailImageSrc('animals', 'Lion'),
         {
            directory: 'animals',
            name: 'Lion',
            options: { basePath: SearchResultPresenter.SEARCH_DETAIL_IMAGE_BASE_PATH },
         }
      );
   } finally {
      DetailImageBuilder.buildDetailImageSrc = original;
   }
});

test('Test_BuildDetailSummary_TestParts_ExpectJoinedOrFallback', () => {
   assert.equal(SearchResultPresenter.buildDetailSummary([], 'fallback'), 'fallback');
   assert.equal(
      SearchResultPresenter.buildDetailSummary(['A', null, 'B'], 'fallback'),
      'fallback\nA | B'
   );
});

test('Test_BuildLocationSummary_TestLocationFields_ExpectJoined', () => {
   assert.equal(
      SearchResultPresenter.buildLocationSummary(
         { location: 'Africa', sub_location: 'Savanna' },
         'fallback'
      ),
      `${Strings.search.location('Africa')}, Savanna`
   );
   assert.equal(
      SearchResultPresenter.buildLocationSummary({}, 'fallback'),
      'fallback'
   );
});

test('Test_GetSearchResultPresentation_TestTypes_ExpectPresentation', () => {
   assert.equal(
      SearchResultPresenter.getSearchResultPresentation({ type: 'restroom' }).getTitle({}),
      Strings.entityLabels.restroom
   );
   assert.equal(
      SearchResultPresenter.getSearchResultPresentation({ type: 'unknown' }),
      SearchResultPresenter.DEFAULT_SEARCH_RESULT_PRESENTATION
   );
   assert.equal(
      SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.attraction.getTitle({ name: 'Carousel' }),
      'Carousel'
   );
   assert.equal(
      SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.pavilion.getSubtitle({ region: 'Indo-Malaya' }),
      Strings.search.region('Indo-Malaya')
   );
});

test('Test_CreateSearchImageRowRenderer_TestPresentation_ExpectRendererConfig', () => {
   const original = ResultRenderer.createDefaultSelectorRowLeftRenderer;
   let captured;

   ResultRenderer.createDefaultSelectorRowLeftRenderer = (config) => {
      captured = config;
      return config;
   };

   try {
      const renderer = SearchResultPresenter.createSearchImageRowRenderer({
         presentation: SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.wildEncounter,
         imageDirectory: 'wild-encounters',
      });

      assert.equal(renderer.getTitle, captured.getTitle);
      assert.match(captured.getImageSrc({ name: 'Encounter' }), /wild-encounters|Encounter/);
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = original;
   }
});

test('Test_CreateSearchImageRowRenderers_TestConfigs_ExpectMap', () => {
   const original = SearchResultPresenter.createSearchImageRowRenderer;
   SearchResultPresenter.createSearchImageRowRenderer = ({ presentation, imageDirectory }) => ({
      presentation,
      imageDirectory,
   });

   try {
      const renderers = SearchResultPresenter.createSearchImageRowRenderers([
         { type: 'attraction', imageDirectory: 'attractions' },
         { type: 'giftShop', imageDirectory: 'gift-shops' },
      ]);

      assert.equal(renderers.attraction.imageDirectory, 'attractions');
      assert.equal(renderers.giftShop.imageDirectory, 'gift-shops');
   } finally {
      SearchResultPresenter.createSearchImageRowRenderer = original;
   }
});

test('Test_GetRestaurantMenuLink_TestRow_ExpectNormalized', () => {
   const original = StoredSelectionNormalizer.normalizeStoredLink;
   StoredSelectionNormalizer.normalizeStoredLink = (link) => `normalized:${link}`;

   try {
      assert.equal(
         SearchResultPresenter.getRestaurantMenuLink({ menu_link: 'menu.pdf' }),
         'normalized:menu.pdf'
      );
   } finally {
      StoredSelectionNormalizer.normalizeStoredLink = original;
   }
});
