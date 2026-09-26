import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { ResultRenderer } from '../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { StoredSelectionNormalizer } from '../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { SearchResultPresenter } from '../../../scripts/search/searchResultPresenter.js';
import { Strings } from '../../../scripts/strings.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BuildSearchDetailImageSrc_TestDirectory_ExpectDetailBuilder', () => {
   const original = DetailImageBuilder.buildDetailImageSrc;
   const directory = 'animals';
   const name = 'African Lion';
   DetailImageBuilder.buildDetailImageSrc = (imageDirectory, imageName, options) => ({
      directory: imageDirectory,
      name: imageName,
      options,
   });

   try {
      const src = SearchResultPresenter.buildSearchDetailImageSrc(directory, name);

      assert.deepEqual(src, {
         directory,
         name,
         options: { basePath: SearchResultPresenter.SEARCH_DETAIL_IMAGE_BASE_PATH },
      });
   } finally {
      DetailImageBuilder.buildDetailImageSrc = original;
   }
});


test('Test_BuildDetailSummary_TestEmpty_ExpectFallback', () => {
   const fallback = 'fallback';

   const summary = SearchResultPresenter.buildDetailSummary([], fallback);

   assert.equal(summary, fallback);
});


test('Test_BuildDetailSummary_TestParts_ExpectJoined', () => {
   const fallback = 'fallback';
   const first = 'A';
   const second = 'B';

   const summary = SearchResultPresenter.buildDetailSummary([first, null, second], fallback);

   assert.equal(summary, `${fallback}\n${first} | ${second}`);
});


test('Test_BuildLocationSummary_TestLocationFields_ExpectJoined', () => {
   const location = 'Africa';
   const subLocation = 'Savanna';
   const fallback = 'fallback';

   const summary = SearchResultPresenter.buildLocationSummary(
      { location, sub_location: subLocation },
      fallback
   );

   assert.equal(summary, `${Strings.search.location(location)}, ${subLocation}`);
});


test('Test_BuildLocationSummary_TestMissing_ExpectFallback', () => {
   const fallback = 'fallback';

   const summary = SearchResultPresenter.buildLocationSummary({}, fallback);

   assert.equal(summary, fallback);
});


test('Test_GetSearchResultPresentation_TestRestroom_ExpectLabel', () => {
   const presentation = SearchResultPresenter.getSearchResultPresentation({ type: ItemType.RESTROOM });

   assert.equal(presentation.getTitle({}), Strings.entityLabels.restroom);
});


test('Test_GetSearchResultPresentation_TestUnknown_ExpectDefault', () => {
   const presentation = SearchResultPresenter.getSearchResultPresentation({ type: 'unknown' });

   assert.equal(presentation, SearchResultPresenter.DEFAULT_SEARCH_RESULT_PRESENTATION);
});


test('Test_GetSearchResultPresentation_TestAttractionTitle_ExpectName', () => {
   const name = 'Conservation Carousel';

   const title = SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.attraction.getTitle({ name });

   assert.equal(title, name);
});


test('Test_GetSearchResultPresentation_TestPavilionSubtitle_ExpectRegion', () => {
   const region = 'Indo-Malaya';

   const subtitle = SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.pavilion.getSubtitle({ region });

   assert.equal(subtitle, Strings.search.region(region));
});


test('Test_CreateSearchImageRowRenderer_TestPresentation_ExpectRendererConfig', () => {
   const original = ResultRenderer.createDefaultSelectorRowLeftRenderer;
   let captured;

   ResultRenderer.createDefaultSelectorRowLeftRenderer = (config) => {
      captured = config;
      return config;
   };

   try {
      const imageDirectory = 'wild-encounters';
      const name = 'African Rainforest';
      const renderer = SearchResultPresenter.createSearchImageRowRenderer({
         presentation: SearchResultPresenter.SEARCH_RESULT_PRESENTATIONS.wildEncounter,
         imageDirectory,
      });
      const imageSrc = captured.getImageSrc({ name });

      assert.equal(renderer.getTitle, captured.getTitle);
      assert.equal(
         imageSrc,
         SearchResultPresenter.buildSearchDetailImageSrc(imageDirectory, name)
      );
   } finally {
      ResultRenderer.createDefaultSelectorRowLeftRenderer = original;
   }
});


test('Test_CreateSearchImageRowRenderers_TestConfigs_ExpectMap', () => {
   const original = SearchResultPresenter.createSearchImageRowRenderer;
   const attractionsDirectory = 'attractions';
   const giftShopsDirectory = 'gift-shops';
   SearchResultPresenter.createSearchImageRowRenderer = ({ presentation, imageDirectory }) => ({
      presentation,
      imageDirectory,
   });

   try {
      const renderers = SearchResultPresenter.createSearchImageRowRenderers([
         { type: ItemType.ATTRACTION, imageDirectory: attractionsDirectory },
         { type: ItemType.GIFT_SHOP, imageDirectory: giftShopsDirectory },
      ]);

      assert.equal(renderers[ItemType.ATTRACTION].imageDirectory, attractionsDirectory);
      assert.equal(renderers[ItemType.GIFT_SHOP].imageDirectory, giftShopsDirectory);
   } finally {
      SearchResultPresenter.createSearchImageRowRenderer = original;
   }
});


test('Test_GetRestaurantMenuLink_TestRow_ExpectNormalized', () => {
   const original = StoredSelectionNormalizer.normalizeStoredLink;
   const menuLink = 'menu.pdf';
   StoredSelectionNormalizer.normalizeStoredLink = (link) => `normalized:${link}`;

   try {
      const link = SearchResultPresenter.getRestaurantMenuLink({ menu_link: menuLink });

      assert.equal(link, `normalized:${menuLink}`);
   } finally {
      StoredSelectionNormalizer.normalizeStoredLink = original;
   }
});
