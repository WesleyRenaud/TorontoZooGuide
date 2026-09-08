import assert from 'node:assert/strict';
import test from 'node:test';

import { ResultRenderer } from '../../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { SelectorResultRowBuilder } from '../../../../../scripts/itinerary/selectors/base/selectorResultRowBuilder.js';
import { SpeciesLinkTitleBuilder } from '../../../../../scripts/animals/speciesLinkTitleBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateSelectorThumb_TestPlaceholderAndError_ExpectFallback', () => {
   const placeholder = ResultRenderer.createSelectorThumb();
   assert.equal(placeholder.className, 'itin-animal-thumb is-placeholder');

   const thumb = ResultRenderer.createSelectorThumb({
      imageSrc: '../images/details/animals/lion.png',
      imageAlt: 'African Lion',
   });
   const img = thumb.querySelector('.itin-animal-thumb-img');
   assert.equal(img.src, '../images/details/animals/lion.png');
   img.listeners.error?.();
   assert.equal(thumb.classList.contains('is-placeholder'), true);
});

test('Test_CreateSelectorTextColumn_TestSubtitleInfoAndParts_ExpectNodes', () => {
   const withSubtitle = ResultRenderer.createSelectorTextColumn({
      title: 'Carousel',
      subtitle: 'Free',
      infoLink: 'https://example.com',
   });
   assert.equal(withSubtitle.querySelector('.animal-result-species')?.textContent, 'Carousel');
   assert.equal(withSubtitle.querySelector('.animal-result-exhibit')?.textContent, 'Free');
   assert.equal(withSubtitle.querySelector('.tooltip-link')?.textContent, Strings.common.moreInfo);

   const titleNode = document.createElement('div');
   titleNode.className = 'custom-title';
   titleNode.textContent = 'Custom';
   const subtitleNode = document.createElement('div');
   subtitleNode.className = 'custom-subtitle';
   const withNodes = ResultRenderer.createSelectorTextColumn({
      titleNode,
      subtitleNode,
   });
   assert.ok(withNodes.querySelector('.custom-title'));
   assert.ok(withNodes.querySelector('.custom-subtitle'));

   const originalParts = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement;
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = ({ species }) => {
      const el = document.createElement('div');
      el.className = 'animal-result-species';
      el.textContent = species;
      return el;
   };

   try {
      const withParts = ResultRenderer.createSelectorTextColumn({
         titleParts: { species: 'Lion', enclosureName: 'Yard' },
         onTitleClick: () => {},
      });
      assert.equal(withParts.querySelector('.animal-result-species')?.textContent, 'Lion');
   } finally {
      SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = originalParts;
   }
});

test('Test_CreateSelectorRowContent_TestThumbAndText_ExpectContent', () => {
   const textColumnEl = document.createElement('div');
   textColumnEl.className = 'text-col';
   const content = ResultRenderer.createSelectorRowContent({
      imageSrc: null,
      imageAlt: '',
      textColumnEl,
   });
   assert.equal(content.className, 'itin-animal-content');
   assert.ok(content.querySelector('.itin-animal-thumb'));
   assert.ok(content.querySelector('.text-col'));
});

test('Test_CreateDefaultSelectorRowLeftRenderer_TestRow_ExpectContent', () => {
   const clicks = [];
   const render = ResultRenderer.createDefaultSelectorRowLeftRenderer({
      getTitle: (row) => row.name,
      getTitleSuffix: () => ' talk',
      getSubtitle: () => 'Africa',
      getImageSrc: () => null,
      getInfoLink: () => null,
      onTitleClick: (row) => {
         clicks.push(row.name);
      },
      shouldEnableTitleClick: () => true,
   });
   const content = render({ name: 'Lion' });
   assert.ok(content.classList.contains('itin-animal-content'));
});

test('Test_RenderSelectorResults_TestRowsToggleAndEmpty_ExpectOk', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const toggled = [];
   const selectedIds = new Set();

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows: [
         { id: 'lion', name: 'African Lion' },
         { id: 'tiger', name: 'Amur Tiger' },
      ],
      emptyText: 'No animals found',
      getId: (row) => row.id,
      isSelected: (id) => selectedIds.has(id),
      renderRowLeft: ResultRenderer.createDefaultSelectorRowLeftRenderer({
         getTitle: (row) => row.name,
         getSubtitle: () => '',
         getImageSrc: () => null,
         getInfoLink: () => null,
      }),
      onToggle: (row) => {
         if (selectedIds.has(row.id)) {
            selectedIds.delete(row.id);
         }
         else {
            selectedIds.add(row.id);
         }
         toggled.push(row.id);
      },
   });

   assert.equal(resultsEl.children.length, 2);
   resultsEl.children[0].querySelector('.itin-add-btn')?.listeners.click?.({
      stopPropagation() {},
   });
   assert.deepEqual(toggled, ['lion']);

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows: [],
      emptyText: 'No animals found',
      getId: () => '',
      isSelected: () => false,
      renderRowLeft: () => createDomNode('div'),
      onToggle: () => {},
   });
   assert.equal(resultsEl.children[0].className, 'itin-empty');
});

test('Test_RenderSelectorResults_TestMissingResultsEl_ExpectNoOp', () => {
   ResultRenderer.renderSelectorResults({
      resultsEl: null,
      rows: [],
      emptyText: 'empty',
      getId: () => '',
      isSelected: () => false,
      renderRowLeft: () => createDomNode('div'),
      onToggle: () => {},
   });
});

test('Test_RenderSelectorResults_TestBeforeToggleAdd_ExpectProceedOrder', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const proceedCalls = [];

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows: [{ id: 'lion', name: 'African Lion' }],
      emptyText: 'No animals found',
      getId: (row) => row.id,
      isSelected: () => false,
      renderRowLeft: ResultRenderer.createDefaultSelectorRowLeftRenderer({
         getTitle: (row) => row.name,
         getSubtitle: () => '',
         getImageSrc: () => null,
         getInfoLink: () => null,
      }),
      onToggle: () => {
         proceedCalls.push('toggled');
      },
      onBeforeToggleAdd: ({ proceed }) => {
         proceedCalls.push('confirmed');
         proceed();
      },
   });

   resultsEl.children[0].querySelector('.itin-add-btn')?.listeners.click?.({
      stopPropagation() {},
   });
   assert.deepEqual(proceedCalls, ['confirmed', 'toggled']);
});

test('Test_RenderSelectorResults_TestHasRowsFalse_ExpectEmptyViaBuilder', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const originalHasRows = SelectorResultRowBuilder.hasRows;
   SelectorResultRowBuilder.hasRows = () => false;

   try {
      ResultRenderer.renderSelectorResults({
         resultsEl,
         rows: [{ id: 'x' }],
         emptyText: 'None',
         getId: () => 'x',
         isSelected: () => false,
         renderRowLeft: () => createDomNode('div'),
         onToggle: () => {},
      });
      assert.equal(resultsEl.children[0].textContent, 'None');
   } finally {
      SelectorResultRowBuilder.hasRows = originalHasRows;
   }
});
