import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   createDefaultSelectorRowLeftRenderer,
   createSelectorTextColumn,
   createSelectorThumb,
   renderSelectorResults,
} from '../../scripts/itinerary/selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { createDomNode } from './helpers/domNodeMock.mjs';

test.describe('selector result renderer', () => {
   installDomTestHooks();

   test('createSelectorThumb renders placeholder and image error fallback', () => {
      const placeholder = createSelectorThumb();
      assert.equal(placeholder.className, 'itin-animal-thumb is-placeholder');
      assert.equal(placeholder.children.length, 0);

      const thumb = createSelectorThumb({
         imageSrc: '../images/details/animals/lion.png',
         imageAlt: 'African Lion',
      });
      const img = thumb.querySelector('.itin-animal-thumb-img');

      assert.ok(img);
      assert.equal(img.src, '../images/details/animals/lion.png');
      assert.equal(img.alt, 'African Lion');

      img.listeners.error?.();
      assert.equal(thumb.classList.contains('is-placeholder'), true);
   });

   test('createSelectorTextColumn renders subtitle and info link', () => {
      const column = createSelectorTextColumn({
         title: 'Conservation Carousel',
         subtitle: 'Free With Admission',
         infoLink: 'https://example.com/carousel',
      });

      assert.equal(
         column.querySelector('.animal-result-species')?.textContent,
         'Conservation Carousel'
      );
      assert.equal(
         column.querySelector('.animal-result-exhibit')?.textContent,
         'Free With Admission'
      );
      assert.equal(
         column.querySelector('.tooltip-link')?.textContent,
         APP_STRINGS.common.moreInfo
      );
   });

   test('renderSelectorResults renders rows and toggles selection state', () => {
      const resultsEl = createDomNode('div', 'animal-results');
      const toggled = [];
      const selectedIds = new Set();

      renderSelectorResults({
         resultsEl,
         rows: [
            { id: 'lion', name: 'African Lion' },
            { id: 'tiger', name: 'Amur Tiger' },
         ],
         emptyText: 'No animals found',
         getId: (row) => row.id,
         isSelected: (id) => selectedIds.has(id),
         renderRowLeft: createDefaultSelectorRowLeftRenderer({
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

      const firstButton = resultsEl.children[0].querySelector('.itin-add-btn');
      assert.equal(firstButton?.textContent, APP_STRINGS.itinerary.actions.addSymbol);

      firstButton?.listeners.click?.({
         stopPropagation() {},
      });
      assert.deepEqual(toggled, ['lion']);
      assert.equal(firstButton?.textContent, APP_STRINGS.itinerary.actions.remove);
      assert.equal(firstButton?.classList.contains('is-added'), true);
   });

   test('renderSelectorResults uses onBeforeToggleAdd before adding a row', () => {
      const resultsEl = createDomNode('div', 'animal-results');
      const proceedCalls = [];

      renderSelectorResults({
         resultsEl,
         rows: [{ id: 'lion', name: 'African Lion' }],
         emptyText: 'No animals found',
         getId: (row) => row.id,
         isSelected: () => false,
         renderRowLeft: createDefaultSelectorRowLeftRenderer({
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

   test('renderSelectorResults renders empty state when there are no rows', () => {
      const resultsEl = createDomNode('div', 'animal-results');

      renderSelectorResults({
         resultsEl,
         rows: [],
         emptyText: 'No animals found',
         getId: () => '',
         isSelected: () => false,
         renderRowLeft: () => createDomNode('div'),
         onToggle: () => {},
      });

      assert.equal(resultsEl.children.length, 1);
      assert.equal(resultsEl.children[0].className, 'itin-empty');
      assert.equal(resultsEl.children[0].textContent, 'No animals found');
   });
});
