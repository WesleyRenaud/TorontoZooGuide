import assert from 'node:assert/strict';
import { test } from 'node:test';

import { createSelectorElements } from '../../scripts/itinerary/selectors/selectorControllerElements.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test.describe('createSelectorElements', () => {
   installDomTestHooks();

   test('builds the selector shell and maps element references', () => {
      const elements = createSelectorElements({
         topTitle: 'Top title',
         h1: 'Heading',
         subtitle: 'Subtitle',
      });

      assert.equal(elements.rootEl.className, 'itin-overlay');
      assert.equal(
         elements.rootEl.querySelector('.itin-top-title')?.textContent,
         'Top title'
      );
      assert.equal(
         elements.bodyEl.querySelector('.itin-h1')?.textContent,
         'Heading'
      );
      assert.equal(
         elements.bodyEl.querySelector('.itin-subtitle')?.textContent,
         'Subtitle'
      );
      assert.equal(elements.inputEl.className, 'itin-search-input');
      assert.equal(elements.resultsEl.className, 'itin-results');
      assert.equal(
         elements.nextButtonEl.textContent,
         APP_STRINGS.itinerary.actions.next
      );
      assert.equal(
         elements.finishButtonEl.textContent,
         APP_STRINGS.itinerary.actions.finish
      );
      assert.equal(
         elements.closeButtonEl.getAttribute('aria-label'),
         APP_STRINGS.itinerary.aria.closeBuilder
      );
   });

   test('omits the next button when hideNextButton is true', () => {
      const elements = createSelectorElements({
         topTitle: 'Top title',
         h1: 'Heading',
         subtitle: 'Subtitle',
         hideNextButton: true,
      });

      assert.equal(elements.nextButtonEl, null);
      assert.ok(elements.finishButtonEl);
   });
});
