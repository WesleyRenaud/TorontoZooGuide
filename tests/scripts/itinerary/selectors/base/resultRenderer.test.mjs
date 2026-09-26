import assert from 'node:assert/strict';
import test from 'node:test';

import { ResultRenderer } from '../../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { SelectorResultRowBuilder } from '../../../../../scripts/itinerary/selectors/base/selectorResultRowBuilder.js';
import { SpeciesLinkTitleBuilder } from '../../../../../scripts/animals/speciesLinkTitleBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSelectorThumb_TestPlaceholder_ExpectPlaceholderClass', () => {
   const placeholder = ResultRenderer.createSelectorThumb();

   assert.equal(placeholder.className, 'itin-animal-thumb is-placeholder');
});


test('Test_CreateSelectorThumb_TestImageError_ExpectFallback', () => {
   const imageSrc = '../images/details/animals/lion.png';
   const imageAlt = 'African Lion';

   const thumb = ResultRenderer.createSelectorThumb({
      imageSrc,
      imageAlt,
   });
   const img = thumb.querySelector('.itin-animal-thumb-img');

   assert.equal(img.src, imageSrc);
   img.listeners.error?.();
   assert.equal(thumb.classList.contains('is-placeholder'), true);
});


test('Test_CreateSelectorTextColumn_TestSubtitleAndInfoLink_ExpectNodes', () => {
   const title = 'Carousel';
   const subtitle = 'Free';
   const infoLink = 'https://example.com';

   const column = ResultRenderer.createSelectorTextColumn({
      title,
      subtitle,
      infoLink,
   });

   assert.equal(column.querySelector('.animal-result-species')?.textContent, title);
   assert.equal(column.querySelector('.animal-result-exhibit')?.textContent, subtitle);
   assert.equal(column.querySelector('.tooltip-link')?.textContent, Strings.common.moreInfo);
});


test('Test_CreateSelectorTextColumn_TestCustomNodes_ExpectNodes', () => {
   const titleClass = 'custom-title';
   const subtitleClass = 'custom-subtitle';
   const titleNode = document.createElement('div');
   titleNode.className = titleClass;
   titleNode.textContent = 'Custom';
   const subtitleNode = document.createElement('div');
   subtitleNode.className = subtitleClass;

   const column = ResultRenderer.createSelectorTextColumn({
      titleNode,
      subtitleNode,
   });

   assert.ok(column.querySelector(`.${titleClass}`));
   assert.ok(column.querySelector(`.${subtitleClass}`));
});


test('Test_CreateSelectorTextColumn_TestTitleParts_ExpectSpecies', () => {
   const originalParts = SpeciesLinkTitleBuilder.createAnimalTitleLinkElement;
   const species = 'Lion';
   SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = ({ species: value }) => {
      const el = document.createElement('div');
      el.className = 'animal-result-species';
      el.textContent = value;
      return el;
   };

   try {
      const column = ResultRenderer.createSelectorTextColumn({
         titleParts: { species, enclosureName: 'Yard' },
         onTitleClick: () => {},
      });

      assert.equal(column.querySelector('.animal-result-species')?.textContent, species);
   } finally {
      SpeciesLinkTitleBuilder.createAnimalTitleLinkElement = originalParts;
   }
});


test('Test_CreateSelectorRowContent_TestThumbAndText_ExpectContent', () => {
   const textClass = 'text-col';
   const textColumnEl = document.createElement('div');
   textColumnEl.className = textClass;

   const content = ResultRenderer.createSelectorRowContent({
      imageSrc: null,
      imageAlt: '',
      textColumnEl,
   });

   assert.equal(content.className, 'itin-animal-content');
   assert.ok(content.querySelector('.itin-animal-thumb'));
   assert.ok(content.querySelector(`.${textClass}`));
});


test('Test_CreateDefaultSelectorRowLeftRenderer_TestRow_ExpectContent', () => {
   const name = 'Lion';
   const render = ResultRenderer.createDefaultSelectorRowLeftRenderer({
      getTitle: (row) => row.name,
      getTitleSuffix: () => ' talk',
      getSubtitle: () => 'Africa',
      getImageSrc: () => null,
      getInfoLink: () => null,
      onTitleClick: () => {},
      shouldEnableTitleClick: () => true,
   });

   const content = render({ name });

   assert.ok(content.classList.contains('itin-animal-content'));
});


test('Test_RenderSelectorResults_TestRowsAndToggle_ExpectOk', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const toggled = [];
   const selectedIds = new Set();
   const lionId = 'lion';
   const lionName = 'African Lion';
   const tigerId = 'tiger';
   const tigerName = 'Amur Tiger';
   const rows = [
      { id: lionId, name: lionName },
      { id: tigerId, name: tigerName },
   ];
   const emptyText = 'No animals found';

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows,
      emptyText,
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

   assert.equal(resultsEl.children.length, rows.length);
   resultsEl.children.at(Position.FIRST).querySelector('.itin-add-btn')?.listeners.click?.({
      stopPropagation() {},
   });
   assert.deepEqual(toggled, [lionId]);
});


test('Test_RenderSelectorResults_TestEmptyRows_ExpectEmptyState', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const emptyText = 'No animals found';

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows: [],
      emptyText,
      getId: () => '',
      isSelected: () => false,
      renderRowLeft: () => createDomNode('div'),
      onToggle: () => {},
   });

   assert.equal(resultsEl.children.at(Position.FIRST).className, 'itin-empty');
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
   const confirmed = 'confirmed';
   const toggled = 'toggled';
   const lionId = 'lion';
   const lionName = 'African Lion';

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows: [{ id: lionId, name: lionName }],
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
         proceedCalls.push(toggled);
      },
      onBeforeToggleAdd: ({ proceed }) => {
         proceedCalls.push(confirmed);
         proceed();
      },
   });
   resultsEl.children.at(Position.FIRST).querySelector('.itin-add-btn')?.listeners.click?.({
      stopPropagation() {},
   });

   assert.deepEqual(proceedCalls, [confirmed, toggled]);
});


test('Test_RenderSelectorResults_TestHasRowsFalse_ExpectEmptyViaBuilder', () => {
   const resultsEl = createDomNode('div', 'animal-results');
   const originalHasRows = SelectorResultRowBuilder.hasRows;
   const emptyText = 'None';
   SelectorResultRowBuilder.hasRows = () => false;

   try {
      ResultRenderer.renderSelectorResults({
         resultsEl,
         rows: [{ id: 'x' }],
         emptyText,
         getId: () => 'x',
         isSelected: () => false,
         renderRowLeft: () => createDomNode('div'),
         onToggle: () => {},
      });

      assert.equal(resultsEl.children.at(Position.FIRST).textContent, emptyText);
   } finally {
      SelectorResultRowBuilder.hasRows = originalHasRows;
   }
});
