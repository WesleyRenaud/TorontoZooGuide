import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ResultRenderer } from '../../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

installDomTestHooks();


test('Test_CreateSelectorThumb_TestPlaceholder_ExpectPlaceholderClass', () => {
   const placeholder = ResultRenderer.createSelectorThumb();

   assert.equal(placeholder.className, 'itin-animal-thumb is-placeholder');
   assert.equal(placeholder.children.length, 0);
});


test('Test_CreateSelectorThumb_TestImageError_ExpectFallback', () => {
   const imageSrc = '../images/details/animals/lion.png';
   const imageAlt = 'African Lion';

   const thumb = ResultRenderer.createSelectorThumb({
      imageSrc,
      imageAlt,
   });
   const img = thumb.querySelector('.itin-animal-thumb-img');

   assert.ok(img);
   assert.equal(img.src, imageSrc);
   assert.equal(img.alt, imageAlt);
   img.listeners.error?.();
   assert.equal(thumb.classList.contains('is-placeholder'), true);
});


test('Test_CreateSelectorTextColumn_TestSubtitleAndInfoLink_ExpectNodes', () => {
   const title = 'Conservation Carousel';
   const subtitle = 'Free With Admission';
   const infoLink = 'https://example.com/carousel';

   const column = ResultRenderer.createSelectorTextColumn({
      title,
      subtitle,
      infoLink,
   });

   assert.equal(column.querySelector('.animal-result-species')?.textContent, title);
   assert.equal(column.querySelector('.animal-result-exhibit')?.textContent, subtitle);
   assert.equal(column.querySelector('.tooltip-link')?.textContent, Strings.common.moreInfo);
});


test('Test_RenderSelectorResults_TestToggle_ExpectSelectionState', () => {
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

   ResultRenderer.renderSelectorResults({
      resultsEl,
      rows,
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

   assert.equal(resultsEl.children.length, rows.length);
   const firstButton = resultsEl.children.at(Position.FIRST).querySelector('.itin-add-btn');
   assert.equal(firstButton?.textContent, Strings.itinerary.actions.addSymbol);
   firstButton?.listeners.click?.({
      stopPropagation() {},
   });
   assert.deepEqual(toggled, [lionId]);
   assert.equal(firstButton?.textContent, Strings.itinerary.actions.remove);
   assert.equal(firstButton?.classList.contains('is-added'), true);
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

   assert.equal(resultsEl.children.length, 1);
   assert.equal(resultsEl.children.at(Position.FIRST).className, 'itin-empty');
   assert.equal(resultsEl.children.at(Position.FIRST).textContent, emptyText);
});
